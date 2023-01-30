from text_file_parent import TextFile
import csv, os
from exceptions import *

# Menu for this file:
    # built-in functions
    # public functions - read
    # math functions - write
    # private functions


class CsvFile (TextFile):

    def __init__(self, file_path, delimiter=',', header=True ):
        """

        :param file_path:
        :param delimiter: default ","
        :param header: bool -> does file have header
        """
        super().__init__(file_path)
        self._isheader = header
        self._delimiter = delimiter
        self._ext = 'csv'

    def __str__(self):
        return f"{self.file_name}\n" \
               f"contains {len(self)} rows\n" \
               f"header: {self.header}\n" \
               f"file creation time: {self.creation_time}\n" \
               f"file last modified: {self.last_modified}"

    def __contains__(self, item):
        for row in self._content:
            if item in row:
                return True
        return False

    def __add__(self, other): #TODO: Take care of exceptions
        """
        Creates new csv file which is combination of two other files
        :param other: second csv file object
        :return: new csv file as object (after creating)
        """

        # ensure other is csv
        if not isinstance(other, CsvFile):
            raise InstanceError(type(other), 'csv')

        # ensure headers are identical
        h1 = self.header
        h2 = other.header
        if None in (h1, h2):
            raise HeaderError('Both files should be with header')
        if not self._is_identical(h1, h2):
            raise HeaderError('The headers are not equals')

        # new file path
        new_fp = os.path.join(self.root, self.file_name + '_' + other.file_name + self._ext)

        if os.path.exists(new_fp):
            raise PathAlreadyExistsError(new_fp)

        with open(new_fp, "w", newline="") as new_csv:
            writer = csv.writer(new_csv)

            for row in self.content:
                writer.writerow(row)
            for row in other.content[1:]:
                writer.writerow(row)

        new_csv = CsvFile(new_fp, header=True)
        return new_csv

    def __len__(self):
        """

        :return: number of rows in file without header
        """
        if self._isheader:
            num_of_rows = -1
        else:
            num_of_rows = 0
        for row in self._content:
            num_of_rows += 1
        return num_of_rows

    def shape(self):
        """
        returns (num_of_rows, num_of_columns)
        """
        num_of_rows = 0
        for row in self._content:
            num_of_rows += 1
        num_of_col = len(self.content[0])

        return num_of_rows, num_of_col

    @property
    def header(self) -> list | None:
        if self._isheader:
            return self.content[0]
        else:
            return None

    def get_row(self, n, w=False):
        """
        :param w: bool - with headers in row?
        :param n: wanted row number
        :return: row content
        """
        if n not in range(len(self)):
            raise OutOfRange(n) #out of range

        wanted_row = self.content[n]
        if w:
            if self._isheader:
                wanted_row = {wanted_row[i]:self.header[i] for i in range(len(wanted_row))}

            else:
                raise HeaderError('There is no header') #no header
            return wanted_row

    def get_column_header(self, n):
        """
        :param n: number of column
        :return: column name
        """
        if self._isheader:
            return self.header[n]
        else:
            return None

    def get_column_data(self, n):
        """
        :param n: column number
        :return: list with all cells in column
        """
        column_data = [self.content[n] for row in self.content]
        return column_data

    def get_cell(self, row_num, column_num):
        """
        :param row_num:
        :param column_num:
        :return: content of table cell
        """
        with open(self._file_path, 'r', newline="") as csvf:
            read_f = csv.reader(csvf, delimiter=self._delimiter)
            csv_list = list(read_f)

            # if the row and column out of range
            if len(csv_list) < row_num - 1 and len(csv_list[0]) < column_num:
                # raise ValueError (out of range)
                pass

            return csv_list[row_num][column_num - 1]

    def search(self, val):
        """
        finds all appearances of parameter
        :param val to search
        :return: []list of tuples(row_num, column_num)
        """
        locations = []
        for index, row in enumerate(self._content):
            if val in row:
                for i, v in enumerate(row):
                    if v == val:
                        locations.append((index, i))
        return locations

    def count(self, val) -> int:
        return len(self.search(val))

    def addrow(self, row_to_add: list):  # TODO: H
        # ",".join(row_to_add)
        # add with csv.write/home/hemed/Desktop/fullstack_course/TextFiles
        pass

    def deleterow(self, row_num):  # TODO: H
        pass

    def update_cell(self, cell_column, cell_row):
        pass  # TODO: Y

    def average(self, n, beginning_row=0, end_row=len(self)):
        #TODO: EXCEPTIONS AND ERRORS - H
        """
         :param n: column serial number
         :param beginning_row: row serial number
         :param end_row: row serial number
         :return: float
         """
        sum_num = self.sum_column(n, beginning_row, end_row)
        divider = len(self.content[beginning_row:end_row])
        return sum_num/divider

    def sum_column(self, n, beginning_row=0, end_row=(len(self)):
        """

        :param n: column serial number
        :param beginning_row: row serial number
        :param end_row: row serial number
        :return: float
        """
        sum_num = 0
        column = self.get_column_data(n)
        for item in column[beginning_row:end_row]:
            if isinstance(item, (int, float)):
                sum_num += item
        return sum_num

    def _csv_list(self, fd):
        """
        :return: csv as list of lists
        """
        ret_val = []
        for row in csv.reader(fd, delimiter=self._delimiter):
            ret_val.append(row)
        return ret_val

    def _csv_dict(self, fd):
        """
        :return: csv as list of dicts
        """
        ret_val = []
        for row in csv.DictReader(fd, delimiter=self._delimiter):
            ret_val.append(row)
        return ret_val

    def _specific_content(self, fd, dict_type=False):  # TODO: add decorators
        """

        :param dict_type: wanted return, False or True -> list of lists or list of dicts
        :return: s/l
        """
        if not dict_type:
            return self._csv_list(fd)
        return self._csv_dict(fd)

    @staticmethod
    def _is_identical(h1: list, h2: list) -> bool:
        """
        Compares headers to ensure safe join
        :param h1: list
        :param h2: list
        :return: bool
        """
        return h1 == h2