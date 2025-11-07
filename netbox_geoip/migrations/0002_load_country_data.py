import os
import csv
from django.db import migrations


def load_countries(apps, schema_editor):
    Country = apps.get_model("netbox_geoip", "Country")
    csv_path = os.path.join(os.path.dirname(__file__), "../data/countries.csv")

    if not os.path.exists(csv_path):
        raise Exception(f"File not found: {csv_path}")

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            Country.objects.get_or_create(
                id=int(row["id"]),
                defaults={"country_code": row["country_code"], "name": row["name"]}
            )

            count += 1
    print(f"Loaded {count} countries")


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_geoip", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_countries),
    ]
