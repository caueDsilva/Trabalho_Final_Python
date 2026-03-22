"""
api/urls.py — URL routing for all API endpoints.

Employee Routes:
  POST  /api/clock-in/                         — Clock in for today
  POST  /api/clock-out/                        — Clock out for today
  GET   /api/dashboard/                        — Employee's today record
  GET   /api/records/                          — All of employee's records
  PATCH /api/records/<pk>/observation/         — Update observation on a record

Admin Routes:
  GET   /api/admin/records/                    — All records (with search & date filter)
  GET   /api/admin/dashboard/                  — Summary (clocked-in counts)
  GET   /api/admin/users/                      — List all users
  POST  /api/admin/users/create/               — Create new user
  GET   /api/admin/employees/<pk>/             — Employee detail
  GET   /api/admin/employees/<pk>/records/     — All records for a specific employee
"""

from django.urls import path
from .views import (
    # Employee views
    ClockInView,
    ClockOutView,
    EmployeeDashboardView,
    EmployeeRecordListView,
    ObservationUpdateView,
    # Admin views
    AdminTimeRecordListView,
    AdminDashboardView,
    AdminEmployeeDetailView,
    AdminEmployeeRecordsView,
    # User management
    UserListView,
    UserCreateView,
)

urlpatterns = [

    # ------------------------------------------------------------------
    # EMPLOYEE ENDPOINTS
    # ------------------------------------------------------------------

    # Clock in — creates or fills today's time record
    path('clock-in/', ClockInView.as_view(), name='clock-in'),

    # Clock out — fills the clock_out field on today's record
    path('clock-out/', ClockOutView.as_view(), name='clock-out'),

    # Employee dashboard — today's record for the authenticated employee
    path('dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),

    # Full history of the authenticated employee's records
    path('records/', EmployeeRecordListView.as_view(), name='employee-records'),

    # Update observation on a specific record (PATCH only)
    path('records/<int:pk>/observation/', ObservationUpdateView.as_view(), name='update-observation'),

    # ------------------------------------------------------------------
    # ADMIN ENDPOINTS
    # ------------------------------------------------------------------

    # All time records across all employees (supports ?search=name, ?date=YYYY-MM-DD)
    path('admin/records/', AdminTimeRecordListView.as_view(), name='admin-records'),

    # Dashboard summary (total employees, clocked-in count, not-clocked-in count)
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),

    # Specific employee detail
    path('admin/employees/<int:pk>/', AdminEmployeeDetailView.as_view(), name='admin-employee-detail'),

    # All records for a specific employee
    path('admin/employees/<int:pk>/records/', AdminEmployeeRecordsView.as_view(), name='admin-employee-records'),

    # ------------------------------------------------------------------
    # USER MANAGEMENT (Admin only)
    # ------------------------------------------------------------------

    # List all users in the system
    path('admin/users/', UserListView.as_view(), name='admin-user-list'),

    # Create a new employee or admin user
    path('admin/users/create/', UserCreateView.as_view(), name='admin-user-create'),
]
