from netbox.api.viewsets import NetBoxModelViewSet
from ..models import Country, Region, GeoIP
from .serializers import CountrySerializer, RegionSerializer, GeoIPSerializer
from .. import filtersets


class CountryViewSet(NetBoxModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_class = filtersets.CountryFilterSet


class RegionViewSet(NetBoxModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_class = filtersets.RegionFilterSet


class GeoIPViewSet(NetBoxModelViewSet):
    queryset = GeoIP.objects.all()
    serializer_class = GeoIPSerializer
    filterset_class = filtersets.GeoIPFilterSet
