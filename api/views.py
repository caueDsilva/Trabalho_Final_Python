"""
api/views.py — API Views for the Employee Time Tracking System.

Structure:
  EMPLOYEE VIEWS (require: IsAuthenticated + IsEmployee)
  --------------------------------------------------------
  ClockInView              POST /api/clock-in/
  ClockOutView             POST /api/clock-out/
  EmployeeDashboardView    GET  /api/dashboard/
  ObservationUpdateView    PATCH /api/records/<pk>/observation/

  ADMIN VIEWS (require: IsAuthenticated + IsAdmin)
  --------------------------------------------------------
  AdminTimeRecordListView  GET  /api/admin/records/?search=<name>&date=<YYYY-MM-DD>
  AdminDashboardView       GET  /api/admin/dashboard/

  USER MANAGEMENT (require: IsAuthenticated + IsAdmin)
  --------------------------------------------------------
  UserListView             GET  /api/admin/users/
  UserCreateView           POST /api/admin/users/create/
"""

from django.utils import timezone
from django.db.models import Q
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, TimeRecord
from .serializers import (
    ClockInSerializer,
    ClockOutSerializer,
    ObservationSerializer,
    TimeRecordEmployeeSerializer,
    TimeRecordAdminSerializer,
    UserSerializer,
    UserCreateSerializer,
)
from .permissions import IsEmployee, IsAdmin, IsEmployeeOwner


# ===========================================================================
# EMPLOYEE VIEWS
# ===========================================================================

class ClockInView(APIView):
    """
    POST /api/clock-in/

    Registers the employee's clock-in time for today.
    An optional observation can be included in the body.

    Employees can only clock in once per day. Returns 400 if already clocked in.

    Request body (JSON, all optional):
      { "observation": "Working from home today" }

    Response (201 Created):
      { "id": 1, "date": "2026-03-16", "clock_in": "...", "clock_out": null, ... }
    """

    permission_classes = [IsAuthenticated, IsEmployee]

    def post(self, request):
        serializer = ClockInSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            record = serializer.save()
            return Response(
                TimeRecordEmployeeSerializer(record).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClockOutView(APIView):
    """
    POST /api/clock-out/

    Registers the employee's clock-out time for today.
    Must have clocked in first. Returns 400 if not clocked in or already clocked out.

    Request body (JSON, optional):
      { "observation": "Finished all tasks" }

    Response (200 OK):
      { "id": 1, "date": "...", "clock_in": "...", "clock_out": "...", "worked_hours": "8h 00m", ... }
    """

    permission_classes = [IsAuthenticated, IsEmployee]

    def post(self, request):
        serializer = ClockOutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            record = serializer.save()
            return Response(
                TimeRecordEmployeeSerializer(record).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDashboardView(APIView):
    """
    GET /api/dashboard/

    Returns the authenticated employee's time record for today.
    If no record exists yet (employee hasn't clocked in), returns 404.

    Response (200 OK):
      {
        "id": 1,
        "date": "2026-03-16",
        "clock_in": "2026-03-16T08:00:00Z",
        "clock_out": null,
        "worked_hours": null,
        "worked_seconds": null,
        "observation": "",
        "created_at": "...",
        "updated_at": "..."
      }
    """

    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):
        today = timezone.localdate()
        record = TimeRecord.objects.filter(user=request.user, date=today).first()
        if not record:
            return Response(
                {'detail': 'No time record found for today. Clock in to start your day.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TimeRecordEmployeeSerializer(record)
        return Response(serializer.data)


class EmployeeRecordListView(generics.ListAPIView):
    """
    GET /api/records/

    For employees, returns only the authenticated employee's records.
    For admins, returns all records (for audit oversight).

    Supports optional filtering by date: ?date=YYYY-MM-DD

    Response (200 OK): List of TimeRecord objects.
    """

    permission_classes = [IsAuthenticated]  # allow admin and employee
    serializer_class = TimeRecordEmployeeSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            queryset = TimeRecord.objects.select_related('user').all()
        else:
            queryset = TimeRecord.objects.filter(user=self.request.user)

        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)
        return queryset


class ObservationUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/records/<pk>/observation/

    Allows an employee to update the observation on one of their own records.
    Only the `observation` field is accepted. Other fields are ignored.

    Request body (JSON):
      { "observation": "Updated note here" }

    Response (200 OK):
      { "id": 1, "observation": "Updated note here" }

    Returns 403 if the record does not belong to the requesting employee.
    """

    permission_classes = [IsAuthenticated, IsEmployee, IsEmployeeOwner]
    serializer_class = ObservationSerializer
    http_method_names = ['patch']  # Only allow PATCH, not PUT

    def get_queryset(self):
        # Restrict queryset to the current employee's records for security
        return TimeRecord.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        # Object-level permission check (IsEmployeeOwner)
        self.check_object_permissions(self.request, obj)
        return obj


# ===========================================================================
# ADMIN VIEWS
# ===========================================================================

class AdminTimeRecordListView(generics.ListAPIView):
    """
    GET /api/admin/records/

    Returns all time records across all employees.
    Supports filtering:
      ?search=<name>       Filter by employee first name, last name, or employee_id
      ?date=<YYYY-MM-DD>   Filter by specific date
      ?employee_id=<id>    Filter by employee's employee_id field

    Response (200 OK): Paginated list of all TimeRecord objects with nested employee info.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = TimeRecordAdminSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__employee_id',
    ]

    def get_queryset(self):
        queryset = TimeRecord.objects.select_related('user').all()

        # Optional date filter
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)

        # Optional search by employee name or ID
        search = self.request.query_params.get('search', '').strip()
        if search:
            terms = [t for t in search.split() if t]
            person_filter = Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(user__employee_id__icontains=search)
            for term in terms:
                person_filter |= Q(user__first_name__icontains=term) | Q(user__last_name__icontains=term)
            queryset = queryset.filter(person_filter)

        return queryset


