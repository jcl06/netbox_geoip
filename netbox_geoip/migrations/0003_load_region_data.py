import os
import csv
from django.db import migrations

def load_regions(apps, schema_editor):
    Country = apps.get_model("netbox_geoip", "Country")
    Region = apps.get_model("netbox_geoip", "Region")
    csv_path = os.path.join(os.path.dirname(__file__), "../data/regions.csv")

    if not os.path.exists(csv_path):
        raise Exception(f"File not found: {csv_path}")

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            try:
                country = Country.objects.get(id=int(row["country"]))
                Region.objects.get_or_create(
                    country=country,
                    name=row["name"],
                    subdivision_code=row["subdivision_code"]
                )
                count += 1
            except Country.DoesNotExist:
                print(f"Skipping region {row['name']}: Country ID {row['country']} not found")
    countries = Country.objects.all()
    c = 0
    for country in countries:
        region = Region.objects.filter(country=country)
        if not region:
            obj, created = Region.objects.get_or_create(
                country=country,
                name='Not Applicable',
                subdivision_code=''
            )
            if created:
                c += 1
    print(f"Loaded {count} regions, {c} without region")


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_geoip", "0002_load_country_data"),
    ]

    operations = [
        migrations.RunPython(load_regions),
    ]
