from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsSuperuserOrReadOnly(BasePermission):
    """
    Custom permission class to allow access to superusers or read-only access for other users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )
