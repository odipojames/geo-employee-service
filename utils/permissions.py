from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsEmployeeOrAdmin(permissions.BasePermission):
    """
    permissions for creating and editing  employees
    """
    message = "you must have rights  to perform this"

    def has_permission(self, request, view):
        if str(request.user.role) == "management" or str(request.user.role) == "staff" and request.method in SAFE_METHODS:
            return True
        return (
            str(request.user.role) == "superuser"
            or str(request.user.role) == "admin"
        )
        
        

