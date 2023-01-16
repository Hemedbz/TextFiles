from text_file_parent import TextFile
import json


class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._ext = 'json'
        self.keys = [key for key in self._content]
        self.values = [self._content[key] for key in self._content]
        self.type = type(self._content) #TODO: Think of how to refactor code if not dict and not list - H&Y

    def _specific_content(self, fd):
        return json.load(fd)

    def get_keys(self):
        pass

    def add_data(self, key, new_value): #TODO: H
        if self.type = 'dict':
            with open(self._file_path, 'r') as fh:
                data = json.load(fh)
            if key not in data: data[key] = new_value
            elif key in data: data[key] = list(data[key]).append(new_value)
            with open(self._file_path, 'w'):
                json.dump(data)
        elif self.type = 'list':
            pass

    def __contains__(self, item):
        """
        Checks if value in json file
        :param item
        :return:
        """
        if item in self.values or item in self.keys:
            return True
        else:
            return False

    def search(self, param):
        data = []
        if self.type == 'dict':
            for key, value in self._content:
                if param == key or data in value:
                    data.append({key:value})
        elif self.type == 'list':
            for i in self._content:
                if param in i:
                    data.append(i)
        return data
    #TODO: Deep search in sub dict - H

    def count(self, val) -> int:
        return len(self.search(val))