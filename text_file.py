import csv
import json
import os.path
from text_file_parent import TextFile


# ------------------------- CsvFile --------------------------------------------------


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


