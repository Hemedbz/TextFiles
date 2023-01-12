from text_file_parent import TextFile
from exceptions import *
import os

class TxtFile(TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._content = self.get_content()
        self._words = self._content.split()
        self.lines = self._content.readlines()
        self._ext = 'txt'

    def _specific_content(self, fd):
        return fd.read()

    def __add__(self, other):
        if not isinstance(other, TxtFile):
            raise ValueError("2 values must be TxtFile type")

        new_name = self.root + "\\" + self.file_name + "_" + other.file_name + \ self._ext

        if os.path.exists(new_name):
            raise AlreadyExists(new_name)

        with open (new_name, 'x') as fh:
            fh.write(self._content + other._content)

        return True

    def __len__(self):
        """
        :return: tuple with number of characters and number of words
        """
        return (len(self._content), len(self._words))

    def is_in(self, val: str | int) -> bool:
        if val in self._content:
            return True
        else:
            return False

    def search(self, val):
        """

        :param val: string to search
        :return: list of tuples with index and line for where str was found
        """
        if not self.is_in(val):
            return None
        findings = []
        for index, line in enumerate(self.lines):
            if val in line:
                findings.append((index, line))
        return findings

    def add_row(self):
        pass

    def count(self, val) -> int:
        data = self._content
        return data.count(val)
