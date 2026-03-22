"""
api/permissions.py — Custom DRF permission classes.

Classes:
  - IsEmployee      : Allows access only to users with role='employee'.
  - IsAdmin         : Allows access only to users with role='admin'.
  - IsEmployeeOwner : Allows employee to access their own TimeRecord only.
"""

from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Grants access only to authenticated users with the 'employee' role.
    Used on all employee-facing endpoints to prevent admins from using those routes.
    """
    message = 'Access restricted to employees.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'employee'
        )


class IsAdmin(BasePermission):
    """
    Grants access only to authenticated users with the 'admin' role.
    Used on all admin-facing endpoints.
    """
    message = 'Access restricted to administrators.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsEmployeeOwner(BasePermission):
    """
    Object-level permission: an employee can only access records that belong to them.
    Applied in conjunction with IsEmployee on detail views.
    """
    message = 'You do not have permission to access this record.'

    def has_object_permission(self, request, view, obj):
        # obj is a TimeRecord — check that it belongs to the requesting user
        return obj.user == request.user