class AdminDashboardView(APIView):
    """
    GET /api/admin/dashboard/

    Returns a summary for the admin dashboard showing:
      - total_employees       : Total number of employees in the system.
      - clocked_in_today      : Employees who have already clocked in today.
      - not_clocked_in_today  : Employees who have NOT clocked in yet today.
      - clocked_out_today     : Employees who have completed their workday.

    Response (200 OK):
      {
        "date": "2026-03-16",
        "total_employees": 10,
        "clocked_in_today": 7,
        "not_clocked_in_today": 3,
        "clocked_out_today": 4
      }
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        today = timezone.localdate()

        # Count total employees (exclude admins)
        total_employees = CustomUser.objects.filter(role='employee').count()

        # Employees who have a clock_in set for today
        clocked_in_today = TimeRecord.objects.filter(
            date=today,
            clock_in__isnull=False,
        ).count()

        # Employees who have completed their day (both clock_in and clock_out set)
        clocked_out_today = TimeRecord.objects.filter(
            date=today,
            clock_in__isnull=False,
            clock_out__isnull=False,
        ).count()

        not_clocked_in_today = total_employees - clocked_in_today

        return Response({
            'date': str(today),
            'total_employees': total_employees,
            'clocked_in_today': clocked_in_today,
            'not_clocked_in_today': max(not_clocked_in_today, 0),
            'clocked_out_today': clocked_out_today,
        })


class AdminEmployeeDetailView(generics.RetrieveAPIView):
    """
    GET /api/admin/employees/<pk>/

    Returns detailed info about a specific employee along with their time records.

    Response (200 OK): User info.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.filter(role='employee')


class AdminEmployeeRecordsView(generics.ListAPIView):
    """
    GET /api/admin/employees/<pk>/records/

    Returns all time records for a specific employee.
    Supports date filtering: ?date=YYYY-MM-DD

    Response (200 OK): List of TimeRecord objects for the specified employee.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = TimeRecordAdminSerializer

    def get_queryset(self):
        employee_pk = self.kwargs['pk']
        queryset = TimeRecord.objects.filter(user__pk=employee_pk).select_related('user')
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)
        return queryset


# ===========================================================================
# USER MANAGEMENT VIEWS (Admin only)
# ===========================================================================

class UserListView(generics.ListAPIView):
    """
    GET /api/admin/users/

    Lists all users in the system with their role information.
    Supports search by name: ?search=<name>

    Response (200 OK): List of user objects.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'employee_id']

    def get_queryset(self):
        return CustomUser.objects.all().order_by('last_name', 'first_name')


class UserCreateView(generics.CreateAPIView):
    """
    POST /api/admin/users/create/

    Creates a new user (employee or admin).
    Only admins can create users.

    Request body (JSON):
      {
        "employee_id": "EMP002",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "password": "securepass123",
        "role": "employee"
      }

    Response (201 Created): UserSerializer data.
    """

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
