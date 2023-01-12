from text_file_parent import TextFile
import json


class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._ext = 'json'
        self.keys = [key for key in self._content]
        self.values = [self._content[key] for key in self._content]
        self.type = type(self._content)

    def _specific_content(self, fd):
        return json.load(fd)

    def get_keys(self):
        pass

    def add_data(self, key, new_value): #TODO: H
        #load json
        #check if key exists
        # if yes: add to key -> key:[old_value, new_value]
        # if no- add key -> key:new_value
        #dump json in separate func
        pass

    def is_in(self, val: str | int) -> bool:
        """
        Checks if value in json file
        :param val:
        :return:
        """
        if val in self.values or val in self.keys:
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

    def count(self, val) -> int:
        return len(self.search(val))