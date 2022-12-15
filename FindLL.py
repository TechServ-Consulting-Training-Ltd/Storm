from geopy.geocoders import Nominatim


def find_lat_lon(location: str):
    app = Nominatim(user_agent="weather")
    location_raw = app.geocode(location).raw
    return float(location_raw['lat']), float(location_raw['lon'])
