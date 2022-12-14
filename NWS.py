from noaa_sdk import NOAA
from FindZip import find_zip

noaa = NOAA()


def forecast(location):
    if ',' in location:
        zip = find_zip(location)
    else:
        zip = location
    try:
        forecast_result = noaa.get_forecasts(str(zip), 'US')
    except Exception as e:
        return 'API could not retrieve data. Wait a few minutes and retry.'
    forecast = {}
    for forecast_row in forecast_result:
        date = forecast_row['startTime'][:10]
        hour = int(forecast_row['startTime'][11:13])
        temperature = forecast_row['temperature']
        wind_speed = forecast_row['windSpeed'].split(' ')[0]
        wind_dir = forecast_row['windDirection']
        weather = forecast_row['shortForecast']
        forecast_dict = {'temperature': temperature, 'windSpeed': wind_speed, 'windDirection': wind_dir,
                         'shortForecast': weather}
        if date not in forecast:
            forecast[date] = {}
        if hour == 7:
            forecast[date]['7AM'] = forecast_dict
        elif hour == 12:
            forecast[date]['12PM'] = forecast_dict
        elif hour == 16:
            forecast[date]['4PM'] = forecast_dict
        elif hour == 21:
            forecast[date]['9PM'] = forecast_dict
    return forecast


def multi_city_forecasts(location_list: list):
    forecasts = {}
    for location in location_list:
        forecasts[location] = forecast(location)
    return forecasts


if __name__ == '__main__':
    locations = ['Lindale, TX', 'Boston, MA', 'Amarillo, TX']
    forecasts = multi_city_forecasts(locations)
    print()
