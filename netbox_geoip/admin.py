from django.contrib import admin
from .models import GeoIP

@admin.register(GeoIP)
class GeoIPModelAdmin(admin.ModelAdmin):
    list_display = ('subnet', 'object_id', 'object', 'type', 'country', 'country_code', 'region', 'subdivision_code', 'city', 'status')
