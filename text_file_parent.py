class TextFile(ABC):

    def __init__(self, file_path: str):
        # if not os.path.exists(file_path):
        #     raise Exception()
        if os.path.splitext(file_path)[-1][1:] != self._get_ext():
            raise Exception()
        self._file_path = file_path

    def get_file_size(self):
        return os.stat(self._file_path).st_size

    def get_content(self):
        with open(self._file_path, 'r') as fd:
            content = self._get_specific_content(fd)
        return content
        # open a file (fd / fh) - common for all
        # get content - specific

    def _base_name_file_path(self):
        return os.path.basename(self._file_path)

    def get_file_name(self):
        return os.path.splitext(self._base_name_file_path())[0]

    def get_file_extension(self):
        return os.path.splitext(self._base_name_file_path())[-1]

    def get_file_path(self):
        return os.path.dirname(self._file_path)

    @abstractmethod
    def is_in(self, val: str | int) -> bool:
        pass

    @abstractmethod
    def search(self, val):
        pass

    @abstractmethod
    def count(self, val) -> int:
        pass

    @abstractmethod
    def __len__(self, *args) -> int:
        pass

    @abstractmethod
    def _get_specific_content(self, fd):
        pass

    @abstractmethod
    def _get_ext(self):
        pass