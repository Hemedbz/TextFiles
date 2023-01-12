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

        file_path_name = self.get_root() + "\\" + self.get_file_name() + "_" + other.get_file_name() + \
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

    def __len__(self, *kwargs):
        pass
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

    def add_row(self):
        pass

    def create(self): #TODO: Y
        if not self.is_exists():
            f = open(self.get_file_path(), 'x')
            f.close()
        else:
            raise Exception()

    def count(self, val) -> int: #TODO: Y
        data = self._txt_file_read()
        return data.count(val)


if __name__ == '__main__':
    alice = TxtFile("features.txt")
    print(alice.count('header'))

    new_file = TxtFile("D:\\Full_Stack_Python\\Python_Course\\C10\\files\\new_file.txt")
    new_file.create()
#
# #TODO: Ask V about __len__
