from rest_framework import permissions


# write another for only admins, editors, members of org or prog
class IsOrganizationAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users that are that organizations' admins
    to edit it
    """
    def has_object_permission(self, request, view, obj):
        #read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

    # however write methods are only allowed if user is owner or an admin
        #if user is owner
        # this obj.user stuff doesn't work
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass

            # in case obj is the organization itself
        try:
            if obj.admins and request.user in obj.admins.all():
                return True
        except AttributeError:
            pass

            # in case obj is a program or any other obj related to organization
        try:
            if obj.organization and request.user in obj.organization.admins.all():
                return True
        except AttributeError:
            pass

        try:
            if obj.organization and request.user == obj.organization.user:
                return True
        except AttributeError:
            pass

        # in case the obj belongs to a something that belongs to a program
        try:
            if obj.program and request.user in obj.program.organization.admins.all():
                return True
        except AttributeError:
            pass

        try:
            if obj.program and request.user == obj.program.organization.user:
                return True
        except AttributeError:
            pass

            # in case obj belongs to an autthor who is a member of a program
        try:
            if obj.author and request.user == obj.author.program.organization.user:
                return True
        except AttributeError:
            pass

        return False



# write another for only admins, editors, members of org or prog
class IsOrganizationCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users that are that organizations' admins
    to edit it
    """

    def has_object_permission(self, request, view, obj):
        # read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

        # however write methods are only allowed if user is owner
        # if user is owner and this is an organization instance
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError: # if object doesn't have the user atribute, pass
            pass

        # in case obj is a program or any other obj related to organization
        try:
            if obj.organization and request.user == obj.organization.user:
                return True
        except AttributeError:
            pass

        # in case obj belongs to a program
        try:
            if obj.program and request.user == obj.program.organization.user:
                return True
        except AttributeError:
            pass

        # in case obj belongs to an autthor who is a member of a program
        try:
            if obj.author and request.user == obj.author.program.organization.user:
                return True
        except AttributeError:
            pass

        return False

