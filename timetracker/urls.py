"""
URL Configuration for the timetracker project.

Endpoints summary:
  /api/token/           — Obtain JWT access + refresh tokens (POST)
  /api/token/refresh/   — Refresh an access token (POST)
  /api/                 — All application endpoints (see api/urls.py)
  /admin/               — Django admin site
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from api.authentication import EmployeeTokenObtainPairView

urlpatterns = [
    # Django administration
    path('admin/', admin.site.urls),

    # JWT authentication endpoints
    # Uses custom view: login with employee_id + password, response includes role & full_name
    path('api/token/', EmployeeTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # All API endpoints
    path('api/', include('api.urls')),
]
