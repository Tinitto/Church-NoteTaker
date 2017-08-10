from rest_framework import viewsets
from .serializers import CitySerializer, RegionSerializer, CountrySerializer,\
    Country, City, Region, LocalAreaSerializer, LocalArea


class CitiesLightListModelViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against name_ascii.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(name_ascii__icontains=self.request.GET['q'])

        return queryset


class CountryModelViewSet(CitiesLightListModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class RegionModelViewSet(CitiesLightListModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class CityModelViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset


class LocalAreaModelViewSet(viewsets.ModelViewSet):
    """
    ListRetrieveCreateViewUpdate for LocalArea
    """
    serializer_class = LocalAreaSerializer
    queryset = LocalArea.objects.all()
