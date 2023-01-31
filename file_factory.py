import json, csv
import os.path
from csv_file import CsvFile, LargeCsvFile
from json_file import JsonFile, LargeJsonFile
from txt_file import TxtFile, LargeTxtFile
from exceptions import *


class FileFactory:

    @staticmethod
    def create_file(filetype, path, header: list=None):
        """
        Creates new file
        :param filetype: str (csv/json/txt)
        :param path: str
        :param header: list[headers for csv]
        :return: instance of new file
        """
        if filetype == 'csv':
            with open(path, 'w', newline="") as cv:
                write = csv.DictWriter(cv, fieldnames=header)
                write.writeheader()
                return CsvFile(path)

        elif filetype == 'txt':
            fh = open(path, 'x')
            fh.close()
            return TxtFile(path)

        elif filetype == 'json':
            with open(path, 'w') as js:
                json.dump(js, None)
            return JsonFile(path)

        else:
            raise InvalidTypeError


    @staticmethod
    def create_instance(filetype, path, header=True, delimiter=',', max_size=50):
        size = os.path.getsize(path)

        if size <= max_size: #check if size comes in mb
            if filetype == 'csv':
                return CsvFile(path, delimiter, header)
            elif filetype == 'txt':
                return TxtFile(path)
            elif filetype == 'json':
                return JsonFile(path)
            else:
                raise InvalidTypeError

        else:
            if filetype == 'csv':
                return LargeCsvFile(path, delimiter, header)
            elif filetype == 'txt':
                return LargeTxtFile(path)
            elif filetype == 'json':
                return LargeJsonFile(path)
            else:
                raise InvalidTypeError

