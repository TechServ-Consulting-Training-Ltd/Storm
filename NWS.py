from noaa_sdk import NOAA
from FindZip import find_zip
from FindLL import find_lat_lon
from ParseDate import parse_date, parse_hour, parse_date_hour, parse_time
from datetime import date, timedelta

noaa = NOAA()
today = date.today()


def forecast_detailed(location):
    lat, lon = find_lat_lon(location)
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


def multi_city_forecasts(location_list: list, detailed=False):
    forecasts = {}
    for location in location_list:
        if detailed == True:
            forecasts[location] = forecast_detailed(location)
        else:
            forecasts[location] = forecast(location)
    return forecasts


if __name__ == '__main__':
    locations = ['Lindale, TX']
    forecasts = multi_city_forecasts(locations)
    detailed = multi_city_forecasts(locations, True)
    print()
