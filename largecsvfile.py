from csv_file import CsvFile


class LargeCsvFile(CsvFile):

    def __init__(self, file_path, delimiter=',', header=True, num_of_lines=1, many=False):
        super().__init__(file_path, delimiter, header)
        if num_of_lines > 1 and many is False or num_of_lines == 1 and many:
            raise Exception()

        self._num_of_lines = num_of_lines
        self._many = many


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

