class IsAdmin:
    async def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return False

    async def has_object_permission(self, request, view, obj):
        return True