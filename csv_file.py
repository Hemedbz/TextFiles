from text_file_parent import TextFile
import csv, os

class CsvFile (TextFile):

    def __init__(self, file_path, delimiter=',', header=True ):
        """

        :param file_path:
        :param delimiter:
        :param header: The user insert True if there is a header else False
        """
        super().__init__(file_path)
        self.header = header
        self._delimiter = delimiter
        self._ext = 'csv'

    def __len__(self):
        """

        :return: number of rows in file without header #TODO: takeout headers
        """
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
        for row in self._content:
            num_of_col = len(row)
            break
        return (num_of_rows, num_of_col)

    def __str__(self):
        pass #TODO: LATER think about what to write here (file name, type, headers, number f rows, date modified- check how we get it)

    def _specific_content(self, val): #TODO: Re-implement -> H
        """

        :param val: wanted return, s or l -> string or list of dicts
        :return: s/l
        """
        ret_val = []
        for row in csv.DictReader(fd, delimiter=self._delimiter):
            ret_val.append(row)
        return ret_val

    def get_headers(self) -> list | None:
        if self.header:
            for row in self.content:
                return row
        return None

    def get_row(self, row_num): #TODO: Check if should redo -H
        with open(self._file_path, "r", newline="") as csvfile:
            read_file = csv.DictReader(csvfile, delimiter=self._delimiter)

            counter = 0
            for item in read_file:
                counter += 1
                if counter == row_num:
                    return item
        raise Exception()#out of range

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

    @staticmethod
    def _is_identical(h1: list, h2: list) -> bool:
        """
        Compares headers to ensure safe join
        :param h1: list
        :param h2: list
        :return: bool
        """
        count = 0
        for cul in h1:
            for cul2 in h2:
                if cul == cul2:
                    count += 1

        if len(h1) == count:
            return True
        return False

    def _is_header(self, csv_line) -> bool: #TODO: Look at again and make sure is good - Y
        """
        ensures first row is header
        """
        first_line = "".join(csv_line)
        first_line = "".join(first_line.split(" "))
        first_line = "".join(first_line.split(self._delimiter))
        if first_line.isalpha():
            return True
        return False

#TODO: Go over both functions and shorten - Y - later
    # def _get_column_name_by_num(self, r, column_n):
    #     line = next(r)
    #     if self._is_header(line):
    #         header = line[0].split(self._delimiter)
    #         return header[column_n - 1]
    #     return column_n
    #
    # def get_column(self, column_num: int):
    #     clu_info = []
    #     with open(self._file_path, "r", newline="") as csvfile:
    #         re = csv.reader(csvfile)
    #         # check if there is a header. if true return name of column else return the column_num
    #         clu_name = self._get_column_name_by_num(re, column_num)
    #         clu_info.append(clu_name)
    #         csvfile.seek(0)
    #
    #         # if csv file haven't header
    #         if clu_name == column_num:
    #             csv_obj = csv.reader(csvfile)
    #             for item in csv_obj:
    #                 clu_info.append(item[0].split(self._delimiter)[column_num - 1])
    #             return clu_info
    #
    #         csv_obj = csv.DictReader(csvfile, delimiter=self._delimiter)
    #         for item in csv_obj:
    #             clu_info.append(item[clu_name])
    #         return clu_info


    def add_header(self, header: list):
        pass

    def __add__(self, other):
        """
        Creates new csv file which is combination of two other files
        :param other:
        :return:
        """

        if not isinstance(other, CsvFile):
            raise Exception() #TODO: Rename all exceptions: at end who cares now
        # self.check_type(other)

        header1, header2 = self.headers(), other.headers()

        if not self._is_header(header1) and not other._is_header(header2):
            raise Exception()

        if not self._is_identical(header1, header2):
            raise Exception()

        file_path_name = self.get_root() + "\\" + self.get_file_name() + "_" + other.get_file_name() + \
                        self.get_file_extension()

        if os.path.exists(file_path_name):
            raise Exception()

        with open(file_path_name, "w", newline="") as csv_f:
            writer = csv.DictWriter(csv_f, fieldnames=header1)
            writer.writeheader()
        # [{name: bla, age: bla},{name: bla, age: bla}]
            for row in self.get_content():
                writer.writerow(row)
            for row in other.get_content():
                writer.writerow(row)

        return True

    def average(self, column):
        pass #TODO: Later
    #add aversge by row range

    def addrow(self, row_to_add: list): #TODO: For WeWork
        # ",".join(row_to_add)
        # add with csv.write
        pass

    def deleterow(self, row_num): #TODO: For WeWork
        pass

    def update_cell(self, cell_column, cell_row):
        pass #TODO: For WeWork

    def __contains__(self, item):
        for row in self._content:
            if item in row:
                return True
        return False

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






