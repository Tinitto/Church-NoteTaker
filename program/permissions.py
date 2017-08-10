from rest_framework import permissions
from program.models import Member

class IsProgramMemberOrReadOnly(permissions.BasePermission):
    """
    This custom permission only allows members (including editors
    and admins) to edit object
    """
    def has_object_permission(self, request, view, obj):
        # read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

            # however write methods are only allowed if user is owner or a member
        # if user is owner
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass # pass if the attribute  does not exist on the object

        # in case obj is the program itself
        try:
            if obj.members and request.user in obj.members.all():
                return True

        except AttributeError:
            pass

        # in case obj is any obj related to program
        try:
            if obj.program and obj.program.members and request.user \
                    in obj.program.members.all():
                return True
        except AttributeError:
            pass # ignore if the obj doesn't have the attribute 'program

        # in case obj is authored by a member of the program
        try:
            if obj.author and obj.author.program.members and request.user \
                    in obj.author.program.members.all():
                return True
        except AttributeError:
            pass # ignore if the obj doesn't have the attribute 'author'

        # in case it is a minute i.e. linked to an agenda linked to an author
        try:
            if obj.agenda and obj.agenda.author.program.members and request.user \
                    in obj.agenda.author.program.members.all():
                return True
        except AttributeError:
            pass

        # in case it is a point linked to a minute linked to an agenda linked to an author
        try:
            if obj.minute and obj.minute.agenda.author.program.members and request.user \
                    in obj.minute.agenda.author.program.members.all():
                return True
        except AttributeError:
            pass

        return False



class IsProgramMemberOnly(permissions.BasePermission):
    """
    This custom permission only allows members of the program
    to view or edit; no one else
    """

    def has_object_permission(self, request, view, obj):
        # if user is owner
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass # if the attribute does not exist on the object then pass
        # in case obj is the program itself

        try:
            if obj.members and request.user in obj.members.all():
                return True
        except AttributeError:
            pass

        # in case obj is a meenut or any other obj related to program
        try:
            if obj.program and obj.program.members and request.user \
                    in obj.program.members.all():
                return True
        except AttributeError:
            pass

        # in case obj is authored by a member of the program
        try:
            if obj.author and obj.author.program.members and request.user \
                    in obj.author.program.members.all():
                return True
        except AttributeError:
            pass # ignore if the obj doesn't have the attribute 'author'

        # in case it is a minute i.e. linked to an agenda linked to an author
        try:
            if obj.agenda and obj.agenda.author.program.members and request.user \
                    in obj.agenda.author.program.members.all():
                return True
        except AttributeError:
            pass

        # in case it is a point linked to a minute linked to an agenda linked to an author
        try:
            if obj.minute and obj.minute.agenda.author.program.members and request.user \
                    in obj.minute.agenda.author.program.members.all():
                return True
        except AttributeError:
            pass

        return False

class IsProgramEditorOrReadOnly(permissions.BasePermission):
    """
    This custom permission only allows editors and admins of the
    program to edit the object
    """
    def has_object_permission(self, request, view, obj):
        # read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

        # however write methods are only allowed if user is owner or a member
        # who has the role of editor or admin
        # if user is owner
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass
        # in case obj is the program itself
        try:
            if obj.members and request.user in obj.members.all():
                user_details = Member.objects.get(program=obj, user=request.user)
                if user_details and (user_details.role == 'A'
                                     or user_details.role == 'E'):
                    return True
        except AttributeError:
            pass

        # in case obj is a meenut or any other obj related to program
        try:
            if obj.program and obj.program.members and request.user in obj.program.members.all():
                user_details = Member.objects.get(program=obj.program, user=request.user)
                if user_details and (user_details.role == 'A'
                                     or user_details.role == 'E'):
                    return True
        except AttributeError:
            pass # pass if the attribute of program or program.members does not exist

        # in case obj is authored by a member
        try:
            if obj.author and obj.author.program.members and request.user in obj.author.program.members.all():
                user_details = Member.objects.get(program=obj.author.program, user=request.user)
                if user_details and (user_details.role == 'A'
                                     or user_details.role == 'E'):
                    return True
        except AttributeError:
            pass # pass if the attribute of program or program.members does not exist

        # in case it is a minute i.e. linked to an agenda linked to an author
        try:
            if obj.agenda and obj.agenda.author.program.members and request.user \
                    in obj.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.agenda.author.program, user=request.user)
                if user_details and (user_details.role == 'A'
                                     or user_details.role == 'E'):
                    return True
        except AttributeError:
            pass

        # in case it is a point linked to a minute linked to an agenda linked to an author
        try:
            if obj.minute and obj.minute.agenda.author.program.members and request.user \
                    in obj.minute.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.minute.agenda.author.program, user=request.user)
                if user_details and (user_details.role == 'A'
                                     or user_details.role == 'E'):
                    return True
        except AttributeError:
            pass

        return False

