import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Country, Region, GeoIP
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


AVAILABLE_LABEL = mark_safe('<span class="badge text-bg-success">Available</span>')


class CountryTable(NetBoxTable):
    name = tables.Column(linkify=True, verbose_name="country")

    class Meta(NetBoxTable.Meta):
        model = Country
        fields = (
            'pk', 'id', 'name', 'country_code', 'created', 'last_updated',
        )
        default_columns = (
            'pk', 'name', 'country_code',
        )
        row_attrs = {
            'class': lambda record: 'success' if not isinstance(record, Country) else '',
        }


class RegionTable(NetBoxTable):
    name = tables.Column(linkify=True, verbose_name="region")
    country = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Region
        fields = (
            'pk', 'id', 'name', 'country', 'subdivision_code', 'created', 'last_updated',
        )
        default_columns = (
            'pk', 'name', 'country', 'subdivision_code',
        )
        row_attrs = {
            'class': lambda record: 'success' if not isinstance(record, Region) else '',
        }


class GeoIPTable(NetBoxTable):
    subnet = tables.Column(linkify=True)
    country_code = tables.columns.Column(
        accessor="country.country_code",
        verbose_name="Country Code",
    )
    subdivision_code = tables.columns.Column(
        verbose_name="Subd Code"
    )

    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status'),
        default=AVAILABLE_LABEL
    )

    class Meta(NetBoxTable.Meta):
        model = GeoIP
        fields = ("pk", "subnet", "country", "country_code", "region", "subdivision_code", "city", "status", "type")
        default_columns = ("subnet", "country", "country_code", "region", "subdivision_code", "city", "status")
        exclude = ('pk', 'actions',)
        row_attrs = {
            'class': lambda record: 'success' if not record.pk else '',
        }


