"""
api/models.py — Data models for the Employee Time Tracking System.

Models:
  - CustomUser  : Extends Django's AbstractUser, adds employee_id (login field) and role.
  - TimeRecord  : Stores clock-in / clock-out data and observations for each employee per day.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that replaces the default username login with employee_id.

    Roles:
      - 'employee' : Regular employee, can only see their own records.
      - 'admin'    : Administrator, can see all employee records.
    """

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    ]

    # The employee_id field is used as the unique login identifier
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Employee ID',
        help_text='Unique identifier used for login (e.g. EMP001)',
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='Role',
    )

    # Remove the default username field — we use employee_id instead
    username = None

    # Tell Django to use employee_id for authentication instead of username
    USERNAME_FIELD = 'employee_id'

    # Fields required when creating a superuser (in addition to USERNAME_FIELD + password)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.employee_id}) — {self.get_role_display()}'

    @property
    def full_name(self):
        return self.get_full_name()


class TimeRecord(models.Model):
    """
    Stores a single workday record for an employee.

    Each employee has at most ONE TimeRecord per calendar day (enforced by unique_together).
    The `observation` field is optional and can be updated at any time by the employee.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='time_records',
        verbose_name='Employee',
    )

    date = models.DateField(
        verbose_name='Work Date',
        help_text='The calendar date this record belongs to (auto-set to today on creation)',
    )

    clock_in = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Clock In',
        help_text='Timestamp when the employee clocked in',
    )

    clock_out = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Clock Out',
        help_text='Timestamp when the employee clocked out',
    )

    observation = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observation',
        help_text='Optional note added by the employee for this record',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Time Record'
        verbose_name_plural = 'Time Records'
        # One record per employee per day
        unique_together = ('user', 'date')
        ordering = ['-date', '-clock_in']

    def __str__(self):
        return f'{self.user.employee_id} — {self.date}'

    @property
    def worked_seconds(self):
        """Return total worked seconds for the day, or None if not yet clocked out."""
        if self.clock_in and self.clock_out:
            delta = self.clock_out - self.clock_in
            return int(delta.total_seconds())
        return None

    @property
    def worked_hours_display(self):
        """
        Return worked time as a human-readable string, e.g. '8h 30m'.
        Returns None if the employee has not clocked out yet.
        """
        seconds = self.worked_seconds
        if seconds is None:
            return None
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        return f'{hours}h {minutes:02d}m'
