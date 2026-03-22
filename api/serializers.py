"""
api/serializers.py — DRF serializers for the Employee Time Tracking System.

Serializers:
  - UserSerializer                 : Read-only user info.
  - TimeRecordEmployeeSerializer   : Employee's own today's record (with worked hours).
  - TimeRecordAdminSerializer      : Admin view — all records with nested user info.
  - ClockInSerializer              : Validates and creates/updates clock-in.
  - ClockOutSerializer             : Validates and updates clock-out.
  - ObservationSerializer          : PATCH-only for updating the observation field.
"""

from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser, TimeRecord


# ---------------------------------------------------------------------------
# User Serializers
# ---------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for user information."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'employee_id', 'first_name', 'last_name', 'full_name', 'email', 'role']
        read_only_fields = fields

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    Passwords are hashed before saving via set_password().
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hashes the password using Django's auth system
        user.save()
        return user


# ---------------------------------------------------------------------------
# TimeRecord Serializers
# ---------------------------------------------------------------------------

class TimeRecordEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for an employee viewing their own record.
    Exposes clock_in, clock_out, worked_hours, and observation.
    Excludes user data since the employee can only see their own record.
    """

    worked_hours = serializers.SerializerMethodField(
        help_text='Total worked time as a string (e.g. "8h 30m") or null if not clocked out.'
    )
    worked_seconds = serializers.SerializerMethodField(
        help_text='Total worked seconds (numeric) or null if not clocked out.'
    )

    class Meta:
        model = TimeRecord
        fields = [
            'id', 'date', 'clock_in', 'clock_out',
            'worked_hours', 'worked_seconds', 'observation',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields

    def get_worked_hours(self, obj):
        return obj.worked_hours_display

    def get_worked_seconds(self, obj):
        return obj.worked_seconds


class TimeRecordAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for admin viewing all employee records.
    Includes nested employee information.
    """

    employee = UserSerializer(source='user', read_only=True)
    worked_hours = serializers.SerializerMethodField()
    worked_seconds = serializers.SerializerMethodField()

    class Meta:
        model = TimeRecord
        fields = [
            'id', 'employee', 'date',
            'clock_in', 'clock_out',
            'worked_hours', 'worked_seconds',
            'observation', 'created_at', 'updated_at',
        ]
        read_only_fields = fields

    def get_worked_hours(self, obj):
        return obj.worked_hours_display

    def get_worked_seconds(self, obj):
        return obj.worked_seconds


# ---------------------------------------------------------------------------
# Action Serializers (Clock In / Out / Observation)
# ---------------------------------------------------------------------------

class ClockInSerializer(serializers.Serializer):
    """
    Validates a clock-in action.

    Business rules:
      - The employee can only clock in once per day.
      - If a record already exists with clock_in set, raise a validation error.
    """

    observation = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, attrs):
        user = self.context['request'].user
        today = timezone.localdate()

        # Check if the employee has already clocked in today
        existing = TimeRecord.objects.filter(user=user, date=today).first()
        if existing and existing.clock_in is not None:
            raise serializers.ValidationError(
                {'detail': 'You have already clocked in today.'}
            )

        attrs['user'] = user
        attrs['today'] = today
        attrs['existing_record'] = existing
        return attrs

    def save(self):
        """Create (or update) today's TimeRecord with the clock_in timestamp."""
        validated = self.validated_data
        record, created = TimeRecord.objects.get_or_create(
            user=validated['user'],
            date=validated['today'],
            defaults={
                'clock_in': timezone.now(),
                'observation': validated.get('observation', ''),
            },
        )
        if not created:
            # Record already existed (e.g. observation saved earlier) — just set clock_in
            record.clock_in = timezone.now()
            if validated.get('observation'):
                record.observation = validated['observation']
            record.save()
        return record


class ClockOutSerializer(serializers.Serializer):
    """
    Validates a clock-out action.

    Business rules:
      - The employee must have clocked in first.
      - The employee can only clock out once per day.
    """

    observation = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user
        today = timezone.localdate()

        record = TimeRecord.objects.filter(user=user, date=today).first()

        if not record or record.clock_in is None:
            raise serializers.ValidationError(
                {'detail': 'You must clock in before clocking out.'}
            )
        if record.clock_out is not None:
            raise serializers.ValidationError(
                {'detail': 'You have already clocked out today.'}
            )

        attrs['record'] = record
        return attrs

    def save(self):
        """Update today's TimeRecord with the clock_out timestamp."""
        record = self.validated_data['record']
        record.clock_out = timezone.now()
        if self.validated_data.get('observation'):
            record.observation = self.validated_data['observation']
        record.save()
        return record


class ObservationSerializer(serializers.ModelSerializer):
    """
    Allows an employee to update (PATCH) the observation on any of their own records.
    Only the `observation` field is exposed.
    """

    class Meta:
        model = TimeRecord
        fields = ['id', 'observation']
