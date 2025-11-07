from django.db import migrations
from django.conf import settings
import os

def update_ipam_urls(apps):
    file_path = os.path.join(settings.BASE_DIR, "ipam/urls.py")
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    print(f'  Updating {file_path}')
    updated_content = []
    import_added = False
    custom_prefix_add_added = False
    custom_prefix_edit_added = False
    custom_prefix_bulk_edit_added = False
    custom_ipaddress_add_added = False
    custom_ipaddress_edit_added = False
    custom_ipaddress_bulk_edit_added = False
    for line in content:
        # Check if import already exists
        if "from netbox_geoip import views as netbox_geoip_views" in line:
            import_added = True
        # Check if CustomPrefixAddView is already in the file
        if "netbox_geoip_views.CustomPrefixAddView.as_view()" in line:
            custom_prefix_add_added = True
        # Check if CustomPrefixEditView is already in the file
        if "netbox_geoip_views.CustomPrefixEditView.as_view()" in line:
            custom_prefix_edit_added = True
        if "netbox_geoip_views.CustomPrefixBulkEditView.as_view()" in line:
            custom_prefix_bulk_edit_added = True
        # Check if CustomIPAddressAddView is already in the file
        if "netbox_geoip_views.CustomIPAddressAddView.as_view()" in line:
            custom_ipaddress_add_added = True
        # Check if CustomIPAddressEditView is already in the file
        if "netbox_geoip_views.CustomIPAddressEditView.as_view()" in line:
            custom_ipaddress_edit_added = True
        if "netbox_geoip_views.CustomIPAddressBulkEditView.as_view()" in line:
            custom_ipaddress_bulk_edit_added = True
        updated_content.append(line)
    if not import_added:
        updated_content.insert(0, "from netbox_geoip import views as netbox_geoip_views\n")
        print('  Added import in Line 1: from netbox_geoip import views as netbox_geoip_views')
    if not custom_prefix_bulk_edit_added:
        for i, line in enumerate(updated_content):
            if "path('prefixes/edit/'" in line:
                updated_content[i] = "    # " + line.strip() + "\n"
                print(f"  Changed Line {i}:\n  From: {line.strip()}\n  To: {updated_content[i].strip()}")
                updated_content.insert(i + 1,
                                       "    path('prefixes/edit/', netbox_geoip_views.CustomPrefixBulkEditView.as_view(), name='prefix_bulk_edit'),\n")
                print(f"  Added in Line {i + 1}:\n  {updated_content[i + 1].strip()}")
                break
    if not custom_prefix_add_added:
        for i, line in enumerate(updated_content):
            if "path('prefixes/add/'" in line:
                updated_content[i] = "    # " + line.strip() + "\n"
                print(f"  Changed Line {i}:\n  From: {line.strip()}\n  To: {updated_content[i].strip()}")
                updated_content.insert(i + 1,
                                       "    path('prefixes/add/', netbox_geoip_views.CustomPrefixAddView.as_view(), name='prefix_add'),\n")
                print(f"  Added in Line {i + 1}:\n  {updated_content[i + 1].strip()}")
                break
    # Insert custom prefix edit path before 'prefixes/<int:pk>/'
    if not custom_prefix_edit_added:
        for i, line in enumerate(updated_content):
            if "path('prefixes/<int:pk>/', include(get_model_urls('ipam', 'prefix')))" in line:
                updated_content.insert(i,
                                       "    path('prefixes/<int:pk>/edit/', netbox_geoip_views.CustomPrefixEditView.as_view(), name='prefix_edit'),\n")
                print(f"  Added in Line {i}:\n  {updated_content[i].strip()}")
                break
    if not custom_ipaddress_bulk_edit_added:
        for i, line in enumerate(updated_content):
            if "path('ip-addresses/edit/'" in line:
                updated_content[i] = "    # " + line.strip() + "\n"
                print(f"  Changed Line {i}:\n  From: {line.strip()}\n  To: {updated_content[i].strip()}")
                updated_content.insert(i + 1,
                                       "    path('ip-addresses/edit/', netbox_geoip_views.CustomIPAddressBulkEditView.as_view(), name='ipaddress_bulk_edit'),\n")
                print(f"  Added in Line {i + 1}:\n  {updated_content[i + 1].strip()}")
                break
    if not custom_ipaddress_add_added:
        for i, line in enumerate(updated_content):
            if "path('ip-addresses/add/'" in line:
                updated_content[i] = "    # " + line.strip() + "\n"
                print(f"  Changed Line {i}:\n  From: {line.strip()}\n  To: {updated_content[i].strip()}")
                updated_content.insert(i + 1,
                                       "    path('ip-addresses/add/', netbox_geoip_views.CustomIPAddressAddView.as_view(), name='ipaddress_add'),\n")
                print(f"  Added in Line {i + 1}:\n  {updated_content[i + 1].strip()}")
                break
    # Insert custom prefix edit path before 'prefixes/<int:pk>/'
    if not custom_ipaddress_edit_added:
        for i, line in enumerate(updated_content):
            if "path('ip-addresses/<int:pk>/', include(get_model_urls('ipam', 'ipaddress')))" in line:
                updated_content.insert(i,
                                       "    path('ip-addresses/<int:pk>/edit/', netbox_geoip_views.CustomIPAddressEditView.as_view(), name='ipaddress_edit'),\n")
                print(f"  Added in Line {i}:\n  {updated_content[i].strip()}")
                break
    # Write back the modified content only if changes were made
    if (not import_added or not custom_prefix_add_added or
            not custom_prefix_bulk_edit_added or
            not custom_ipaddress_add_added or
            not custom_ipaddress_bulk_edit_added or
            not custom_prefix_edit_added or
            not custom_ipaddress_edit_added):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_content)


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_geoip", "0004_create_custom_fields"),
    ]

    operations = [
        migrations.RunPython(update_ipam_urls),
    ]
