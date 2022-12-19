import json
from noaa_sdk import NOAA
from FindZip import find_zip
from FindLL import find_lat_lon
from ParseDate import parse_date, parse_hour, parse_date_hour, parse_time
from datetime import date, timedelta
from requests import get
from GetResponse import get_response

noaa = NOAA()
today = date.today()


def get_zones():
    url = f'https://api.weather.gov/zones/land'
    zones_raw = get_response(url)
    zones_dict = {}
    for zone in zones_raw:
        cwa = zone['properties']['cwa']
        offices = [x.split('/')[-1] for x in zone['properties']['forecastOffices']]
        state = zone['properties']['state']
        name = zone['properties']['name']
        id = zone['properties']['id']
        stations = [x.split('/')[-1] for x in zone['properties']['observationStations']]
        if state not in zones_dict:
            zones_dict[state] = {}
        zones_dict[state][name] = {'id': id, 'cwa': cwa, 'offices': offices, 'stations': stations}
    return zones_dict


def get_stations():
    url = f'https://api.weather.gov/stations'
    stations_raw = get_response(url)
    stations_dict = {}
    for station in stations_raw:
        elevation_ft = int(station['properties']['elevation']['value'] * 3.28084)
        zone = station['properties']['forecast'].split('/')[-1]
        name = station['properties']['name']
        id = station['properties']['stationIdentifier']
        latitude = station['geometry']['coordinates'][1]
        longitude = station['geometry']['coordinates'][0]
        stations_dict[name] = {'id': id, 'zone': zone, 'elevation_ft': elevation_ft, 'latitude': latitude,
                               'longitude': longitude}
    return stations_dict


def alerts(location: str):
    try:
        lat, lon = find_lat_lon(location)
    except Exception as e:
        return e
    url = f'https://api.weather.gov/alerts/active?point={lat},{lon}'
    response = get_response(url)
    alerts_raw = json.loads(' '.join(response.text.split()).replace('{ ', '{').replace('} ', '}'))
    alerts_features = alerts_raw['features']
    if len(alerts_features) != 0:
        alerts_cleaned = [
            {'event': x['properties']['event'], 'headline': x['properties']['headline'],
             'description': x['properties']['description'], 'start': x['properties']['onset'],
             'end': x['properties']['ends']} for x in alerts_features]
    else:
        alerts_cleaned = []
    return alerts_cleaned


def forecast_detailed(location):
    lat, lon = find_lat_lon(location)
    if lat == None:
        return f'Failed to locate {location}'
    try:
        forecast_detailed = noaa.points_forecast(lat, lon, type='forecastGridData')
    except Exception as e:
        return e

    forecast_dict = {}
    for n1 in range(8):
        d = str(today + timedelta(days=n1))
        forecast_dict[d] = {}
        for n2 in range(24):
            forecast_dict[d][n2] = {}
    for property in forecast_detailed['properties']:
        if 'values' in forecast_detailed['properties'][property]:
            for row in forecast_detailed['properties'][property]['values']:
                date = parse_date(row['validTime'])
                hour = parse_hour(row['validTime'])
                time = parse_time(row['validTime'])
                value_raw = row['value']
                if date in forecast_dict:
                    if property == 'weather':
                        for prop, val in forecast_detailed['properties']['weather']['values']:
                            forecast_dict[date][hour][prop] = val
                    elif property in ['temperature', 'dewpoint', 'minTemperature', 'apparentTemperature', 'heatIndex',
                                      'windChill', 'maxTemperature']:
                        if value_raw != None:
                            forecast_dict[date][hour][property] = float(value_raw) * 1.8 + 32
                    else:
                        forecast_dict[date][hour][property] = value_raw
    return forecast_dict


def forecast(location):
    if ',' in location:
        zip = find_zip(location)
        if len(zip) != 5:
            return zip
    else:
        zip = location
    try:
        forecast_result = noaa.get_forecasts(str(zip), 'US')
    except Exception as e:
        return e

    forecast_dict = {}
    for n1 in range(8):
        d = str(today + timedelta(days=n1))
        forecast_dict[d] = {}
        for n2 in range(24):
            forecast_dict[d][n2] = {}
    for forecast_row in forecast_result:
        date, hour = parse_date_hour(forecast_row['startTime'])
        temperature = forecast_row['temperature']
        wind_speed = forecast_row['windSpeed'].split(' ')[0]
        wind_dir = forecast_row['windDirection']
        weather = forecast_row['shortForecast']
        values = {'temperature': temperature, 'windSpeed': wind_speed, 'windDirection': wind_dir,
                  'shortForecast': weather}
        if date in forecast_dict:
            forecast_dict[date][hour] = values

    return forecast_dict


def multi_city_forecasts(location_list: list, type: str = 'standard'):
    forecasts = {}
    for location in location_list:
        if type == 'detailed':
            forecasts[location] = forecast_detailed(location)
        elif type == 'standard':
            forecasts[location] = forecast(location)
        elif type == 'alerts':
            forecasts[location] = alerts(location)
    return forecasts


if __name__ == '__main__':
    locations = ['Lindale, TX', 'Dallas, TX', 'Norman, OK']
    # forecasts = multi_city_forecasts(locations, 'standard')
    # detailed = multi_city_forecasts(locations, 'detailed')
    # alerts = multi_city_forecasts(locations, 'alerts')
    # zones = get_zones()
    # stations = get_stations()
    print()
