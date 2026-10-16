from rest_framework import permissions
from .access import editable_properties

class PropertyWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return editable_properties(request.user).filter(pk=obj.pk).exists()

class OwnerWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return editable_properties(request.user).filter(pk=obj.property_id).exists()
