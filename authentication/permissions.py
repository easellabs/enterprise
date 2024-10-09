from django.utils.functional import cached_property
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile

User = get_user_model()

# class IsRole(BasePermission):
#     """
#     Base permission class to check user roles.
#     Subclasses should define the required_role attribute.
#     """

#     required_role = None

#     def has_permission(self, request, view):
#         # Ensure the user is authenticated
#         if not request.user or not request.user.is_authenticated:
#             return False

#         # Check if the user has a profile and if the role matches
#         try:
#             user_profile = request.user.profile
#             return user_profile.role == self.required_role
#         except (ObjectDoesNotExist, AttributeError):
#             # User does not have a profile or userprofile does not exist
#             return False


# class IsAdmin(IsRole):
#     """
#     Permission class to check if the user is an Admin.
#     """
#     required_role = 'Admin'


# class IsEmployee(IsRole):
#     """
#     Permission class to check if the user is an Employee.
#     """
#     required_role = 'Employee'
