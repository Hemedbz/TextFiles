class TextFileExceptions(Exception):
    pass

class NoFile(TextFileExceptions):
    pass

class InvalidInputError(TextFileExceptions):
    def __init__(self, val):
        super().__init__(f"{val} not in..")

class TypeError(TextFileExceptions):
    pass

class AlreadyExists(TextFileExceptions):
    def __init__(self, val):
        super().__init__(f"{val} already exist")