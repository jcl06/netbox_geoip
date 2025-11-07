from netbox.api.routers import NetBoxRouter
from .views import CountryViewSet, RegionViewSet, GeoIPViewSet

router = NetBoxRouter()
router.register("countries", CountryViewSet)
router.register("regions", RegionViewSet)
router.register("", GeoIPViewSet)

#router.register("", GeoIPViewSet, basename='geoip-list')

urlpatterns = router.urls
