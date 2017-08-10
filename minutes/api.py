from rest_framework import viewsets, permissions
from .serializers import ReferenceSerializer, Reference, \
    Agenda, AgendaSerializer, Minute, MinuteSerializer, Point, \
    PointSerializer #, AgendaViewSerializer
from program import permissions as program_permissions
from .permissions import IsPointAuthorOrReadOnly


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()#.\
       # filter(author__program__organization__approved=True)
    serializer_class = AgendaSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        program_permissions.IsProgramEditorOrReadOnly
    )

#class AgendaPublicViewSet(viewsets.ModelViewSet):
#    queryset = Agenda.objects.all()  # .\
#    # filter(author__program__organization__approved=True)
#    serializer_class = AgendaViewSerializer
#    permission_classes = (
#        permissions.IsAuthenticatedOrReadOnly,
#    )

#    def perform_create(self, serializer):
#        serializer.save(current_user=self.request.user)

#    def perform_update(self, serializer):
 #       serializer.save(current_user=self.request.user)


class MinuteViewSet(viewsets.ModelViewSet):
    queryset = Minute.objects.all()#.\
        #filter(agenda__author__program__organization__approved=True)
    serializer_class = MinuteSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
       # program_permissions.IsProgramEditorOrReadOnly,
        program_permissions.IsProgramMemberOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(current_user=self.request.user) #  I may need to ass this field in serializer

    def perform_update(self, serializer):
        serializer.save(current_user=self.request.user)


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()#.\
        #filter(minute__agenda__author__program__organization__approved=True)
    serializer_class = PointSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        program_permissions.IsProgramMemberOrReadOnly,
        IsPointAuthorOrReadOnly
    )
