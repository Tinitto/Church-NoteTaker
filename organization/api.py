from rest_framework import viewsets, permissions
from .models import Organization, Category, Branch
from .serializers import OrganizationSerializer, CategorySerializer, \
    BranchSerializer
from user import permissions as user_permissions
from .permissions import IsOrganizationAdminOrReadOnly

class SearcheableModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against name.
        """
        queryset = super(SearcheableModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])

        return queryset


class CategoryViewSet(SearcheableModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          user_permissions.IsAppAdminOrReadOnly,)


class OrganizationViewSet(SearcheableModelViewSet):
    queryset = Organization.objects.all()#.filter(approved=True)
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # to ensure the user is saved in the model as the woner
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BranchViewSet(SearcheableModelViewSet):
    queryset = Branch.objects.all()#.filter(organization__approved=True)
    serializer_class = BranchSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOrganizationAdminOrReadOnly)
