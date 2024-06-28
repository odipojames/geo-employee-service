from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin to perform all CRUD operations.
    Other roles (management, staff, tech_lead) can only list and view.
    """
    message = "You must have rights to perform this action."

    def has_permission(self, request, view):
        # Allow only GET, HEAD, and OPTIONS requests for non-admin users
        if request.method in SAFE_METHODS:
            return True
        
        # Allow all CRUD operations for admin users
        return request.user.role in ["superuser", "admin"]

    def has_object_permission(self, request, view, obj):
        # Allow only GET, HEAD, and OPTIONS requests for non-admin users
        if request.method in SAFE_METHODS:
            return True
        
        # Allow all CRUD operations for admin users
        return request.user.role in ["superuser", "admin"]

        
        

