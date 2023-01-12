from text_file_parent import TextFile
import csv, os

class CsvFile (TextFile):

    def __init__(self, file_path, delimiter=','):
        super().__init__(file_path)
        self._delimiter = delimiter

    def _get_ext(self):
        return 'csv'

    def _get_specific_content(self, val): #TODO: Re-implement -> H
        """

        :param val: wanted return, s or l -> string or list of dicts
        :return: s/l
        """
        ret_val = []
        for row in csv.DictReader(fd, delimiter=self._delimiter):
            ret_val.append(row)
        return ret_val

    def headers(self) -> list:
        #dict reader- 1st row - keys #TODO- Y
        #if no headers- None
        pass

    def __len__(self):
        #TODO: H
        pass

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


    def _is_header(self, csv_line) -> bool: #TODO: Look at again and make sure is good - later
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

        file_path_name = self.get_file_path() + "\\" + self.get_file_name() + "_" + other.get_file_name() + \
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

    def addrow(self, row_to_add: list): #TODO: H
        # ",".join(row_to_add)
        # add with csv.write
    pass

    def deleterow(self, row_num): #TODO: For WeWork
        pass

    def update_cell(self, cell_column, cell_row):
        pass #TODO: For WeWork

    #TODO: Read again about generators

    def is_in(self, val: str | int) -> bool: #TODO: H
        pass

    def search(self, val): #TODO: H
        pass

    def create(self): #TODO: Y
        pass

    def count(self, val) -> int: #TODO: Y
        pass