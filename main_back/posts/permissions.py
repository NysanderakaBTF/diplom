class IsAdmin:
    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthenticated:
    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthorOrAdmin:
    """
    Custom permission to allow access only to the author of the post or admins.
    """
    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the author or an admin
        return request.user == obj.author or request.user.is_staff
