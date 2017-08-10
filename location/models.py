from cities_light.abstract_models import (AbstractCity, AbstractCountry, AbstractRegion)
from cities_light.receivers import connect_default_signals
from django.db import models

# This contais the following models
# Country
# Region
# City
# Local Area

# ------pending -----
# CurrentLocation (user, lat, long, last_modified)


class Country(AbstractCountry):
    pass
connect_default_signals(Country)


class Region(AbstractRegion):
    pass
connect_default_signals(Region)


class City(AbstractCity):
    # you can add extra fields here
    pass
connect_default_signals(City)


class LocalArea(models.Model):
    area_name = models.CharField(max_length=200, default='')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.area_name