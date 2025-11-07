from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.plugins import PluginMenu
from netbox.plugins.utils import get_plugin_config

menu_name = get_plugin_config("netbox_geoip", "menu_name")
top_level_menu = get_plugin_config("netbox_geoip", "top_level_menu")


public_ip = PluginMenuItem(
        link="plugins:netbox_geoip:geoip_list",
        link_text="Public IPs",
        permissions=["netbox_geoip.view_geoip"]
    )

country = PluginMenuItem(
    link="plugins:netbox_geoip:country_list",
    link_text="Countries",
    permissions=["netbox_geoip.view_country"],
    buttons=(
        PluginMenuButton(
            'plugins:netbox_geoip:country_add',
            _('Add'),
            'mdi mdi-plus-thick',
            permissions=["netbox_geoip.add_country"],
        ),
        PluginMenuButton(
            'plugins:netbox_geoip:country_import',
            _('Import'),
            'mdi mdi-upload',
            permissions=["netbox_geoip.add_country"],
        )
    )
)

region = PluginMenuItem(
    link="plugins:netbox_geoip:region_list",
    link_text="Regions",
    permissions=["netbox_geoip.view_region"],
    buttons=(
        PluginMenuButton(
            'plugins:netbox_geoip:region_add',
            _('Add'),
            'mdi mdi-plus-thick',
            permissions=["netbox_geoip.add_region"],
        ),
        PluginMenuButton(
            'plugins:netbox_geoip:region_import',
            _('Import'),
            'mdi mdi-upload',
            permissions=["netbox_geoip.add_region"],
        )
    )
)


if top_level_menu:
    menu = PluginMenu(
        label=menu_name,
        icon_class='mdi mdi-web',
        groups=(
            (
                _("GEOIP Info"),
                (
                    public_ip,
                )

            ),
            (
                _("GEOIP Locations"),
                (
                    country,
                    region,
                )
            ),
        )
    )
else:
    menu_items = (
        public_ip,
        country,
        region,
    )

