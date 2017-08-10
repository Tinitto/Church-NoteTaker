from rest_framework import viewsets, permissions
from .models import PermittedUserAttributes, Program, Member
from .serializers import ProgramSerializer, PermittedUserAttributesSerializer, \
    MemberSerializer
from organization import permissions as org_permissions
from user.api import SearcheableUserModelViewSet
from organization.api import SearcheableModelViewSet
from .permissions import IsProgramAdminOrReadOnly


class PermittedUserAttributesViewSet(viewsets.ModelViewSet):
    queryset = PermittedUserAttributes.objects.all().filter(program__organization__approved=True)
    serializer_class = PermittedUserAttributesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          org_permissions.IsOrganizationAdminOrReadOnly)


class MemberViewSet(SearcheableUserModelViewSet):
    """
    Only Program admins are allowed to edit or approve members
    """
    queryset = Member.objects.all()#.filter(program__organization__approved=True)
    serializer_class = MemberSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsProgramAdminOrReadOnly)


class ProgramViewSet(SearcheableModelViewSet):
    """
    Only Organization admins are allowed to edit any program
    """
    queryset = Program.objects.all()#.filter(organization__approved=True)
    serializer_class = ProgramSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          org_permissions.IsOrganizationAdminOrReadOnly)
