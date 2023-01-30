import json, csv
import os.path
from csv_file import SmallCsvFile, LargeCsvFile
from json_file import SmallJsonFIle, LargeJsonFile
from txt_file import SmallTxtFIle, LargeTxtFile
from exceptions import *


class FileFactory:

    @staticmethod
    def create(filetype, path, header: list=None):
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
                return SmallCsvFile(path)

        elif filetype == 'txt':
            fh = open(path, 'x')
            fh.close()
            return SmallTxtFile(path)

        elif filetype == 'json':
            with open(path, 'w') as js:
                json.dump(js, None)
            return SmallJsonFile(path)

        else:
            raise InvalidTypeError


    @staticmethod
    def instance(filetype, path, header=True, delimiter=',', max_size=50):
        size = os.path.getsize(path)

        if size <= max_size: #check if size comes in mb
            if filetype == 'csv':
                return SmallCsvFile(path, delimiter, header)
            elif filetype == 'txt':
                return SmallTxtFile(path)
            elif filetype == 'json':
                return SmallJsonFile(path)
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




if __name__ == '__main__':

    my_file = FileFactory.instance('csv',"D:\\Full_Stack_Python\\Python_Course\\C10\\files", True, delimiter=';')
    print(my_file.content)

