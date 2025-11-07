from django import forms
from netbox.forms import NetBoxModelForm
from ipam.forms import PrefixForm, PrefixBulkEditForm, IPAddressForm, IPAddressBulkEditForm
from netbox.forms import NetBoxModelBulkEditForm
from .models import Country, Region, GeoIP, GoeIPStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from netbox.forms import NetBoxModelImportForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, TagFilterField


#
# Country Forms
#
class CountryForm(NetBoxModelForm):
    name = forms.CharField(
        label=_('Country'),
        max_length=100,
        required=True
    )
    country_code = forms.CharField(
        label=_('Country Code'),
        max_length=2,
        required=True
    )

    class Meta:
        model = Country
        fields = ("name", "country_code")


class CountryBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(
        label=_('Country'),
        max_length=100,
        required=True
    )
    country_code = forms.CharField(
        label=_('Country Code'),
        max_length=2,
        required=True
    )

    model = Country
    fieldsets = (
        FieldSet('name', 'country_code',),
    )


class CountryImportForm(NetBoxModelImportForm):
    name = forms.CharField(
        label=_('Country'),
        max_length=100,
        required=True
    )
    country_code = forms.CharField(
        label=_('Country Code'),
        max_length=2,
        required=True
    )

    class Meta:
        model = Country
        fields = ('name', 'country_code')


class CountryFilterForm(NetBoxModelFilterSetForm):
    model = Country
    fieldsets = (
        FieldSet('q', 'filter_id'),
    )
    tag = TagFilterField(model)


#
# Region Forms
#
class RegionForm(NetBoxModelForm):
    name = forms.CharField(
        label=_('Region'),
        max_length=100,
        required=True
    )
    country = DynamicModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        label=_('Country')
    )
    subdivision_code = forms.CharField(
        label=_('Subdivision Code'),
        max_length=10,
        required=True
    )

    class Meta:
        model = Region
        fields = ("name", "country", "subdivision_code")


class RegionBulkEditForm(NetBoxModelBulkEditForm):
    name = forms.CharField(
        label=_('Region'),
        max_length=100,
        required=False
    )
    country = DynamicModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        label=_('Country')
    )

    subdivision_code = forms.CharField(
        label=_('Subdivision Code'),
        max_length=10,
        required=True
    )

    model = Region
    fieldsets = (
        FieldSet('name', 'country', 'subdivision_code'),
    )


class RegionImportForm(NetBoxModelImportForm):
    name = forms.CharField(
        label=_('Region'),
        max_length=100,
        required=False
    )
    country = DynamicModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        label=_('Country')
    )

    subdivision_code = forms.CharField(
        label=_('Subdivision Code'),
        max_length=10,
        required=True
    )

    class Meta:
        model = Region
        fields = ('name', 'country', 'subdivision_code')


class RegionFilterForm(NetBoxModelFilterSetForm):
    model = Region
    fieldsets = (
        FieldSet('q', 'filter_id'),
        FieldSet('country', 'region', name=_('Attributes')),
    )

    selector_fields = ('filter_id', 'q', 'country')

    country = DynamicModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label=_('Country')
    )

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        query_params={"country": "$country"},
        label=_('Region')
    )

    tag = TagFilterField(model)


#
# GeoIP Forms
#
class GoeIPFilterForm(NetBoxModelFilterSetForm):
    model = GeoIP
    fieldsets = (
        FieldSet('q', 'filter_id'),
        FieldSet('country', 'region', 'city', 'status', name=_('Attributes')),
    )
    selector_fields = ('filter_id', 'q', 'country')

    country = DynamicModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label=_('Country')
    )

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        query_params={"country": "$country"},
        label=_('Region')
    )

    city = forms.MultipleChoiceField(
        choices=[],
        required=False,
        label=_('City')
    )

    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=GoeIPStatusChoices,
        required=False
    )

    tag = TagFilterField(model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate city choices dynamically
        self.fields['city'].choices = [(c, c) for c in GeoIP.objects.values_list('city', flat=True).distinct() if c]
        self.fields['city'].choices.insert(0, ("", "---------"))  # Add empty choice for 'Any'


class CustomPrefixForm(PrefixForm):
    """@property
    def selector_fields(self):
        return super().selector_fields + ('cf_country',)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "cf_region" in self.fields:
            self.fields["cf_region"].query_params = {'country': '$cf_country'}
            self.fields["cf_region"].widget.attrs['data-dynamic-params'] = '[{"fieldName":"cf_country", "queryParam":"country"}]'

    def clean(self):
        cleaned_data = super().clean() or {}
        cf_data = getattr(self.instance, "custom_field_data", {}) or {}
        geoip_feed = cleaned_data.get("cf_geoip_feed", cf_data.get("geoip_feed"))
        country    = cleaned_data.get("cf_country",    cf_data.get("country"))
        region     = cleaned_data.get("cf_region",     cf_data.get("region"))

        if geoip_feed:
            if not country:
                self.add_error("cf_country", "Country is required when GeoIP is enabled.")
            if not region:
                self.add_error("cf_region", "Region is required when GeoIP is enabled.")


class CustomBulkPrefixForm(PrefixBulkEditForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "cf_region" in self.fields:
            self.fields["cf_region"].query_params = {'country': '$cf_country'}
            self.fields["cf_region"].widget.attrs['data-dynamic-params'] = '[{"fieldName":"cf_country", "queryParam":"country"}]'


class CustomIPAddressForm(IPAddressForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "cf_region" in self.fields:
            self.fields["cf_region"].query_params = {'country': '$cf_country'}
            self.fields["cf_region"].widget.attrs['data-dynamic-params'] = '[{"fieldName":"cf_country", "queryParam":"country"}]'

    def clean(self):
        cleaned_data = super().clean() or {}
        cf_data = getattr(self.instance, "custom_field_data", {}) or {}
        geoip_feed = cleaned_data.get("cf_geoip_feed", cf_data.get("geoip_feed"))
        country    = cleaned_data.get("cf_country",    cf_data.get("country"))
        region     = cleaned_data.get("cf_region",     cf_data.get("region"))

        if geoip_feed:
            if not country:
                self.add_error("cf_country", "Country is required when GeoIP is enabled.")
            if not region:
                self.add_error("cf_region", "Region is required when GeoIP is enabled.")


class CustomBulkIPAddressForm(IPAddressBulkEditForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "cf_region" in self.fields:
            self.fields["cf_region"].query_params = {'country': '$cf_country'}
            self.fields["cf_region"].widget.attrs['data-dynamic-params'] = '[{"fieldName":"cf_country", "queryParam":"country"}]'
