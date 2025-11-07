import django_filters
import netaddr
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from netbox.filtersets import NetBoxModelFilterSet, BaseFilterSet

from netaddr.core import AddrFormatError
from .models import *


class CountryFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Country
        fields = ('id', 'name', 'country_code')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value) |
                Q(country_code__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class RegionFilterSet(NetBoxModelFilterSet):
    country_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.objects.all(),
        label=_('Country (ID)'),
    )
    country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.objects.all(),
        field_name="country",
        label=_("Country"),
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name="name",
        label=_("Region"),
    )

    class Meta:
        model = Region
        fields = ('id', 'name', 'region', 'country', 'country_id', 'subdivision_code')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(country__name__icontains=value) |
            Q(subdivision_code__icontains=value)
        )


class GeoIPFilterSet(BaseFilterSet):
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        method="filter_region",
        label=_("Region"),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=GoeIPStatusChoices,
        null_value=None
    )

    class Meta:
        model = GeoIP
        fields = ('id', 'country', 'region', 'subdivision_code', 'city', 'status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(city__icontains=value)
        qs_filter |= Q(region__icontains=value)
        qs_filter |= Q(country__name__icontains=value)
        qs_filter |= Q(country__country_code__icontains=value)
        qs_filter |= Q(region__icontains=value)
        qs_filter |= Q(subdivision_code__icontains=value)
        qs_filter |= Q(subnet__contains=value.strip())
        try:
            prefix = str(netaddr.IPNetwork(value.strip()).cidr)
            qs_filter |= Q(subnet__net_contains_or_equals=prefix)
            qs_filter |= Q(subnet__contains=value.strip())
        except (AddrFormatError, ValueError):
            pass
        return queryset.filter(qs_filter)

    def filter_region(self, queryset, name, value):
        if (len(value) == 0):
            return queryset
        try:
            return queryset.filter(region__in=value)
        except ValidationError:
            return queryset



