import importlib
from django import forms
from django.contrib.contenttypes.models import ContentType

from utilities.forms.rendering import FieldSet

from ipam.models import Prefix, IPAddress
from .models import Country, Region, GeoIP
from utilities.forms.fields import DynamicModelChoiceField
from netbox.context import current_request
from core.choices import ObjectChangeActionChoices


def _get_prefix_form_class():
    try:
        mod = importlib.import_module("ipam.forms.model_forms")
        return mod.PrefixForm
    except (ImportError, AttributeError):
        mod = importlib.import_module("ipam.forms")
        return mod.PrefixForm


def _get_ipaddress_form_class():
    try:
        mod = importlib.import_module("ipam.forms.model_forms")
        return mod.IPAddressForm
    except (ImportError, AttributeError):
        mod = importlib.import_module("ipam.forms")
        return mod.IPAddressForm


def _add_new_fieldset(form_cls, *field_names):
    existing = list(getattr(form_cls, "fieldsets", ()))
    geoip_fs = FieldSet(*field_names, name="GeoIP Info")
    existing.append(geoip_fs)
    form_cls.fieldsets = tuple(existing)


def _load_geoip_for(obj):
    """
    Return the GeoIP instance for this object, or None.
    """
    ct = ContentType.objects.get_for_model(obj)
    return GeoIP.objects.filter(object_type=ct, object_id=obj.pk).first()


def _save_geoip_from_form(obj, cleaned_data: dict):
    feed = cleaned_data.get("geoip_feed")
    country = cleaned_data.get("geoip_country")
    region = cleaned_data.get("geoip_region")
    city = cleaned_data.get("geoip_city") or ""

    ct = ContentType.objects.get_for_model(obj)
    existing = GeoIP.objects.filter(object_type=ct, object_id=obj.pk).first()

    if not feed:
        if existing:
            # snapshot parent so changelog shows the change
            if hasattr(obj, "snapshot"):
                obj.snapshot()

            existing.delete()

            # log change against the parent just like NetBox does, but only if we have request
            req = current_request.get()
            if req is not None and hasattr(obj, "to_objectchange"):
                change = obj.to_objectchange(ObjectChangeActionChoices.ACTION_UPDATE)
                change.user = req.user
                change.request_id = req.id
                change.user_name = req.user.username
                change.save()
        return 

    # CASE 2: feed is ON → create or update GeoIP
    geoip, _ = GeoIP.objects.get_or_create(
        object_type=ct,
        object_id=obj.pk,
    )

    # detect object type + subnet
    if isinstance(obj, Prefix):
        geoip.subnet = str(obj.prefix)
        geoip.type = "prefix"
    elif isinstance(obj, IPAddress):
        if obj.address:
            geoip.subnet = f"{obj.address.ip}/32"
        geoip.type = "ipaddress"

    geoip.country = country if country else None

    if region:
        geoip.region = region.name
        geoip.subdivision_code = region.subdivision_code
    else:
        geoip.region = ""
        geoip.subdivision_code = ""

    geoip.city = city

    if hasattr(obj, "status") and obj.status:
        geoip.status = obj.status

    geoip.save()

    req = current_request.get()
    if req is not None and hasattr(obj, "to_objectchange"):
        change = obj.to_objectchange(ObjectChangeActionChoices.ACTION_UPDATE)
        change.user = req.user
        change.request_id = req.id
        change.user_name = req.user.username
        change.save()



def patch_form(form_name):
    if form_name == "IPAddressForm":
        form = _get_ipaddress_form_class()
    else:
        form = _get_prefix_form_class()

    form.base_fields["geoip_feed"] = forms.BooleanField(
        required=False,
        label="Enable GeoIP",
        help_text="Enable Geolocation for this IP/Subnet.",
    )
    form.base_fields["geoip_country"] = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Country",
        help_text="Country to Feed for Geolocation"
    )
    form.base_fields["geoip_region"] = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Region",
        help_text="Region to Feed for Geolocation",
        query_params = {'country': '$geoip_country'},
    )
    form.base_fields["geoip_city"] = forms.CharField(
        required=False,
        label="City",
        help_text="City to Feed for Geolocation"
    )

    _add_new_fieldset(
        form,
        "geoip_feed",
        "geoip_country",
        "geoip_region",
        "geoip_city",
    )

    original_init = form.__init__

    def __init__(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if getattr(self, "instance", None) and self.instance.pk:
            geoip = _load_geoip_for(self.instance)
            if geoip:
                self.fields["geoip_feed"].initial = True
                self.fields["geoip_country"].initial = geoip.country_id
                if geoip.region:
                    region_obj = Region.objects.filter(name=geoip.region, country=geoip.country_id).first()
                    if region_obj:
                        self.fields["geoip_region"].initial = region_obj.pk
                self.fields["geoip_city"].initial = geoip.city

    form.__init__ = __init__

    original_save = form.save

    def save_with_geoip(self, *args, **kwargs):
        obj = original_save(self, *args, **kwargs)
        _save_geoip_from_form(obj, self.cleaned_data)
        return obj

    form.save = save_with_geoip

    orig_clean = form.clean

    def clean(self):
        orig_clean(self)

        feed = self.cleaned_data.get("geoip_feed")
        country = self.cleaned_data.get("geoip_country")
        region = self.cleaned_data.get("geoip_region")

        if feed:
            if not country:
                self.add_error("geoip_country", "Country is required when GeoIP is enabled.")
            if not region:
                self.add_error("geoip_region", "Region is required when GeoIP is enabled.")

        return self.cleaned_data 

    form.clean = clean



# run patches
patch_form("PrefixForm")
patch_form("IPAddressForm")


# --- Prefix ---
_original_prefix_serialize = Prefix.serialize_object

def prefix_serialize_object(self, *args, **kwargs):
    data = _original_prefix_serialize(self, *args, **kwargs)

    ct = ContentType.objects.get_for_model(Prefix)
    geo = GeoIP.objects.filter(object_type=ct, object_id=self.pk).first()

    if geo:
        data["geoip"] = {
            "enable_geoip": True,
            "country": geo.country.name if geo.country else None,
            "region": geo.region,
            "city": geo.city,
            "status": geo.status
        }
    else:
        data['geoip'] = {"enable_geoip": False}

    return data

Prefix.serialize_object = prefix_serialize_object


# --- IPAddress ---
_original_ip_serialize = IPAddress.serialize_object

def ip_serialize_object(self, *args, **kwargs):
    data = _original_ip_serialize(self, *args, **kwargs)

    ct = ContentType.objects.get_for_model(IPAddress)
    geo = GeoIP.objects.filter(object_type=ct, object_id=self.pk).first()

    if geo:
        data["geoip"] = {
            "enable_geoip": True,
            "country": geo.country.name if geo.country else None,
            "region": geo.region,
            "city": geo.city,
            "status": geo.status
        }
    else:
        data['geoip'] = {"enable_geoip": False}

    return data

IPAddress.serialize_object = ip_serialize_object
