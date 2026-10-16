from rest_framework import permissions
from apps.properties.access import manageable_properties

class CanManageCompliance(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        property_id = getattr(obj, "property_id", None)
        if property_id is None and hasattr(obj, "property"):
            property_id = obj.property_id
        if request.method in permissions.SAFE_METHODS:
            return True
        return manageable_properties(request.user).filter(pk=property_id).exists()
