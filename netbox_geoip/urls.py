from django.urls import include, path
from utilities.urls import get_model_urls
from . import views


app_name = 'netbox_geoip'

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    path('countries/add/', views.CountryCreateView.as_view(), name='country_add'),
    path('countries/import/', views.CountryBulkImportView.as_view(), name='country_import'),
    path('countries/edit/', views.CountryBulkEditView.as_view(), name='country_bulk_edit'),
    path('countries/delete/', views.CountryBulkDeleteView.as_view(), name='country_bulk_delete'),
    path('countries/<int:pk>/', include(get_model_urls('netbox_geoip', 'country'))),

    path('regions/', views.RegionListView.as_view(), name='region_list'),
    path('regions/add/', views.RegionCreateView.as_view(), name='region_add'),
    path('regions/import/', views.RegionBulkImportView.as_view(), name='region_import'),
    path('regions/edit/', views.RegionBulkEditView.as_view(), name='region_bulk_edit'),
    path('regions/delete/', views.RegionBulkDeleteView.as_view(), name='region_bulk_delete'),
    path('regions/<int:pk>/', include(get_model_urls('netbox_geoip', 'region'))),

    path('', views.GeoIPListView.as_view(), name='geoip_list'),
]
