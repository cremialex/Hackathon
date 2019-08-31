# -*- coding: utf-8 -*-
import os

import dash
import pandas as pd
import datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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

##create dataframe that plot of each date the PnL
    #header date, name each team,
    # 2018.08.01 -20
    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'title': 'Analytics for the PnL over time',
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(id='pnl_graph'),

])



@app.callback(
    dash.dependencies.Output('pnl_graph', 'figure'),
    [dash.dependencies.Input('dropdownYear', 'value')],)
def update_graph(value):

    pnl_table= read_clients_and_create_dataframe(value)
    print(pnl_table)
    trace=[]
    for el in pnl_table.columns:
        trace.append(go.Scatter(x=pnl_table.index, y=pnl_table[el], name=el))
    return {
        'data': trace,
        'layout': {
            'title': 'PnL over time RFQ MS',
            }
    }




@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('dropdownYear', 'value')])
def running_rfq(n_clicks, value):
    if n_clicks == 0 or not n_clicks:
        return "RFQ is not running"
    else:
        os.system("gnome-terminal --working-directory=" + os.getcwd() + "/../ -- bash -c 'python3 main.py " +
                  value + "; exec bash'")
        return 'RFQ launched for {}'.format(value)

#read the list of the clietns in the answer folder and create the initial dataframe
def read_clients_and_create_dataframe(value):
    dateJan= datetime.date(year=int(value), month=1, day=1).isoformat()
    data = {}
    directory_answers = os.getcwd() + "/../answers"
    for file in os.listdir(directory_answers):
        if file.endswith(".py"):
            filename = os.fsdecode(file)
            name = filename.split(".")[0]
            data[name]= 0

    pnl_table = pd.DataFrame(data, index=[dateJan])
    #test to see the chart
    i=1
    data2 = {}
    dateJan2 = datetime.date(year=int(value), month=1, day=2).isoformat()
    for file in os.listdir(directory_answers):
        if file.endswith(".py"):
            filename = os.fsdecode(file)
            name = filename.split(".")[0]
            data2[name]= 1+ i
            i=i+1
    print(data2)
    print(pnl_table)
    pnl_table.loc[dateJan2] = data2
    #pnl_table.append(pd.Series(data2,index=dateJan2))
    print(pnl_table)
    print("hitting loop")
    return pnl_table

if __name__ == '__main__':
    app.run_server(debug=True)
