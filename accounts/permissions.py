from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsJobSeeker(BasePermission):
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.role == 1


class IsEmployer(BasePermission):
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.role == 2


class IsEmployerOrAdmin(BasePermission):
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.role in [2, 3]
