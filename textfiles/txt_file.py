from .text_file_parent import TextFile
from .exceptions import *
import os


class TxtFile (TextFile):
    """
    The class corresponds to a txt file, allowing an easy API for handling it.
    To initiate, simply provide the file path as a string.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.lines = self._read_lines()

    @staticmethod
    def _specific_content(fd):
        return fd.read()

    def _read_lines(self):
        with open(self.file_path) as fh:
            lines = fh.readlines()
        return lines

    def __add__(self, other) -> bool:
        """
        Creates new file that combines two existing txt files
        :param other: TxtFIle
        :return: bool, just to approve file was created
        """

        if not isinstance(other, TxtFile):
            raise ValueError("both files must be .txt")

        self.lock.acquire()

        new_name = os.path.join(self.root, self.file_name + '_' + other.file_name + '.' + self._ext)

        if os.path.exists(new_name):
            raise PathAlreadyExistsError(new_name)

        with open(new_name, 'x') as fh:
            fh.write(self._content + other._content)

        self.lock.release()

        return True

    def __len__(self) -> int:
        """
        :return: int, number of words in txt
        """
        return len(self.words)

    def __contains__(self, item: str | int) -> bool:

        if item in self._content:
            return True
        else:
            return False

    def __iter__(self):
        return iter(self.words)


    def __str__(self):
        return f"{self.file_name}\n" \
               f"contains {len(self.lines)} lines\n" \
               f"file creation time: {self.creation_time}\n" \
               f"file last modified: {self.last_modified}"

    @property
    def words(self) -> list:
        """
        :return: list of words in txt file
        """
        to_remove = []
        list_of_words = self._content.split()
        for i in range(len(list_of_words)):
            if list_of_words[i][-1] == "-":
                list_of_words[i] = list_of_words[i][0:-2] + list_of_words[i + 1]
                to_remove.append(list_of_words[i + 1])
        for word in to_remove:
            list_of_words.remove(word)
        return list_of_words

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

    def add_line(self, line, line_num=None):
        """
        Adds a line to txt file in specified place (index).
        :param line: str, content to be added
        :param line_num: int, index number of line to add. Default is last line.
        """
        if line_num is None:
            line_num = len(self.lines)

            self.lock.acquire()
            with open(self._file_path, "a") as fh:
                fh.write(f"\n"
                         f"{line}\n")
            self.lock.release()

        else:
            self.lock.acquire()
            new_text = self.lines[:line_num] + line + self.lines[line_num:]
            with open(self.file_path, "w") as fh:
                fh.write(new_text)
            self.lock.release()

    def count(self, val) -> int:
        """
        Counts appearance of value in file
        :param: str, value to be searched
        :return: int, number of appearances
        """

        return self.content.count(val)

    def _ext(self):
        return 'txt'
