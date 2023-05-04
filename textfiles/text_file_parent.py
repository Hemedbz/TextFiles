from abc import ABC, abstractmethod
import os
from .exceptions import *
import time
from threading import Lock


class TextFile(ABC):

    def __init__(self, file_path: str):
        self._file_path = file_path

        if not os.path.exists(self._file_path):
            raise FileNotFoundError()
        if self._ext() != self.get_extension():
            raise TypeError
        if os.path.getsize(self._file_path) > 50000000:
            raise SizeError("File to large to handle with this library")


        self._content = self.load_content()
        self._file_size = os.stat(self._file_path).st_size
        self._root = os.path.dirname(self._file_path)
        self._base_name = os.path.basename(self._file_path)
        self._file_name = os.path.splitext(self.base_name)[0]
        self._creation_t = self.get_creation_time()
        self._last_modified_t = self._update_last_modified()
        self.lock = Lock()

    def __str__(self):
        return str(self._content)

    @abstractmethod
    def _ext(self):
        pass

    @abstractmethod
    def _specific_content(self, fd):
        pass

    @abstractmethod
    def search(self, val):
        raise Exception()


    @abstractmethod
    def count(self, val) -> int:
        raise Exception()


    def load_content(self):
        """
        The function loads the content of the file according to its type. -> csv, txt, json
        """
        with open(self._file_path, 'r') as fd:
            content = self._specific_content(fd)
        return content

    def get_extension(self):
        return os.path.splitext(self._file_path)[-1][1:]

    def get_file_path(self):
        return self._file_path

    def get_creation_time(self):
        return os.path.getctime(self._file_path)

    def _update_last_modified(self):
        return os.path.getmtime(self._file_path)


    @property
    def content(self):
        return self._content

    @property
    def creation_time(self):
        return self._creation_t

    @property
    def last_modified(self):
        return time.ctime(self._last_modified_t)

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_size(self):
        return self._file_size

    @property
    def root(self):
        return self._root

    @property
    def base_name(self):
        return self._base_name

    @property
    def file_name(self):
        return self._file_name
