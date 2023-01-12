from abc import ABC, abstractmethod
import os
from exceptions import *

class TextFile(ABC):

    def __init__(self, file_path: str):
        if os.path.splitext(file_path)[-1][1:] != self._ext():
            raise FileNotMatchError
        #TODO: if not exists: raise exception NoFile(-> create) -> Y

        self._file_path = file_path
        self._content = self.get_content()
        self.file_size = os.stat(self._file_path).st_size
        self.root = os.path.dirname(self._file_path)
        self.base_name = os.path.basename(self._file_path)
        self.file_name = os.path.splitext(self.base_name)[0]

    def __str__(self):
        return str(self._content)

    def get_content(self):
        with open(self._file_path, 'r') as fd:
            content = self._specific_content(fd)
        return content

    def get_file_extension(self):
        return os.path.splitext(self.base_name)[-1]

    def get_file_path(self):
        return self._file_path

    def is_exists(self):
        if not os.path.exists(self._file_path):
            return False
        return True

    @abstractmethod
    def is_in(self, val: str | int) -> bool:
        pass

    @abstractmethod
    def search(self, val):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def count(self, val) -> int:
        pass

    @abstractmethod
    def __len__(self, *kwargs) -> int:
        pass

    @abstractmethod
    def _specific_content(self, fd):
        pass

    @abstractmethod
    def _ext(self):
        pass