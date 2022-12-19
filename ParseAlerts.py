from NWS import multi_city_forecasts
from ParseDate import parse_time, parse_date_time


def parse_alerts(location_list: list, detail: bool = False):
    alerts = multi_city_forecasts(location_list, 'alerts')
    alerts_list = []
    for k, v in alerts.items():
        for x in v:
            start_date, start_time = parse_date_time(x['start'])
            end_date, end_time = parse_date_time(x['end'])
            start = f'{start_date} {start_time}'
            end = f'{end_date} {end_time}'
            alerts_list.append((k, x['event'], start, end))
    return alerts_list


if __name__ == '__main__':
    alerts = parse_alerts(['Lindale, TX', 'Norman, OK', 'Kansas City, MO'])
    print()
