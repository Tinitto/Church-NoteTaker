from django.conf.urls import url, include
from rest_framework import routers
from .api import OrganizationViewSet, CategoryViewSet, BranchViewSet

router = routers.SimpleRouter()
router.register(r'list', OrganizationViewSet, base_name='cell-api-organization')
router.register(r'category', CategoryViewSet, base_name='cell-api-org-category')
router.register(r'branch', BranchViewSet, base_name='cell-api-org-branch')

urlpatterns = [
    url(r'^', include(router.urls)),
    ]