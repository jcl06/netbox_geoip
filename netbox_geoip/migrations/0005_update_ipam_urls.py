from django.db import migrations


def noop(*args, **kwargs):
    # This migration used to patch netbox ipam/urls.py.
    # It is now intentionally a no-op.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_geoip", "0004_create_custom_fields"),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]
