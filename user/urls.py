from django.conf.urls import url, include
from rest_framework import routers, renderers
from .api import UserUpdateViewSet, UserViewSet, ProfileViewSet, CreateUserView, ActivateUserViewSet


router = routers.SimpleRouter()
router.register(r'list', UserViewSet, base_name='cell-api-user')
router.register(r'update', UserUpdateViewSet, base_name='cell-api-userupdate')
router.register(r'profile', ProfileViewSet, base_name='cell-api-userprofile')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^add/', CreateUserView.as_view()),
    url(r'^activate/', ActivateUserViewSet.as_view({'get':'activate'},
                                                   renderer_classes=[renderers.StaticHTMLRenderer]),
        name='user-activate'),
]