import os
import threading
import PySimpleGUI as sg
from NWS import multi_city_forecasts


def new_layout(i):
    return [[sg.T("City"), sg.InputText(key=("city", i)), sg.T("State"), sg.InputText(key=("state", i))]]


column_layout = [
    [sg.T("City"), sg.InputText(key="city"), sg.T("State"), sg.InputText(key="state"),
     sg.Button('Add', enable_events=True, key="add")]
]

layout = [
    [sg.Column(column_layout, key='column')],
    [sg.Submit()],
    [sg.Text('', key='run_status')],
    [sg.Multiline('Output', key='output', auto_size_text=True)]
]

window = sg.Window("Generate Forecasts", layout, element_padding=(6, 5))

i = 1
while True:
    locations = []
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'add':
        city = values['city']
        state = values['state']
        locations.append(f'{city}, {state}')
        window.extend_layout(window['column'], new_layout(i))
        i += 1
    elif event == 'Submit':
        locations.append(f'{city}, {state}')
        window['run_status'].update('Generating forecasts')
        result = multi_city_forecasts(locations)
        window['output'].update(result)

event, values = window.read()
window.close()
