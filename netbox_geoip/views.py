from utilities.views import register_model_view
from .models import Country, Region, GeoIP
from . import forms, filtersets

from netbox.views import generic
from . import tables
from ipam.views import PrefixEditView, PrefixBulkEditView, IPAddressEditView, IPAddressBulkEditView


#
# Country
#
class CountryListView(generic.ObjectListView):
    queryset = Country.objects.all()
    filterset = filtersets.CountryFilterSet
    filterset_form = forms.CountryFilterForm
    table = tables.CountryTable


@register_model_view(Country)
class CountryView(generic.ObjectView):
    queryset = Country.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (Region.objects.restrict(request.user, 'view').filter(country=instance), 'country'),
            (GeoIP.objects.restrict(request.user, 'view').filter(country=instance), 'country'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(Country, 'edit')
class CountryCreateView(generic.ObjectEditView):
    queryset = Country.objects.all()
    form = forms.CountryForm


@register_model_view(Country, 'delete')
class CountryDeleteView(generic.ObjectDeleteView):
    queryset = Country.objects.all()


class CountryBulkImportView(generic.BulkImportView):
    queryset = Country.objects.all()
    model_form = forms.CountryImportForm


class CountryBulkEditView(generic.BulkEditView):
    queryset = Country.objects.all()
    filterset = filtersets.CountryFilterSet
    table = tables.CountryTable
    form = forms.CountryBulkEditForm


class CountryBulkDeleteView(generic.BulkDeleteView):
    queryset = Country.objects.all()
    table = tables.CountryTable


#
# Region
#
class RegionListView(generic.ObjectListView):
    queryset = Region.objects.all()
    filterset = filtersets.RegionFilterSet
    filterset_form = forms.RegionFilterForm
    table = tables.RegionTable


@register_model_view(Region)
class RegionView(generic.ObjectView):
    queryset = Region.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (GeoIP.objects.restrict(request.user, 'view').filter(region=str(instance.name)), 'region'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(Region, 'edit')
class RegionCreateView(generic.ObjectEditView):
    queryset = Region.objects.all()
    form = forms.RegionForm


@register_model_view(Region, 'delete')
class RegionDeleteView(generic.ObjectDeleteView):
    queryset = Region.objects.all()


class RegionBulkImportView(generic.BulkImportView):
    queryset = Region.objects.all()
    model_form = forms.RegionImportForm


class RegionBulkEditView(generic.BulkEditView):
    queryset = Region.objects.all()
    filterset = filtersets.RegionFilterSet
    table = tables.RegionTable
    form = forms.RegionBulkEditForm


class RegionBulkDeleteView(generic.BulkDeleteView):
    queryset = Region.objects.all()
    table = tables.RegionTable


#
# To override Prefix/IPAddress Forms
#
class CustomPrefixAddView(PrefixEditView):
    form = forms.CustomPrefixForm


class CustomPrefixBulkEditView(PrefixBulkEditView):
    form = forms.CustomBulkPrefixForm


class CustomPrefixEditView(PrefixEditView):
    form = forms.CustomPrefixForm


class CustomIPAddressAddView(IPAddressEditView):
    form = forms.CustomIPAddressForm


class CustomIPAddressBulkEditView(IPAddressBulkEditView):
    form = forms.CustomBulkIPAddressForm


class CustomIPAddressEditView(IPAddressEditView):
    form = forms.CustomIPAddressForm


#
# GeoIP
#
class GeoIPListView(generic.ObjectListView):
    queryset = GeoIP.objects.all()
    filterset = filtersets.GeoIPFilterSet
    filterset_form = forms.GoeIPFilterForm
    table = tables.GeoIPTable
