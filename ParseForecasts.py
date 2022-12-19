from NWS import multi_city_forecasts
from ParseDate import parse_time


def parse_forcasts(location_list: list, detail: bool = False):
    forecasts = multi_city_forecasts(location_list, 'standard')
    forecasts_list = []
    for loc, dates in forecasts.items():
        for date, hours in dates.items():
            for hour, time_forc in hours.items():
                time = parse_time(hour)
                if len(time_forc) != 0:
                    if detail == False:
                        T = time_forc['temperature']
                        V = int(time_forc['windSpeed'])
                        if T > 50 or V < 5:
                            aT = T
                        else:
                            aT = int(35.74 + (0.6215*T) - 35.75*(V**0.16) + 0.4275*T*(V**0.16))
                        weather = time_forc['shortForecast']
                        try:
                            forecasts_list.append((loc, date, time, T, V, aT, weather))
                        except:
                            forecasts_list.append((loc, dates, time, 'Error', 'Error', 'Error', 'Error'))
    return forecasts_list


if __name__ == '__main__':
    print(parse_forcasts(['Lindale, TX']))
    print()
