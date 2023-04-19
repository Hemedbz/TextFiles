class TextFileExceptions(Exception):
    pass


class NoFile(TextFileExceptions):
    pass


class InvalidInputError(TextFileExceptions):
    def __init__(self, val):
        super().__init__(f"{val} not in..")


# class TypeError(TextFileExceptions):
#     pass


class PathAlreadyExistsError(TextFileExceptions):
    def __init__(self, val):
        super().__init__(f"{val} already exist")


class FilePathNotExistsError(TextFileExceptions):
    def __init__(self, val):
        super().__init__(f"'{val}': file not exists")


class InstanceError(TextFileExceptions):
    def __init__(self, type_other, type_class):
        super().__init__(f"can't add {type_other} file to {type_class} file")


class HeaderError(TextFileExceptions):
    def __init__(self, text):
        super().__init__(text)


class OutOfRange(TextFileExceptions):
    def __init__(self, param):
        super().__init__(f'{param} not in range')

class KeyValueError(TextFileExceptions):
    def __init__(self, msg):
        super().__init__(msg)


class IndexValueError(TextFileExceptions):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidTypeError(TextFileExceptions):
        def __init__(self, param):
        super().__init__(f'{param} file not supported')


class SizeError(TextFileExceptions):
        def __init__(self, param):
        super().__init__(f'{param} is too large')

