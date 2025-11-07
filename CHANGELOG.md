# 🧭 NetBox GeoIP Plugin — v1.1

## 🚀 New in This Release

- **Removed dependency on NetBox Custom Fields.**  
  GeoIP integration is now handled natively at the form level (no more custom fields for country, region, city, or GeoIP feed).

- **Dynamic GeoIP form integration for Prefix and IPAddress.**  
  New fields (`Enable GeoIP`, `Country`, `Region`, `City`) are automatically injected into NetBox forms — no manual UI changes needed.

- **Automatic GeoIP data sync.**  
  GeoIP records are now created, updated, or deleted automatically when saving a Prefix or IPAddress.

- **Integrated logging and snapshot support.**  
  Changes to GeoIP data now appear in the object’s changelog, maintaining audit traceability.

- **Improved region filtering.**  
  Regions are now dynamically filtered based on the selected country.

- **Code structure improvements.**  
  The plugin now uses a centralized patch mechanism (`patch_form()` and `serialize_object` overrides) instead of manual view overrides.

- **Better compatibility.**  
  Works seamlessly with NetBox 4.1.3+ and Python 3.10+.


---

## ⚠️ Upgrade Notes

If upgrading from **v1.0**:

1. **Remove old custom fields**  
   Delete the following from **Customization → Custom Fields**:
   - `country`
   - `region`
   - `city`
   - `geoip_feed`

2. **Uncomment and remove the following in `ipam/urls.py`:**

    ```diff
    - from netbox_geoip import views as netbox_geoip_views  # remove from the top

    # Prefixes
    ...
    + path('prefixes/add/', views.PrefixEditView.as_view(), name='prefix_add'),
    - # path('prefixes/add/', views.PrefixEditView.as_view(), name='prefix_add'),
    - path('prefixes/add/', netbox_geoip_views.CustomPrefixAddView.as_view(), name='prefix_add'),
    ...
    + path('prefixes/edit/', views.PrefixBulkEditView.as_view(), name='prefix_bulk_edit'),
    - # path('prefixes/edit/', views.PrefixBulkEditView.as_view(), name='prefix_bulk_edit'),
    - path('prefixes/edit/', netbox_geoip_views.CustomPrefixBulkEditView.as_view(), name='prefix_bulk_edit'),
    ...
    - path('prefixes/<int:pk>/edit/', netbox_geoip_views.CustomPrefixEditView.as_view(), name='prefix_edit'),

    # IP addresses
    ...
    + path('ip-addresses/add/', views.IPAddressEditView.as_view(), name='ipaddress_add'),
    - # path('ip-addresses/add/', views.IPAddressEditView.as_view(), name='ipaddress_add'),
    - path('ip-addresses/add/', netbox_geoip_views.CustomIPAddressAddView.as_view(), name='ipaddress_add'),
    ...
    + path('ip-addresses/edit/', views.IPAddressBulkEditView.as_view(), name='ipaddress_bulk_edit'),
    - # path('ip-addresses/edit/', views.IPAddressBulkEditView.as_view(), name='ipaddress_bulk_edit'),
    - path('ip-addresses/edit/', netbox_geoip_views.CustomIPAddressBulkEditView.as_view(), name='ipaddress_bulk_edit'),
    ...
    - path('ip-addresses/<int:pk>/edit/', netbox_geoip_views.CustomIPAddressEditView.as_view(), name='ipaddress_edit'),
    ```


3. **Run plugin migrations:**

    ```bash
    python manage.py migrate netbox_geoip
    ```


---

## 🧩 Version Information

| Version | Date | Highlights |
|----------|------|------------|
| **1.1** | 2025-11-06 | Native form integration, auto GeoIP management, no more custom fields |
| **1.0** | 2025-10-10 | Initial release with Custom Field–based GeoIP integration |

---

## 📬 Feedback & Support

For issues or feature requests, open a GitHub issue or submit a pull request to the repository.
