import csv
import json
import os.path
from abc import ABC, abstractmethod
import pandas as ps
from text_file_parent import TextFile






# ------------------------- CsvFile --------------------------------------------------
class CsvFile(TextFile):

    def __init__(self, file_path, delimiter=','):
        super().__init__(file_path)
        self._delimiter = delimiter

    def _get_ext(self):
        return 'csv'

    def _get_specific_content(self, fd):
        ret_val = []
        for row in csv.DictReader(fd, delimiter=self._delimiter):
            ret_val.append(row)
        return ret_val

    def _open_csv_file(self):
        with open(self._file_path, "r", newline="") as csvfile:
            # read_file = csv.reader(csvfile)
            read_file = ps.read_csv(csvfile, delimiter=self._delimiter)
        return read_file

    def get_header(self) -> list:
        return list(self._open_csv_file().columns)

    def get_rows_num(self):
        return len(self._open_csv_file()) + 1

        # with open(self._file_path, "r", newline="") as csvfile:
        #     read_file = csv.reader(csvfile)
        # read_file = self._open_csv_file()

    def get_columns_num(self):
        return len(self._open_csv_file().axes[1])

        # with open(self._file_path, "r", newline="") as csvfile:
        #     read_file = csvfile.readline()
        # return len(read_file.split(self._delimiter))

    def get_row(self, row_num):
        with open(self._file_path, "r", newline="") as csvfile:
            read_file = csv.DictReader(csvfile, delimiter=self._delimiter)

            counter = 0
            for item in read_file:
                counter += 1
                if counter == row_num:
                    return item
        raise Exception()

    def get_cell(self, row_num, column_num):
        with open(self._file_path, 'r', newline="") as csvf:
            read_f = csv.reader(csvf, delimiter=self._delimiter)
            csv_list = list(read_f)

            # if the row and column out of range
            if len(csv_list) < row_num - 1 and len(csv_list[0]) < column_num:
                return False

            return csv_list[row_num][column_num - 1]
    @staticmethod
    def _is_equal(h1: list, h2: list):
        count = 0
        for cul in h1:
            for cul2 in h2:
                if cul == cul2:
                    count += 1

        if len(h1) == count:
            return True
        return False


    def _is_header(self, csv_line):
        first_line = "".join(csv_line)
        first_line = "".join(first_line.split(" "))
        first_line = "".join(first_line.split(self._delimiter))
        if first_line.isalpha():
            return True
        return False

    def _get_column_name_by_num(self, r, column_n):
        line = next(r)
        if self._is_header(line):
            header = line[0].split(self._delimiter)
            return header[column_n - 1]
        return column_n

    def get_column(self, column_num: int):
        clu_info = []
        with open(self._file_path, "r", newline="") as csvfile:
            re = csv.reader(csvfile)
            # check if there is a header. if true return name of column else return the column_num
            clu_name = self._get_column_name_by_num(re, column_num)
            clu_info.append(clu_name)
            csvfile.seek(0)

            # if csv file haven't header
            if clu_name == column_num:
                csv_obj = csv.reader(csvfile)
                for item in csv_obj:
                    clu_info.append(item[0].split(self._delimiter)[column_num - 1])
                return clu_info

            csv_obj = csv.DictReader(csvfile, delimiter=self._delimiter)
            for item in csv_obj:
                clu_info.append(item[clu_name])
            return clu_info

    def __add__(self, other):

        if not isinstance(other, CsvFile):
            raise Exception()
        # self.check_type(other)

        header1, header2 = self.get_header(), other.get_header()

        if not self._is_header(header1) and not other._is_header(header2):
            raise Exception()

        if not self._is_equal(header1, header2):
            raise Exception()

        file_path_name = self.get_file_path() + "\\" + self.get_file_name() + "_" + other.get_file_name() + \
                        self.get_file_extension()

        if os.path.exists(file_path_name):
            raise Exception()

        # print(other.get_content())
        # print(self.get_content())

        with open(file_path_name, "w", newline="") as csv_f:
            writer = csv.DictWriter(csv_f, fieldnames=header1)
            writer.writeheader()
        # [{name: bla, age: bla},{name: bla, age: bla}]
            for row in self.get_content():
                writer.writerow(row)
            for row in other.get_content():
                writer.writerow(row)

        return True


# ------------------------- TxtFile --------------------------------------------------
class TxtFile(TextFile):

    def _get_specific_content(self, fd):
        return fd.read()

    def _get_ext(self):
        return 'txt'

    def _txt_file_read(self):
        with open(self._file_path, 'r') as fd:
            return fd.read()
        # return file_read.split()

    def get_words_num(self):
        return len(self._txt_file_read().split())

    def get_avg_word_len(self):
        sum_words_len = 0
        for word in self._txt_file_read().split():
            sum_words_len += len(word)
        return int(sum_words_len / self.get_words_num())

    def __add__(self, other):
        if not isinstance(other, TxtFile):
            raise ValueError("2 values must be TxtFile type")

        file_path_name = self.get_file_path() + "\\" +self.get_file_name() + "_" + other.get_file_name() + \
                         self.get_file_extension()

        if os.path.exists(file_path_name):
            file_name_exists = f"{self.get_file_name()}_{other.get_file_name()}{self.get_file_extension()}"
            raise FileNameExistsEror(file_name_exists)

        with open(file_path_name, 'w') as fh:
            fh.write(self.get_content() + other.get_content())

        return True


# ------------------------- JsonFile --------------------------------------------------
class JsonFile(TextFile):

    def _get_specific_content(self, fd):
        return json.load(fd)

    def _get_ext(self):
        return 'json'

    def _json_file_load(self):
        with open(self._file_path, 'r') as fd:
            json_file_name = json.load(fd)
        return json_file_name

    def is_list(self):
        if type(self._json_file_load()) is list:
            return True
        return False

    def is_object(self):
        if type(self._json_file_load()) is dict:
            return True
        return False


