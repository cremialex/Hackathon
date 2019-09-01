import socket

if __name__ == "__main__":
    HEADER_SIZE = 10
    HOST, PORT = socket.gethostname(), 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(2)

    full_msg = ''
    new_msg = True
    msg_len = 0

    client_socket, address = s.accept()
    print(f'Connection from {address} has been established. Sending warm up message')
    client_socket.send(bytes('Hello world!', 'utf-8'))
    print('Waiting for data...')
    while True:
        msg = client_socket.recv(1024)
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADER_SIZE == msg_len:
            print(full_msg[HEADER_SIZE:])
            new_msg = True
            full_msg = ''

hello