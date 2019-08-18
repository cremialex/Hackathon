# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import subprocess
import os
import runner.runner as run

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

    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter the year for the RFQ to run'),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'title': 'Dash Data Visualization',
                'font': {
                    'color': colors['text']
                }
            }
        }
    )


])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def runningRFQ(n_clicks, value):
    if not value :
        return "RFQ is not running"
    else:
        os.system("gnome-terminal -- bash -c 'python3 '"+os.getcwd()+"'/../main.py "+value+"; exec bash'")
        return 'RFQ launched for {}'.format(
        value)

if __name__ == '__main__':
    app.run_server(debug=True)


