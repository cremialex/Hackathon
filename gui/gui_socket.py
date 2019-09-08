import socket
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

PNL_DATA = []

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

    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    ),

    html.Div(id='live-update-text')
])


@app.callback(Output('live-update-text', 'children'), [Input('interval-component', 'n_intervals')])
def read_pnl(n):
    if len(pnl_data) > 0:
        lock.acquire()
        res = pnl_data[-1]
        lock.release()
        res = res.split(",")
        return res[1]

    else:
        return 'no data yet'


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
            lock.acquire()
            pnl_data.append(full_msg[HEADER_SIZE:])
            lock.release()
            new_msg = True
            full_msg = ''


if __name__ == '__main__':
    HEADER_SIZE = 10
    HOST, PORT = socket.gethostname(), 9999

    pnl_data = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)

    lock = threading.Lock()

    socket_thread = threading.Thread(target=server_socket, daemon=True)
    socket_thread.start()
    app.run_server(debug=False)
