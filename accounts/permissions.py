from rest_framework import permissions 


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create or modify objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # allow read-only access for all users
            return True
        else:
            # only allow write access for admins
            return request.user.is_authenticated and request.user.is_staff
