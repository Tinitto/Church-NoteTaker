"""
Couple djangorestframework and cities_light.
adapted from cities_light

And that's all !
"""
from rest_framework import relations, serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from cities_light.loading import get_cities_models
from .models import LocalArea


Country, Region, City = get_cities_models()


class CountrySerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for Country.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cell-api-country-detail')

    class Meta:
        model = Country
        exclude = []


class RegionSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for Region.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cell-api-region-detail')
    country = relations.HyperlinkedRelatedField(
        view_name='cell-api-country-detail', read_only=True)

    class Meta:
        model = Region
        exclude = ('slug',)


class CitySerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for City.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cell-api-city-detail')
    country = relations.HyperlinkedRelatedField(
        view_name='cell-api-country-detail', read_only=True)
    region = relations.HyperlinkedRelatedField(
        view_name='cell-api-region-detail', read_only=True)

    class Meta:
        model = City
        exclude = ('slug',)


class LocalAreaSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for LocalArea
    """
    #id = serializers.IntegerField(required=False)
    url = relations.HyperlinkedIdentityField(
        view_name='cell-api-localarea-detail')
    city = relations.HyperlinkedRelatedField(required=False,
        view_name='cell-api-city-detail', queryset=City.objects.all())

    class Meta:
        model = LocalArea
        exclude = []