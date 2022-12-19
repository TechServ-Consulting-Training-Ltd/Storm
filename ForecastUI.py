import csv
import PySimpleGUI as sg
from AnalyzeForecast import analyze_forecasts
from ParseForecasts import parse_forcasts
from ParseAlerts import parse_alerts


def loc_row(i):
    return [
        [sg.T("City"), sg.InputText(key=("city", i), size=20), sg.T("State"), sg.InputText(key=("state", i), size=3)]]


column_layout = [
    [sg.T("City"), sg.InputText(key="city", size=20), sg.T("State"), sg.InputText(key="state", size=3),
     sg.Button('Add', enable_events=True, key="add")]
]

layout = [
    [sg.T('Locations to obtain forecast for:')],
    [sg.Column(column_layout, key='column')],
    [sg.Button('Run Forecast Report')],
    [sg.Table(key='forecast', values=[],
              headings=['   Location   ', '  Date  ', 'Time', 'Temp', 'Wind', 'A Temp', '      Weather      '],
              size=(80, 10))],
    [sg.Table(key='alerts', values=[],
              headings=['   Location   ', '      Event      ', '     Start     ', '     End     '], size=(100, 5))],
    # [sg.T('Criteria to highlight:')],
    # [sg.T('Min Temp (F)'), sg.InputText(key='min_t', size=3, default_text=32),
    #  sg.T('Max Temp (F)'), sg.InputText(key='max_t', size=3, default_text=90),
    #  sg.T('Min Apparent Temp (F)'), sg.InputText(key='min_at', size=3, default_text=20),
    #  sg.T('Max Apparent Temp (F)'), sg.InputText(key='max_at', size=3, default_text=100)],
    # [sg.T('Max Sustained Wind (mph)'), sg.InputText(key='wind', size=3, default_text=20)],
    # [sg.T('Keywords to search for:')],
    # [sg.Checkbox('Heavy', key='heavy', default=True), sg.Checkbox('Strong', key='strong', default=True),
    #  sg.Checkbox('Hurricane', key='hurricane', default=True),
    #  sg.Checkbox('Tropical Storm', key='trop_storm', default=True)],
    # [sg.Checkbox('Flood', key='flood', default=True), sg.Checkbox('Thunderstorm', key='thunder', default=True),
    #  sg.Checkbox('Severe', key='severe', default=True), sg.Checkbox('Blowing', key='blowing', default=True)],
    # [sg.Checkbox('Rain', key='rain', default=True), sg.Checkbox('Snow', key='snow', default=True), sg.Checkbox(
    #     'Sleet', key='sleet', default=True), sg.Checkbox('Freezing Rain', key='freezing_rain', default=True),
    #  sg.Checkbox('Ice', key='ice', default=True)],
    # [sg.Button('Run Criteria Report')],
    [sg.InputText('Export Location', key='save_as', size=30),
     sg.FileSaveAs('Save As', target='save_as', file_types=(('CSV', 'csv')))],
    [sg.Button('Export')],
    [sg.T('', key='response')]
]

window = sg.Window("Generate Forecasts", layout, element_padding=(6, 5), resizable=True)
i = 1
while True:
    locations = []
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'add':
        window.extend_layout(window['column'], loc_row(i))
        i += 1
    # elif event == 'Run Criteria Report':
    #     window['response'].update('Running Criteria Report')
    #     cities = [values['city']]
    #     states = [values['state']]
    #     keywords = []
    #     for k, v in values.items():
    #         if isinstance(k, tuple):
    #             if k[0] == 'city':
    #                 cities.append(v)
    #             if k[0] == 'state':
    #                 states.append(v)
    #         if v == True:
    #             keywords.append(k)
    #     locations = [f'{x[0]}, {x[1]}' for x in zip(cities, states)]
    #     criteria = {'min_temp': values['min_t'], 'max_temp': values['max_t'],
    #                 'min_atemp': values['min_at'], 'max_atemp': values['max_at'],
    #                 'max_wind': values['wind'], 'keywords': keywords}
    #     result = analyze_forecasts(locations, criteria)
    #     if isinstance(result, str):
    #         window['response'].update(result)
    #         break
    #     window['output'].update(values=result)
    #     window['response'].update('Ran Criteria Report')
    elif event == 'Run Forecast Report':
        window['response'].update('Running Forecast Report')
        cities = [values['city']]
        states = [values['state']]
        for k, v in values.items():
            if isinstance(k, tuple):
                if k[0] == 'city':
                    cities.append(v)
                if k[0] == 'state':
                    states.append(v)
        locations = [f'{x[0]}, {x[1]}' for x in zip(cities, states)]
        forecast = parse_forcasts(locations)
        alerts = parse_alerts(locations)
        if isinstance(forecast, str):
            window['response'].update(forecast)
            break
        window['forecast'].update(values=forecast)
        window['alerts'].update(values=alerts)
        window['response'].update('Ran Forecast Report')
    elif event == 'Export':
        window['response'].update('Exporting to csv')
        try:
            with open(values['save_as'], 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Location', 'Date', 'Time', 'Condition', 'Value'])
                writer.writerows(forecast)
            window['response'].update('Exported to csv')
        except:
            if '.csv' not in values['save_as']:
                window['response'].update('Save as csv')
            else:
                window['response'].update('A report has to be ran first')

event, values = window.read()
window.close()
