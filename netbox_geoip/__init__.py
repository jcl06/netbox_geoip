from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginConfig
import logging

logger = logging.getLogger(__name__)

__version__ = "1.1"


class GeoIPConfig(PluginConfig):
    name = "netbox_geoip"
    label = "netbox_geoip"
    verbose_name = "NetBox GeoIP"
    description = _("NetBox plugin for Public IP Geolocation")
    version = "1.1"
    author = "Joel Loreno"
    author_email = "jcloreno@gmail.com"
    required_settings = []
    base_url = "netbox-geoip"
    min_version = "4.1.3"
    max_version = "4.9.9"
    default_settings = {
        "menu_name": "GeoIP",
        "top_level_menu": True,
    }

    def ready(self):
        super().ready()

        import netbox_geoip.signals # noqa
        import netbox_geoip.extensions  # noqa

config = GeoIPConfig