class IsProgramAdminOrReadOnly(permissions.BasePermission):
    """
    This custom permission only allows program admins of the object
    to edit that object, other can only view
    """
    def has_object_permission(self, request, view, obj):
        # read requests are permitted
        if request.method in permissions.SAFE_METHODS:
            return True

        # however write methods are only allowed if user is owner or a member
        # who has the role of  admin
        # if user is owner
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass

        # in case obj is the program itself
        try:
            if obj.members and request.user in obj.members.all():
                user_details = request.user.member_set.get(program=obj)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case obj is a meenut or any other obj related to program
        try:
            if obj.program and obj.program.members and request.user \
                    in obj.program.members.all():
                user_details = request.user.member_set.get(program=obj.program)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case obj is authored by a member
        try:
            if obj.author and obj.author.program.members and request.user \
                    in obj.author.program.members.all():
                user_details = request.user.member_set.get(program=obj.author.program)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass # pass if the attribute of program or program.members does not exist


        # in case it is a minute i.e. linked to an agenda linked to an author
        try:
            if obj.agenda and obj.agenda.author.program.members and request.user \
                    in obj.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.agenda.author.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case it is a point linked to a minute linked to an agenda linked to an author
        try:
            if obj.minute and obj.minute.agenda.author.program.members and request.user \
                    in obj.minute.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.minute.agenda.author.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        return False



class IsProgramAdminOnly(permissions.BasePermission):
    """
    This custom permission only allows program admins any access to this
    object
    """

    def has_object_permission(self, request, view, obj):
        # only allowed if user is owner or a member
        # who has the role of  admin
        # if user is owner
        try:
            if obj.user and obj.user == request.user:
                return True
        except AttributeError:
            pass # pass if the user attribute doesn ot exist on the obj

        # in case obj is the program itself
        try:
            if obj.members and request.user in obj.members.all():
                user_details = Member.objects.get(program=obj, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case obj is a meenut or any other obj related to program
        try:
            if obj.program and obj.program.members and request.user in obj.program.members.all():
                user_details = Member.objects.get(program=obj.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case obj is authored by a member
        try:
            if obj.author and obj.author.program.members and request.user \
                    in obj.author.program.members.all():
                user_details = Member.objects.get(program=obj.author.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass # pass if the attribute of program or program.members does not exist

        # in case it is a minute i.e. linked to an agenda linked to an author
        try:
            if obj.agenda and obj.agenda.author.program.members and request.user \
                    in obj.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.agenda.author.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        # in case it is a point linked to a minute linked to an agenda linked to an author
        try:
            if obj.minute and obj.minute.agenda.author.program.members and request.user \
                    in obj.minute.agenda.author.program.members.all():
                user_details = Member.objects.get(program=obj.minute.agenda.author.program, user=request.user)
                if user_details and user_details.role == 'A':
                    return True
        except AttributeError:
            pass

        return False
