from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginConfig
import logging

logger = logging.getLogger(__name__)

__version__ = "1.0"


class GeoIPConfig(PluginConfig):
    name = "netbox_geoip"
    label = "netbox_geoip"
    verbose_name = "NetBox GEOIP"
    description = _("NetBox plugin for Public IP Geolocation")
    version = "1.0"
    author = "Joel Loreno"
    author_email = "jcloreno@gmail.com"
    required_settings = []
    base_url = "netbox-geoip"
    min_version = "4.0.5"
    max_version = "4.1.9"
    default_settings = {
        "menu_name": "NETBOX GEOIP",
        "top_level_menu": True,
    }

    def ready(self):
        super().ready()

        import netbox_geoip.signals

config = GeoIPConfig

