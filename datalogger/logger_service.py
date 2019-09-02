import csv
import os
import socket

class LoggerService:
    class __LoggerService:
        def __init__(self):
            self._log_files = {}
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = socket.gethostname()
            self.HEADER_SIZE = 10
            self.port = 9999
            self.sock.connect((self.host, self.port))
            warmup_msg = self.sock.recv(1024)
            warmup_msg = warmup_msg.decode('utf-8')
            print(f'Connection established and received: {warmup_msg}')

        def register_class(self, clazz):

            file_name = 'logs/' + clazz.__name__ + '.csv'
            name = clazz.__name__ + '.csv'

            if file_name and self.file_already_there(name):
                os.remove(file_name)
            self._log_files[clazz] = file_name
            open(file_name, 'w+').close()
            return file_name

        def log_csv(self, obj):
            file_name = self._log_files.get(obj.__class__)
            if not file_name:
                file_name = self.register_class(obj.__class__)
            with open(file_name, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(obj.log())
            csvFile.close()

        def log_sock(self, obj):
            msg = self.convert_tuple(obj.log())
            msg = f'{len(msg):<{self.HEADER_SIZE}}' + msg
            self.sock.send(bytes(msg, 'utf-8'))

        def __del__(self):
            self.sock.close()

        @staticmethod
        def convert_tuple(tup):
            res = ','.join(tup)
            return res

        def file_already_there(self, name):
            directory_logs = os.getcwd() + "/logs"
            for file in os.listdir(directory_logs):
                if file == name:
                    return True
            return False

    instance = None

    def __init__(self):
        if not LoggerService.instance:
            LoggerService.instance = LoggerService.__LoggerService()

    @staticmethod
    def log(obj):
        LoggerService.instance.log_csv(obj)
        LoggerService.instance.log_sock(obj)
