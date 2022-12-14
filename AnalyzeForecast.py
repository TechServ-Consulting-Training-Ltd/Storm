from NWS import multi_city_forecasts


def analyze_forecasts(location_list: list, criteria: dict):
    forecasts = multi_city_forecasts(location_list)
    highlight_forecasts = []
    for loc, dates in forecasts.items():
        for date, times in dates.items():
            for time, time_forc in times.items():
                for k, v in time_forc.items():
                    if 'temperature' == k:
                        if v < int(criteria['min_temp']):
                            highlight_forecasts.append((loc, date, time, k, v))
                        if v > int(criteria['max_temp']):
                            highlight_forecasts.append((loc, date, time, k, v))
                    if 'windSpeed' == k:
                        if int(v.split(' ')[0].strip()) > int(criteria['max_wind']):
                            highlight_forecasts.append((loc, date, time, k, v))
                    if 'shortForecast' == k:
                        for word in criteria['keywords']:
                            if word.lower() in v.lower():
                                highlight_forecasts.append((loc, date, time, k, v))
    return highlight_forecasts


if __name__ == '__main__':
    a = analyze_forecasts(['Lindale, TX', 'Boston, MA', 'Seattle, WA'],
                          {'min_temp': '32', 'max_temp': '50', 'max_gust': '20', 'weather': 'Severe'})
