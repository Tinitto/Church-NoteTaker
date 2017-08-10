from rest_framework import permissions
# Permission for org or program admin might need to be created


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow a user to access their details for editing
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj == request.user


class IsUser(permissions.BasePermission):
    """
    Custom permission to only users to access their private details
    """

    def has_object_permission(self, request, view, obj):
        # permissions are only allowed to the owner of the snippet.
        return obj == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or view it.
    """

    def has_object_permission(self, request, view, obj):
        # permissions are only allowed to the owner of the snippet.
        # if it the object is a profile - an extension of the user
        try:
            if obj.user:
                return obj.user == request.user
        except AttributeError:
            pass # pass if the obj doesn't have the attribute user

        try:
            if obj.profile:
                return obj.profile.user == request.user
        except AttributeError:
            pass # pass if the obj doesn't have the profile attribute

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            if obj.user:
                return obj.user == request.user
        except AttributeError:
            pass  # pass if the obj doesn't have the attribute user

        try:
            if obj.profile:
                return obj.profile.user == request.user
        except AttributeError:
            pass  # pass if the obj doesn't have the profile attribute

        return False


class IsAppAdminOrReadOnly(permissions.BasePermission):
    """
    Allow editing to be for only App Admin This is completetly useless
    It is like it never runs. use the IsAdmin
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return request.user and request.user.is_staff
        # return request.user.is_staff

