from rest_framework import serializers
from ..models import Country, Region, GeoIP
from netbox.api.serializers import NetBoxModelSerializer


class CountrySerializer(NetBoxModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code', 'display']


class RegionSerializer(NetBoxModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'country', 'subdivision_code', 'display']


class GeoIPSerializer(NetBoxModelSerializer):
    subnet = serializers.CharField(read_only=True)
    country = serializers.CharField(source='country.name', read_only=True)
    country_code = serializers.CharField(source='country.country_code', read_only=True)
    region = serializers.CharField(read_only=True)
    subdivision_code = serializers.CharField(read_only=True)

    class Meta:
        model = GeoIP
        fields = ['subnet', 'country', 'country_code', 'region', 'subdivision_code', 'city', 'status']

