from text_file_parent import TextFile
import json

class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._ext = 'json'
        self.keys = [key for key in self._content]
        self.values = [self._content[key] for key in self._content]
        self.type = type(self._content) #TODO: Think of how to refactor code if not dict and not list - Ask Valeria

    def _specific_content(self, fd):
        return json.load(fd)

    def get_keys(self):
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
        if self.type == 'dict':
            return self._search_dict(param, self.content)
        elif self.type == 'list':
            return self._search_list(param)
        elif self.type == 'str':
            return self._search_str(param)
        elif self.type in ['None', 'bool', 'int', 'float']:
            raise Exception #cannot search in this types

    def add_data(self, new_value, key=None):
        if self.type == 'dict':
            return self._add_data_dict(key, new_value)
        elif self.type == 'list':
            return self._add_data_list(new_value)
        elif self.type == 'int' or if self.type == 'float':
            return self._add_data_num(new_value)
        elif self.type == 'str':
            return self._add_data_str(new_value)
        elif self.type == 'bool':
            return self._add_data_bool(new_value)
        elif self.type == 'None':
            return self._add_data_none(new_value)
        # TODO: Change to match case H

    def count(self, val) -> int:
        return len(self.search(val))