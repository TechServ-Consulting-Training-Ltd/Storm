from NWS import multi_city_forecasts
from ParseDate import parse_time


def parse_forcasts(location_list: list, detail: bool = False):
    forecasts = multi_city_forecasts(location_list, detail)
    forecasts_list = []
    for loc, dates in forecasts.items():
        for date, hours in dates.items():
            for hour, time_forc in hours.items():
                time = parse_time(hour)
                if len(time_forc) != 0:
                    if detail == False:
                        temp = time_forc['temperature']
                        wind = time_forc['windSpeed']
                        weather = time_forc['shortForecast']
                        try:
                            forecasts_list.append((loc, date, time, temp, wind, weather))
                        except:
                            forecasts_list.append((loc, dates, time, 'Error', 'Error', 'Error'))
    return forecasts_list


if __name__ == '__main__':
    print(parse_forcasts(['Lindale, TX']))
    print()
