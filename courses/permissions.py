from rest_framework.permissions import BasePermission

class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated and has the user_type 'admin'
        return request.user.is_authenticated and request.user.user_type == 'admin'
