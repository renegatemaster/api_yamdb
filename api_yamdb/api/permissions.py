from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrAdmins(BasePermission):
    """Разрешение на уровне владелец или админ."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (obj == request.user
                or request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return False


class IsAuthor(BasePermission):
    """Разрешение на уровне автора."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsStaff(BasePermission):
    """Разрешение на уровне персонала."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )
