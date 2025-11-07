from itertools import chain
from ipam.models import IPAddress, Prefix
from django.db.models import F, Value, CharField

# Annotate IP Address queryset
ip_qs = IPAddress.objects.filter(custom_field_data__geoip_feed=True).annotate(
    type=Value("IPAddress", output_field=CharField()),
    country=F('custom_field_data__cf_country'),  # Correct way to pull custom field
    region=F('custom_field_data__cf_region'),  # Correct way to pull custom field
    subdivision_code=Value("Subdivision1", output_field=CharField()),  # Adjust based on actual custom fields
    city=Value("City1", output_field=CharField()),
)

# Annotate Prefix queryset
prefix_qs = Prefix.objects.filter(custom_field_data__geoip_feed=True).annotate(
    type=Value("Prefix", output_field=CharField()),
    country=F('custom_field_data__cf_country'),  # Correct way to pull custom field
    region=F('custom_field_data__cf_region'),  # Correct way to pull custom field
    subdivision_code=Value("Subdivision2", output_field=CharField()),  # Adjust based on actual custom fields
    city=Value("City2", output_field=CharField()),
)

# Combine the querysets in Python using chain (avoids database-level union)
geoip_qs = chain(ip_qs, prefix_qs)

# Now geoip_qs contains both IPAddress and Prefix data, annotated with required fields.
