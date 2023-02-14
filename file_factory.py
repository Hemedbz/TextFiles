import json, csv
import os.path
from csv_file import CsvFile
from json_file import JsonFile
from txt_file import TxtFile
from exceptions import *


class FileFactory:

    @staticmethod
    def open_file(filetype: str, path: str, header: bool = True, delimiter: str = ',') -> CsvFile | \
                                                                                                TxtFile | JsonFile:
        """
        The function receives a file path, file type, and variables required for each file type,
        and returns an instance of that file. If the file type is not one of the three specified -> txt, csv, json,
        it will not be possible to use the library.
        :param filetype: str (csv/json/txt).
        :param path: str, file path.
        :param header: bool, in csv -> if is there a header.
        :param delimiter: Character or sequence of characters that separate columns.
        :return: instance of CsvFile | TxtFile | JsonFile
        """
        max_size: int = 50
        size = os.path.getsize(path)

        # checks if the file is smaller than the max size
        if size <= max_size:
            if filetype == 'csv':
                return CsvFile(path, delimiter, header)
            elif filetype == 'txt':
                return TxtFile(path)
            elif filetype == 'json':
                return JsonFile(path)
            else:
                raise InvalidTypeError()

        else:
            raise InvalidTypeError()

    @staticmethod
    def create_file(filetype: str, path: str, header: list=None) -> CsvFile | TxtFile | JsonFile:
        """
        Creates new file. The function receives a string representing the file type,
        creates the new file, and returns an instance of the class corresponding to that file.
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
            raise InvalidTypeError()


