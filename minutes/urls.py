from rest_framework import routers
from django.conf.urls import url, include
from .api import ReferenceViewSet, AgendaViewSet, MinuteViewSet, \
    PointViewSet

router = routers.SimpleRouter()
router.register(r'agenda', AgendaViewSet, base_name='cell-api-agenda')
router.register(r'minute', MinuteViewSet, base_name='cell-api-minute')
router.register(r'point', PointViewSet, base_name='cell-api-point')
router.register(r'reference', ReferenceViewSet, base_name='cell-api-reference')

urlpatterns = [
    url(r'^', include(router.urls)),
]