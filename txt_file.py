from text_file_parent import TextFile
from exceptions import *


class TxtFile (TextFile):
    pass

    def _get_specific_content(self, fd):
        return fd.read()

    def _get_ext(self):
        return 'txt'

    def __add__(self, other):
        if not isinstance(other, TxtFile):
            raise ValueError("2 values must be TxtFile type")

        file_path_name = self.get_file_path() + "\\" + self.get_file_name() + "_" + other.get_file_name() + \
                         self.get_file_extension()

        if os.path.exists(file_path_name):
            file_name_exists = f"{self.get_file_name()}_{other.get_file_name()}{self.get_file_extension()}"
            raise FileNameExistsEror(file_name_exists)

        with open(file_path_name, 'w') as fh:
            fh.write(self.get_content() + other.get_content())

        return True

    def _txt_file_read(self):
        with open(self._file_path, 'r') as fd:
            return fd.read()

    # def __len__(self, *kwargs):
    #     if kwargs[0] == 'c':
    #         return len(self._txt_file_read())
    #     elif kwargs[0] == 'w':
    #         return len(self._txt_file_read().split())
    #     else:
    #         raise InvalidInputError(val)

    def is_in(self, val: str | int) -> bool: #TODO: H
        pass

    def search(self, val): #TODO: H
        pass

    def create(self): #TODO: Y
        pass

    def count(self, val) -> int: #TODO: Y
        pass


# if __name__ == '__main__':
#     alice = TxtFile("features.txt")
#     print(len(alice, 'c'))
#
# #TODO: Ask V about __len__
