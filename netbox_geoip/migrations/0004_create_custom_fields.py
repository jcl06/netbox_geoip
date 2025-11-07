from django.db import migrations


def noop(*args, **kwargs):
    # This migration used to create NetBox custom fields for Prefix/IPAddress.
    # It is now intentionally a no-op to avoid installing CFs on new setups.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_geoip", "0003_load_region_data"),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]
