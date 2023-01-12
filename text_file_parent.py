from abc import ABC, abstractmethod
import os
from exceptions import *

class TextFile(ABC):

    def __init__(self, file_path: str):
        self._file_path = file_path

        if not os.path.exists(self._file_path):
            raise FileNotFoundError
        if self._ext() != self.get_extension():
            raise TypeError

        self._content = self.get_content()
        self.file_size = os.stat(self._file_path).st_size
        self.root = os.path.dirname(self._file_path)
        self.base_name = os.path.basename(self._file_path)
        self.file_name = os.path.splitext(self.base_name)[0]

    def __str__(self):
        return str(self._content)

    @abstractmethod
    def _ext(self):
        pass

    @abstractmethod
    def _specific_content(self, fd):
        pass

    def get_content(self):
        with open(self._file_path, 'r') as fd:
            self._content = self._specific_content(fd)
        return self._content

    def get_extension(self):
        return os.path.splitext(self.base_name)[-1]

    def get_file_path(self):
        return self._file_path

    @abstractmethod
    def is_in(self, val: str | int) -> bool:
        pass

    @abstractmethod
    def search(self, val):
        pass

    @abstractmethod
    def count(self, val) -> int:
        pass

    #TODO: Read again about generators- both of us
