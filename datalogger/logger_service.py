import csv
import os

class LoggerService:
    class __LoggerService:
        def __init__(self):
            self._log_files = {}

        def register_class(self, clazz):

            file_name = 'logs/' + clazz.__name__ + '.csv'
            if file_name:
                os.remove(file_name)
            self._log_files[clazz] = file_name
            open(file_name, 'w+').close()
            return file_name

        def log(self, obj):
            file_name = self._log_files.get(obj.__class__)
            if not file_name:
                file_name = self.register_class(obj.__class__)
            with open(file_name, 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(obj.log())
            csvFile.close()

    instance = None

    def __init__(self):
        if not LoggerService.instance:
            LoggerService.instance = LoggerService.__LoggerService()

    @staticmethod
    def log(obj):
        LoggerService.instance.log(obj)
