# -*- coding: utf-8 -*-
import os

import dash
import pandas as pd
import datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import csv
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




pnl_table= pd.DataFrame()



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
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
])



@app.callback(
    Output('pnl_graph', 'figure'),
    [Input('dropdownYear', 'value'), Input('interval-component', 'n_intervals'), Input('button', 'n_clicks')],)
def update_graph(value, n, n_clicks):
    if n_clicks == 0 or not n_clicks:
        pnl_table= read_clients_and_create_dataframe(value)
    else:
        pnl_table = read_clients_and_create_dataframe(value)
        pnl_table= parseDataCSV(pnl_table)


    trace=[]
    for el in pnl_table.columns:
        trace.append(go.Scatter(x=pnl_table.index, y=pnl_table[el], name=el))
    return {
        'data': trace,
        'layout': {
            'title': 'PnL over time RFQ MS',
                }
        }


def test(value):
    os.system("python " + os.getcwd() + "/main.py " + value)


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('dropdownYear', 'value')])
def running_rfq(n_clicks, value):
    if n_clicks == 0 or not n_clicks:
        return "RFQ is not running"
    else:
        x = threading.Thread(target=test,args=(value,), daemon=True)
        x.start()
        #os.system("python " + os.getcwd() + "/main.py " + value)
        return 'RFQ launched for {}'.format(value)

#read the list of the clietns in the answer folder and create the initial dataframe
def read_clients_and_create_dataframe(value):
    dateJan= datetime.date(year=int(value), month=1, day=1).isoformat()
    data = {}
    directory_answers = os.getcwd() + "/answers"
    for file in os.listdir(directory_answers):
        if file.endswith(".py"):
            filename = os.fsdecode(file)
            name = filename.split(".")[0]
            data[name]= 0

    pnl_table = pd.DataFrame(data, index=[dateJan])
    return pnl_table

def parseDataCSV(pnl_table):
    # #read csv + plot
    with open(os.getcwd() + '/logs/PnlEvent.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for eventPnl in csv_reader:
            date= datetime.datetime.strptime(eventPnl[0], '%Y%m%d').date()
            if date.isoformat() not in pnl_table.index:
                data= pnl_table.loc[pnl_table.index[-1]]
                pnl_table.loc[date.isoformat()]=data
                #pnl_table.iloc[-1]=#add new date in PnL
            pnl_table.at[date.isoformat(), eventPnl[2]] = float(pnl_table.at[date.isoformat(), eventPnl[2]]) + float(eventPnl[1])
    return pnl_table

def parseDataSocket(pnl_table):
    for eventPnl in PnL_DATA[:]:
        date= datetime.datetime.strptime(eventPnl[0], '%Y%m%d').date()
        if date.isoformat() not in pnl_table.index:
            data= pnl_table.loc[pnl_table.index[-1]]
            pnl_table.loc[date.isoformat()]=data
            #pnl_table.iloc[-1]=#add new date in PnL
        pnl_table.at[date.isoformat(), eventPnl[2]] = float(pnl_table.at[date.isoformat(), eventPnl[2]]) + float(eventPnl[1])

    return pnl_table

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
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADER_SIZE == msg_len:
            print(full_msg[HEADER_SIZE:])
            PnL_DATA.append(full_msg[HEADER_SIZE:])
            new_msg = True
            full_msg = ''


import socket
import threading
if __name__ == '__main__':
    PnL_DATA = []

    HEADER_SIZE = 10
    HOST, PORT = socket.gethostname(), 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)

    x = threading.Thread(target=server_socket, daemon=True)
    x.start()
    app.run_server(debug=False)
