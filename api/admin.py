"""
api/admin.py — Django admin configuration.

Registers CustomUser and TimeRecord so they are manageable
through the Django admin interface at /admin/.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TimeRecord


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin and adapts it for our employee_id login field.
    """

    # Columns shown in the list view
    list_display = ('employee_id', 'first_name', 'last_name', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

    # Fields displayed when editing an existing user
    fieldsets = (
        (None, {'fields': ('employee_id', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_id', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(TimeRecord)
class TimeRecordAdmin(admin.ModelAdmin):
    """Admin configuration for the TimeRecord model."""

    list_display = ('user', 'date', 'clock_in', 'clock_out', 'worked_hours_display', 'observation')
    list_filter = ('date',)
    search_fields = ('user__employee_id', 'user__first_name', 'user__last_name')
    ordering = ('-date', 'user__last_name')
    readonly_fields = ('worked_hours_display', 'worked_seconds', 'created_at', 'updated_at')
    date_hierarchy = 'date'

    def worked_hours_display(self, obj):
        """Show worked hours in the admin column."""
        return obj.worked_hours_display or '—'
    worked_hours_display.short_description = 'Worked Hours'

    def worked_seconds(self, obj):
        return obj.worked_seconds
    worked_seconds.short_description = 'Worked Seconds'
