"""
Management command: create_admin

Usage:
    python manage.py create_admin

Creates an admin user interactively. Useful for initial setup when
there are no users in the database yet (since only admins can create users via the API).
"""

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from api.models import CustomUser


class Command(BaseCommand):
    help = 'Interactively create an admin user for initial system setup.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Create Admin User ===\n'))

        employee_id = input('Employee ID (e.g. ADMIN001): ').strip()
        first_name  = input('First name: ').strip()
        last_name   = input('Last name: ').strip()
        email       = input('Email: ').strip()

        import getpass
        password = getpass.getpass('Password: ')
        password2 = getpass.getpass('Confirm password: ')

        if password != password2:
            self.stderr.write(self.style.ERROR('Passwords do not match. Aborting.'))
            return

        try:
            user = CustomUser(
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role='admin',
                is_staff=True,       # Allows access to Django admin site
                is_superuser=True,   # Full permissions on admin site
            )
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nAdmin user "{employee_id}" ({first_name} {last_name}) created successfully!'
                )
            )
        except IntegrityError:
            self.stderr.write(
                self.style.ERROR(f'Error: Employee ID "{employee_id}" is already taken.')
            )
