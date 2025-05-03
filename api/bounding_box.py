from geopy.geocoders import Nominatim

def get_geoapify_bbox(location_name):

    geolocator = Nominatim(user_agent="tutorial")
    location = geolocator.geocode(location_name).raw

    if location and 'boundingbox' in location:
        bbox = location['boundingbox']  # ['lat_min', 'lat_max', 'lon_min', 'lon_max']

        lat_min = round(float(bbox[0]), 1)
        lat_max = round(float(bbox[1]), 1)
        lon_min = round(float(bbox[2]), 1)
        lon_max = round(float(bbox[3]), 1)

        # Format for Geoapify API
        geoapify_bbox = f"{lon_min},{lat_max},{lon_max},{lat_min}"
        return geoapify_bbox

    return None  # If location not found

if __name__ == "__main__":
    location = "Maharashtra, India"
    bbox = get_geoapify_bbox(location)
    if bbox:
        print(f"Geoapify Bounding Box for {location}: {bbox}")
    else:
        print("Location not found!")
