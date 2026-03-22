"""
api/authentication.py — Custom JWT token serializer.

By default, Simple JWT uses `username` as the login field.
This overrides the token serializer to use `employee_id` instead,
matching our CustomUser model's USERNAME_FIELD.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that:
      1. Uses employee_id as the login field (inherits from USERNAME_FIELD on the model).
      2. Adds the user's role and full_name into the token claims so the frontend
         can know the role without making another API call.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Embed extra claims into the JWT payload
        token['employee_id'] = user.employee_id
        token['role'] = user.role
        token['full_name'] = user.get_full_name()

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Also append user info to the response body (not just the JWT payload)
        data['employee_id'] = self.user.employee_id
        data['role'] = self.user.role
        data['full_name'] = self.user.get_full_name()
        data['user_id'] = self.user.id

        return data


class EmployeeTokenObtainPairView(TokenObtainPairView):
    """Custom view that uses our enriched token serializer."""
    serializer_class = EmployeeTokenObtainPairSerializer
