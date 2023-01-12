from text_file_parent import TextFile
import json


class JsonFile (TextFile):

    def _get_specific_content(self, fd):
        return json.load(fd)

    def _get_ext(self):
        return 'json'

    def _json_file_load(self):
        with open(self._file_path, 'r') as fd:
            json_file_name = json.load(fd)
        return json_file_name

    def is_list(self):
        if type(self._json_file_load()) is list:
            return True
        return False

    def is_dict(self):
        if type(self._json_file_load()) is dict:
            return True
        return False

    def get_keys(self):
        pass

    def add_data(self, key, new_value): #TODO: H
        #load json
        #check if key exists
        # if yes: add to key -> key:[old_value, new_value]
        # if no- add key -> key:new_value
        #dump json in separate func
        pass

    def is_in(self, val: str | int) -> bool: #TODO: H
        pass

    def search(self, val): #TODO: H
        pass

    def create(self): #TODO: Y
        pass

    def count(self, val) -> int: #TODO: Y
        pass

    def __len__(self):
        pass
