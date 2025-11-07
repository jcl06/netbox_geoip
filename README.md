# NetBox GeoIP Plugin

## Overview
The **NetBox GeoIP Plugin** extends NetBox to store and manage IP Geolocation data, including country, region, subdivision codes, country codes, city, and IP/Network address mappings.

## Features
- Store GeoIP location data with country, region, and city fields.
- Link `subnet` to NetBox's IPAddress and Prefix.
- Use dynamic filtering for `country`, and `region` selections.
- Provide a database of countries and regions for accurate selection.
- Integrate seamlessly with NetBox custom fields for IP Addresses.


## Requirements
* NetBox 4.0.5 or higher
* Python 3.10 or higher


## Installation & Configuration
### NetBox Configuration
Add the plugin to the NetBox config. ~/netbox/configuration.py
   ```python
   PLUGINS = ["netbox_geoip"]
   ```
### Installation
   ```sh
   $ source /opt/netbox/venv/bin/activate
   (venv) $ pip install /path/netbox-geoip
   ```

To add the netbox_geoip tables to NetBox database:
   ```sh
   (venv) $ python manage.py migrate netbox_geoip
   ```


Full documentation on using plugins with NetBox: [Using Plugins - NetBox Documentation](https://netbox.readthedocs.io/en/stable/plugins/)

## Configuration
No additional configuration is required. The plugin will automatically integrate with NetBox. Just ensure the migration is successful.

## Usage
- Navigate to the **GEOIP Locations** section in NetBox to manage locations.
- When adding/editing an IP/Prefix Address, set the **Enable GeoIP** to `True` in the custom fields to add the IP/Prefix Address to GeoIP table.

## Models
### `GeoIP`
Stores GeoIP location data with fields:
- `subnet` (linked to NetBox's IP Address and Prefix)
- `country`
- `country_code`
- `region`
- `subdivision_code`
- `city`

### `Country`
Stores a list of countries and their country codes.

### `Region`
Stores a list of regions and subdivision codes, linked to `GeoIP`.


## Contact
For issues and feature requests, open a GitHub issue.

