import abc
import csv
import os

from exceptions import *
from text_file_parent import TextFile

# header = False
# def csv_open_big_file_generator(num_of_lins = 1):
#     with open('D:\\Full_Stack_Python\\C10\\files\\text-Copy.csv', 'r') as cv:
#         f = csv.reader(cv, delimiter=',')
#         lins_list = []
#         count = 0
#         header_flag = True if header else False
#
#         for row in f:
#             if header and header_flag:
#                 header_flag = False
#                 continue
#             elif count < num_of_lins:
#                 lins_list.append(row)
#                 count += 1
#             else:
#                 yield lins_list
#                 lins_list = [row]
#                 count = 1
#         if lins_list:
#             yield lins_list
#
#
#
# for i in csv_open_big_file_generator(2):
#     print(i)
#
# print()
# for i in csv_open_big_file_generator():
#     print(i)




# Menu for this file:
    # built-in functions
    # public functions - read
    # math functions - write
    # private functions


class CsvFile(TextFile):

    def __init__(self, file_path, delimiter=',', header=True ):
        """

        :param file_path:
        :param delimiter: default ","
        :param header: bool -> does file have header
        """
        self._isheader = header
        self._delimiter = delimiter
        # self._ext = 'csv'
        super().__init__(file_path)



    def __str__(self):
        return f"{self.file_name}\n" \
               f"contains {len(self)} rows\n" \
               f"header: {self.header}\n" \
               f"file creation time: {self.creation_time}\n" \
               f"file last modified: {self.last_modified}"

    def __contains__(self, item):
        for row in self.content():
            if item in row:
                return True
        return False

    def __add__(self, other): #TODO: Take care of exceptions
        """
        Creates new csv file which is combination of two other files
        :param other: second csv file object
        :return: new csv file as object (after creating)
        """
        count = 0

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
        ext = '.' + self._ext()
        new_fp = os.path.join(self.root, self.file_name + '_' + other.file_name + ext)

        if os.path.exists(new_fp):
            raise PathAlreadyExistsError(new_fp)

        # Must use DictReader -> If the header is the same but in a different order the final table will be incorrect
        with open(new_fp, "w", newline="") as new_csv:
            writer = csv.DictWriter(new_csv, fieldnames=h1)
            writer.writeheader()

            for row in self._csv_dictreader_generator():
                writer.writerow(row)
            for row in other._csv_dictreader_generator():
                writer.writerow(row)

        new_csv = self._create_new(new_fp)
        # new_csv = CsvFile(new_fp, header=True)
        return new_csv

    def __len__(self):
        """

        :return: number of rows in file without header
        """
        if self._isheader:
            num_of_rows = -1
        else:
            num_of_rows = 0
        for row in self.content():
            if self.many:
                print(row)
                num_of_rows += len(row)
            else:
                num_of_rows += 1
        return num_of_rows

    def __iter__(self):
        self.text = open(self.file_path, 'r')
        return self

    def __next__(self):
        read = self.text.readline()  # 'Identifier,First name,Last name\n'
        if read == '':
            self.text.close()
            raise StopIteration()
        read = read.rstrip("\n")  # 'Identifier,First name,Last name'
        return read.split(self._delimiter)  # ['Identifier', 'First name', 'Last name']



        # try:
        #     return self._csv_open_big_file_generator(1, False)
        # except Exception:
        #     raise StopIteration()

    @staticmethod
    @abc.abstractmethod
    def _create_new(path):
        pass

    @abc.abstractmethod
    def _csv_dictreader_generator(self):
        pass

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
            for row in self.content():
                if self.many:
                    return row[0]
                else:
                    return row
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

    def average(self, n, beginning_row=0, end_row=None):
        #TODO: EXCEPTIONS AND ERRORS - H
        """
         :param n: column serial number
         :param beginning_row: row serial number
         :param end_row: row serial number
         :return: float
         """
        sum_num = self.sum_column(n, beginning_row, end_row if end_row is not None else len(self))
        divider = len(self.content[beginning_row:end_row if end_row is not None else len(self)])
        return sum_num/divider

    def sum_column(self, n, beginning_row=0, end_row=None):
        """

        :param n: column serial number
        :param beginning_row: row serial number
        :param end_row: row serial number
        :return: float
        """
        sum_num = 0
        column = self.get_column_data(n)
        for item in column[beginning_row:end_row if end_row is not None else len(self)]:
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

    def _ext(self):
        return 'csv'

    @property
    def delimiter(self):
        return self._delimiter

    # @delimiter.setter
    # def delimiter(self, value):
    #     pass


class LargeCsvFile(CsvFile):

    def __init__(self, file_path, delimiter=',', header=True, num_of_lines=1, many=False):
        super().__init__(file_path, delimiter, header)
        if num_of_lines > 1 and many is False or num_of_lines == 1 and many:
            raise Exception()

        self.num_of_lines = num_of_lines
        self.many = many
        self.content = self._generate_call

    def display_content(self):
        """
        Print the csv file
        """
        for row in self.content():
            print(row)

    def _generate_call(self):
        return self._csv_open_big_file_generator(self.num_of_lines, self.many)

    def _csv_open_big_file_generator(self, num_of_lines, many):
        """
        Generator of open csv file as csv reader
        :param num_of_lines: The bunch of lines the user want to get each time
        :param many: True if num_of_lines > 1 else False
        :return:
        """
        with open(self.file_path, 'r') as cv:
            f = csv.reader(cv, delimiter=self.delimiter)
            lines_list = []
            count = 0

            start_first_time = True
            header_flag = True if self._isheader else False

            for row in f:

                if many:
                    # if self._isheader and header_flag:
                    #     header_flag = False
                    #     count += 1
                    #     continue
                    if count < num_of_lines:
                        lines_list.append(row)
                        count += 1
                    else:
                        yield lines_list
                        lines_list = [row]
                        count = 1
                else:
                    yield row

            if lines_list and many:
                yield lines_list

    def _csv_dictreader_generator(self):
        """
        Generator of open csv file as a DictReader
        :return:
        """
        with open(self.file_path, 'r') as cv:
            f = csv.DictReader(cv, delimiter=self.delimiter)

            for row in f:
                yield row

    @staticmethod
    def _create_new(path):
        return LargeCsvFile(path)


if __name__ == '__main__':
    # cv = LargeCsvFile('D:\\Full_Stack_Python\\C10\\files\\text_text_4.csv', num_of_lines=2, many=True)
    cv = LargeCsvFile('D:\\Full_Stack_Python\\C10\\files\\text_text_4.csv', num_of_lines=1, many=False)
    cv2 = LargeCsvFile('D:\\Full_Stack_Python\\C10\\files\\text_text_4.csv', num_of_lines=1, many=False)

    # cv3 = cv + cv2
    # print(len(cv3))

    for row in cv:
        print(row)

    # print(len(cv))
    # print(cv.display_content())

    # text = open('D:\\Full_Stack_Python\\C10\\files\\text_text_4.csv', 'r')
    # read = text.readline()
    # read = read.rstrip("\n")
    # print(read.split(','))





