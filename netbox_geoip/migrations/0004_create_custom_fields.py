from django.db import migrations


def create_custom_fields(apps, schema_editor):
    CustomField = apps.get_model("extras", "CustomField")
    ContentType = apps.get_model("contenttypes", "ContentType")
    IPAddress = apps.get_model("ipam", "IPAddress")
    Prefix = apps.get_model("ipam", "Prefix")
    Country = apps.get_model("netbox_geoip", "Country")
    Region = apps.get_model("netbox_geoip", "Region")
    comments = 'DO NOT EDIT or DELETE! This has been automatically created by the NetBox GEOIP plugin.'
    custom_fields = [
        {
            "name": "country",
            "label": "Country",
            "type": "object",
            "required": False,
            "weight": 101,
            "group_name": "GeoIP Info",
            "related_object_type": ContentType.objects.get_for_model(Country),
            "description": "Country to Feed for Geolocation",
            "comments": comments,
        },
        {
            "name": "region",
            "label": "Region",
            "type": "object",
            "required": False,
            "weight": 102,
            "group_name": "GeoIP Info",
            "related_object_type": ContentType.objects.get_for_model(Region),
            "description": "Region to Feed for Geolocation",
            "comments": comments,
        },
        {
            "name": "city",
            "label": "City",
            "type": "text",
            "required": False,
            "weight": 103,
            "group_name": "GeoIP Info",
            "description": "City to Feed for Geolocation",
            "related_object_type": None,
            "comments": comments,
        },
        {
            "name": "geoip_feed",
            "label": "Enable GeoIP",
            "type": "boolean",
            "default": False,
            "required": False,
            "weight": 100,
            "group_name": "GeoIP Info",
            "description": "Enable Geolocation for this IP/Subnet",
            "related_object_type": None,
            "comments": comments,
        },
    ]
    for field_data in custom_fields:
        if CustomField.objects.filter(name=field_data["name"]).exists():
            cf = CustomField.objects.filter(name=field_data["name"])[0]
            print(f'  Checking custom field: {field_data["name"]}')
            if cf.group_name != field_data['group_name']:
                raise Exception(f'Custom field {field_data["name"]} conflict with the existing custom field (ID: {cf.id}).')
            if cf.related_object_type != field_data["related_object_type"]:
                raise Exception(f'Custom field {field_data["name"]} conflict with the existing custom field (ID: {cf.id}).')
            if cf.label != field_data["label"]:
                print(f'  Updated custom field "label" from "{cf.label}" to "{field_data["label"]}"')
                cf.label = field_data["label"]
            if cf.type != field_data["type"]:
                print(f'  Updated custom field "type" from "{cf.type}" to "{field_data["type"]}"')
                cf.type = field_data["type"]
            if cf.required != field_data["required"]:
                print(f'  Updated custom field "required" from "{cf.required}" to "{field_data["required"]}"')
                cf.required = field_data["required"]
            if cf.weight != field_data["weight"]:
                print(f'  Updated custom field "weight" from "{cf.weight}" to "{field_data["weight"]}"')
                cf.weight = field_data["weight"]
            if cf.description != field_data["description"]:
                print(f'  Updated custom field "description" from "{cf.description}" to "{field_data["description"]}"')
                cf.description = field_data["description"]
            if cf.comments != field_data["comments"]:
                print(f'  Updated custom field "comments" from "{cf.comments}" to "{field_data["comments"]}"')
                cf.comments = field_data["comments"]
            if list(cf.object_types.all()) != [ContentType.objects.get_for_model(Prefix),
                                               ContentType.objects.get_for_model(IPAddress)]:
                cf.object_types.clear()
                cf.object_types.add(ContentType.objects.get_for_model(IPAddress).id)
                cf.object_types.add(ContentType.objects.get_for_model(Prefix).id)
            cf.save()
        else:
            # If no fields exist, create them
            field, created = CustomField.objects.get_or_create(name=field_data["name"], defaults=field_data)
            field.object_types.add(ContentType.objects.get_for_model(IPAddress).id)
            field.object_types.add(ContentType.objects.get_for_model(Prefix).id)
            print(f'  Created custom field: {field_data["name"]}')



class Migration(migrations.Migration):
    dependencies = [
        ("netbox_geoip", "0003_load_region_data"),
    ]

    operations = [
        migrations.RunPython(create_custom_fields),
    ]
