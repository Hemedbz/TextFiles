class Create:

    def __init__(self, file_path, file_type):
        #if file_path exists: error
        self._file_path = file_path
        pass

    def c_txt(self):
        f = open(self._file_path, 'x')
        f.close()

    def c_csv(self):
        # header = [name, city, age]
        # rows = [[yael, tel aviv, 30], [hemed, tel aviv, 32]]
        pass

    def c_json(self):
        pass
