from rest_framework import routers
from django.conf.urls import url, include
from .api import CityModelViewSet, LocalAreaModelViewSet, \
    CountryModelViewSet, RegionModelViewSet

router = routers.SimpleRouter()
router.register(r'localarea', LocalAreaModelViewSet,
                base_name='cell-api-localarea')
router.register(r'city', CityModelViewSet,
                base_name='cell-api-city')
router.register(r'country', CountryModelViewSet,
                base_name='cell-api-country')
router.register(r'region', RegionModelViewSet,
                base_name='cell-api-region')


urlpatterns = [
    url(r'^', include(router.urls)),
]
