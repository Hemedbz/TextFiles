from text_file_parent import TextFile
from exceptions import *
import os

class TxtFile(TextFile):
    pass


class TxtFile_C(TxtFile):


class TxtFile_M (TxtFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        # self._content = self.get_content()
        self.lines = self._content.readlines()
        self._ext = 'txt'

    @staticmethod
    def _specific_content(fd):
        return fd.read()

    @property
    def words(self):
        """
        :return: list of words in txt file
        """
        to_remove = []
        list_of_words = self._content.split()
        for i in range(len(list_of_words)):
            if list_of_words[i][-1] == "-":
                list_of_words[i] = list_of_words[i][0:-2]+list_of_words[i+1]
                to_remove.append(list_of_words[i+1])
        for word in to_remove:
            list_of_words.remove(word)
        return list_of_words

    def __add__(self, other):
        if not isinstance(other, TxtFile):
            raise ValueError("2 values must be TxtFile type")

        new_name = self.root + "\\" + self.file_name + "_" + other.file_name + \ self._ext

        if os.path.exists(new_name):
            raise PathAlreadyExistsError(new_name)

        with open (new_name, 'x') as fh:
            fh.write(self._content + other._content)

        return True

    def __len__(self):
        """
        :return: number of words in txt
        """
        return len(self.words)

    def __contains__ (self, item: str | int) -> bool:
        if item in self._content:
            return True
        else:
            return False

    def search(self, val):
        """
        :param val: string to search
        :return: list of tuples with index and line for where str was found
        """
        if val not in self:
            return None
        findings = []
        for index, line in enumerate(self.lines):
            if val in line:
                findings.append((index, line))
        return findings

    def add_row(self, row):
        with open(self._file_path, "a") as fh:
            fh.write(f"\n"
                     f"{row}\n")

    def count(self, val) -> int:
        return self.content.count(val)
