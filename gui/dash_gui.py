# -*- coding: utf-8 -*-
import csv
import datetime
import os
import socket
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    'background': '#FFFFFF',
    'text': '#A9A9A9'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='RFQ Morgan Stanley ',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Request for Quote Morgan Stanley powered by the Strats', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(dcc.Dropdown(
        id='dropdownYear',
        options=[
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'},
        ],
        value='2018'
    ), style={'width': '10%', 'justify-content': 'left'}),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter the year for the RFQ to run'),

    dcc.Graph(id='pnl_graph'),
    dcc.Interval(
        id='interval-component',
        interval=200,  # in milliseconds
        n_intervals=0
    )
])


# noinspection PyUnusedLocal
@app.callback(
    Output('pnl_graph', 'figure'),
    [Input('dropdownYear', 'value'), Input('interval-component', 'n_intervals'), Input('button', 'n_clicks')], )
def update_graph(value, n, n_clicks):
    global initialised
    if not initialised:
        read_clients_and_create_dataframe(value)
        initialised = True
    parse_data_socket()

    trace = []
    for el in pnl_data.columns:
        trace.append(go.Scatter(x=pnl_data.index, y=pnl_data[el], name=el))
    return {
        'data': trace,
        'layout': {
            'title': 'PnL over time RFQ MS',
        }
    }


def run_simulation(value):
    os.system("python " + os.getcwd() + "/main.py " + value)


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('dropdownYear', 'value')])
def running_rfq(n_clicks, value):
    if n_clicks == 0 or not n_clicks:
        return "RFQ is not running"
    else:
        sim_thread = threading.Thread(target=run_simulation, args=(value,), daemon=True)
        sim_thread.start()
        return 'RFQ launched for {}'.format(value)


# read the list of the clietns in the answer folder and create the initial dataframe
def read_clients_and_create_dataframe(value):
    global pnl_data
    date_jan = datetime.date(year=int(value), month=1, day=1).isoformat()
    data = {}
    directory_answers = os.getcwd() + "/answers"
    for file in os.listdir(directory_answers):
        if file.endswith(".py"):
            filename = os.fsdecode(file)
            name = filename.split(".")[0]
            data[name] = 0
    if not pnl_data:
        pnl_data = pd.DataFrame(data, index=[date_jan])


def parse_data_csv(pnl_table_inner):
    # read csv + plot
    with open(os.getcwd() + '/logs/PnlEvent.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for eventPnl in csv_reader:
            date = datetime.datetime.strptime(eventPnl[0], '%Y%m%d').date()
            if date.isoformat() not in pnl_table_inner.index:
                data = pnl_table_inner.loc[pnl_table_inner.index[-1]]
                pnl_table_inner.loc[date.isoformat()] = data
            pnl_table_inner.at[date.isoformat(), eventPnl[2]] = float(
                pnl_table_inner.at[date.isoformat(), eventPnl[2]]) + float(eventPnl[1])
    return pnl_table_inner


def parse_data_socket():
    global pnl_data
    lock.acquire()
    data_to_process = incoming_data[:]
    incoming_data.clear()
    lock.release()
    for element in data_to_process:
        event_pnl = element.split(",")
        date = datetime.datetime.strptime(event_pnl[0], '%Y%m%d').date()
        if date.isoformat() not in pnl_data.index:
            data = pnl_data.loc[pnl_data.index[-1]]
            pnl_data.loc[date.isoformat()] = data
        pnl_data.at[date.isoformat(), event_pnl[2]] = float(
            pnl_data.at[date.isoformat(), event_pnl[2]]) + float(event_pnl[1])


def server_socket():
    client_socket, address = s.accept()
    print(f'Connection from {address} has been established. Sending warm up message')
    client_socket.send(bytes('Hello world!', 'utf-8'))
    print('Waiting for data...')

    full_msg = ''
    new_msg = True
    msg_len = 0
    while True:
        msg = client_socket.recv(1024)
        if new_msg:
            msg_len = max(int(msg[:HEADER_SIZE]), 0)
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADER_SIZE >= msg_len:
            lock.acquire()
            incoming_data.append(full_msg[HEADER_SIZE:])
            lock.release()
            new_msg = True
            full_msg = ''


if __name__ == '__main__':
    incoming_data = []

    HEADER_SIZE = 10
    HOST, PORT = 'localhost', 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)

    lock = threading.Lock()

    socket_thread = threading.Thread(target=server_socket, daemon=True)
    socket_thread.start()
    initialised = False
    pnl_data = None
    app.run_server(debug=False)
