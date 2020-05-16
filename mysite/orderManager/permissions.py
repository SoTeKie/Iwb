from rest_framework import permissions
from django.db.models import Q

class OrderPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET','PATCH', 'DELETE']:
            return request.user.groups.filter(name="Bartender").exists() or request.user.is_staff

        if request.method == 'POST':
            return request.user.groups.filter(name="Table").exists()


class ItemPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user and request.user.is_authenticated)

        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.is_staff and request.user