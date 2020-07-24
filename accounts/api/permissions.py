from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    message = 'You are already authenticated. Please log out to try again.'
    """
    Non-authenicated Users only
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated # request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    message  = 'You must be the owner of this content to change.'
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        # if obj.user == request.user:
        #     return True
        return obj.owner == request.user