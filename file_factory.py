import json

from csv_file import CsvFile
from json_file import JsonFile
from txt_file import TxtFile
import csv

class FileFactory:

    @staticmethod
    def create(filetype, path, header: list=None):
        match filetype:
            case 'csv':
                with open(path, 'w', newline="") as cv:
                    write = csv.DictWriter(cv, fieldnames=header)
                    write.writeheader()

                return CsvFile(path, header=True)
            case 'txt':
                fh = open(path, 'x')
                fh.close()
                return TxtFile(path)
            case 'json':
                with open(path, 'w') as js:
                    json.dump(js, None)
                return JsonFile(path)


    @staticmethod
    def instance(filetype, path, header=True, delimiter=','):
        match filetype:
            case 'csv':
                return CsvFile(path, delimiter, header)
            case 'txt':
                return TxtFile(path)
            case 'json':
                return JsonFile(path)


if __name__ == '__main__':

    my_file = FileFactory.instance('csv',"D:\\Full_Stack_Python\\Python_Course\\C10\\files", True, delimiter=';')
    print(my_file.content)
