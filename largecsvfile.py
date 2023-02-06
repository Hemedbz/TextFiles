import csv
from csv_file import CsvFile


class LargeCsvFile(CsvFile):

    def __init__(self, file_path, delimiter=',', has_header=True, as_dict=False, iterator_size=1, many=False):
        super().__init__(file_path, delimiter, has_header, as_dict)
        if iterator_size > 1 and many is False \
                or iterator_size == 1 and many:
            raise Exception() #TODO: Define exception
        if iterator_size < 1:
            raise Exception() #TODO: Define exception

        self._lines_for_iterator = iterator_size
        self._many = many

    def __add__(self, other):
        raise Exception("Adding two large files is not possible through this package")

    def __iter__(self):
        for row in self._listreader_generator():
            yield row

    def _call_generator(self):
        return self._listreader_generator()

    def _listreader_generator(self):

        with open(self.file_path, 'r') as cv:
            f = csv.reader(cv, delimiter=self._delimiter)
            lines_list = []
            count = 0

            for row in f:

                if self._many:
                    if count < self._lines_for_iterator:
                        lines_list.append(row)
                        count += 1
                    else:
                        yield lines_list
                        lines_list = [row]
                        count = 1

                    if len(lines_list) > 1:
                        yield lines_list

                else:
                    yield row

    def _dictreader_generator(self):
        """
        Generator of open csv file as a DictReader
        :return:
        """
        with open(self.file_path, 'r') as cv:
            f = csv.DictReader(cv, delimiter=self._delimiter)

            for row in f:
                yield row

    def load_content(self):
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                yield row
