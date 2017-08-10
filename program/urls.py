from django.conf.urls import url, include
from rest_framework import routers
from .api import ProgramViewSet, MemberViewSet, PermittedUserAttributesViewSet


router = routers.SimpleRouter()
router.register(r'list', ProgramViewSet, base_name='cell-api-program')
router.register(r'member', MemberViewSet, base_name='cell-api-member')
router.register(r'attributes', PermittedUserAttributesViewSet, base_name='cell-api-permitteduserattributes')

urlpatterns = [
    url(r'^', include(router.urls)),
    ]
