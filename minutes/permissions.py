from rest_framework import permissions


class IsPointAuthorOrReadOnly(permissions.BasePermission):
    """
    This custom permission only allows only the minute point author
    to edit the minute
    """
    def has_object_permission(self, request, view, obj):
        # read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

            # however write methods are only allowed if user is owner or a member
        # if user is owner
        try:
            if obj.author and obj.author.user == request.user:
                return True
        except AttributeError:
            pass # if obj does not

        return False