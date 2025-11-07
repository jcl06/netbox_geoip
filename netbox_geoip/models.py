from django.db import models
from netbox.models import NetBoxModel
from ipam.fields import IPNetworkField
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from utilities.choices import ChoiceSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


CONTENT_TYPE_CHOICES = (
    Q(app_label='ipam', model='prefix') |
    Q(app_label='ipam', model='ipaddress')
)

OBJECT_TYPE_CHOICES = (
    ("ipaddress", "IPAddress"),
    ("prefix", "Prefix"),
)


class GoeIPStatusChoices(ChoiceSet):
    key = 'GoeIP.status'

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_DHCP = 'dhcp'
    STATUS_SLAAC = 'slaac'
    STATUS_CONTAINER = 'container'

    CHOICES = [
        (STATUS_ACTIVE, _('Active'), 'blue'),
        (STATUS_RESERVED, _('Reserved'), 'cyan'),
        (STATUS_DEPRECATED, _('Deprecated'), 'red'),
        (STATUS_DHCP, _('DHCP'), 'green'),
        (STATUS_SLAAC, _('SLAAC'), 'purple'),
        (STATUS_CONTAINER, _('Container'), 'gray'),
    ]


class Country(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=100, unique=True, blank=True)
    tags = models.ManyToManyField(
        'extras.Tag',
        blank=True,
        related_name='netbox_geoip_country',  # Change the default reverse accessor
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_geoip:country', args=[self.pk])


class Region(NetBoxModel):
    name = models.CharField(max_length=100)
    subdivision_code = models.CharField(max_length=100, verbose_name="code", blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="netbox_geoip_regions")
    tags = models.ManyToManyField(
        'extras.Tag',
        blank=True,
        related_name='netbox_geoip_region',  # Change the default reverse accessor
    )

    class Meta:
        unique_together = ('country', 'name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_geoip:region', args=[self.pk])


class GeoIP(NetBoxModel):
    subnet = IPNetworkField(
        verbose_name=_("IP/Network Address")
    )
    object_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=CONTENT_TYPE_CHOICES
    )
    object_id = models.PositiveBigIntegerField()
    type = models.CharField(
        choices=OBJECT_TYPE_CHOICES,
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        to='netbox_geoip.Country',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    region = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    subdivision_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=GoeIPStatusChoices,
        default=GoeIPStatusChoices.STATUS_ACTIVE,
        verbose_name=_('status'),
        help_text=_('Operational status of this prefix')
    )

    object = GenericForeignKey('object_type', 'object_id')

    class Meta:
        verbose_name = "NETBOX GEOIP"
        ordering = ['subnet', 'pk']

    def __str__(self):
        return str(self.subnet)

    def save(self, *args, **kwargs):
        self.type = self.object_type.model
        self.status = self.object.status
        self.city = self.object.custom_field_data['city']
        self.country = Country.objects.filter(id=self.object.custom_field_data['country']).first()
        region = Region.objects.filter(id=self.object.custom_field_data['region']).first()
        if region.name == 'Not Applicable':
            self.region = ''
            self.subdivision_code = ''
        else:
            self.region = region.name
            self.subdivision_code = region.subdivision_code
        if self.object_type.model == "ipaddress":
            self.subnet = f'{self.object.address.ip}/32'
        else:
            self.subnet = str(self.object.prefix)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.object.get_absolute_url()

    def get_status_color(self):
        return GoeIPStatusChoices.colors.get(self.status)

    @property
    def country_code(self):
        country_id = self.object.custom_field_data['country']
        obj = None
        if country_id:
            obj = Country.objects.filter(id=country_id).first().country_code
        return obj

