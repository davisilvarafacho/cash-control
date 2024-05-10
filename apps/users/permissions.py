from rest_framework.permissions import BasePermission


class AllowCreateWithoutAuth(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated
