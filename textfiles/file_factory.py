import json, csv
import os.path
from .csv_file import CsvFile
from .json_file import JsonFile
from .txt_file import TxtFile
from .exceptions import *


class TextFile:

    @staticmethod
    def make_file_instance(path: str, filetype: str, has_header: bool = True, delimiter: str = ',', max_size: int = 50)\
            ->\
            CsvFile | TxtFile | JsonFile:
        """
        This functions creates a file class instance for an existing text file.
        If the file type is not one of the three specified -> txt, csv, json,
        it will not be possible to use the library.
        :param filetype: str (csv/json/txt).
        :param path: str, file path.
        :param has_header: bool, applicable for csv files only. Does the file have a header? Default is True.
        :param delimiter: str, applicable for csv files only. Character or sequence of characters that separate columns.
         Default is ','.
        :param max_size: int, max file size in MB that TextFile should allow. Default is 50.
        :return: instance of CsvFile | TxtFile | JsonFile
        """
        max_size = max_size*1000000
        size = os.path.getsize(path)

        # ensures file is within size limits
        if size > max_size:
            raise SizeError()

        # create instance
        if filetype == 'csv':
            return CsvFile(path, delimiter, has_header)
        elif filetype == 'txt':
            return TxtFile(path)
        elif filetype == 'json':
            return JsonFile(path)

        else:
            raise InvalidTypeError()


    @staticmethod
    def make_file(filetype: str, path: str, header: list = None) -> CsvFile | TxtFile | JsonFile:
        """
        Creates new file in the file path, and a corresponding Python instance of it.
        :param filetype: str, must be 'csv', 'txt' or 'json'
        :param path: str, must be valid clear path
        :param header: list, for csv files only. Provide a list of column headers.
        :return: instance of TxtFIle | JsonFile | CsvFile
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
            raise InvalidTypeError()
