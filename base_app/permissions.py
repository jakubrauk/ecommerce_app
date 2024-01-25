from rest_framework.permissions import BasePermission


class IsAdminOrSalesmanPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.groups.all())
        return request.user.groups.filter(name='Salesman').exists() or request.user.is_superuser
