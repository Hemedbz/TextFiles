from text_file_parent import TextFile
import json


class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._content = self.get_content()
        self.keys = [key for key in self._content]
        self.values = [self._content[key] for key in self._content]

    def _get_specific_content(self, fd):
        return json.load(fd)

    def _get_ext(self):
        return 'json'

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
    #
    # def is_in(self, val: str | int) -> bool:
    #     """
    #     Checks if value in json file
    #     :param val:
    #     :return:
    #     """
    #     if val in self.values or val in self.keys:
    #         return True
    #     else:
    #         return False
    #
    # def search(self, val):
    #     if not self.is_in(val):
    #         return None
    #     ret_val = []
    #     for val in self.keys:
    #         ret_val.append({val:self._content[val]})
    #     if val in self.values:
    #         ret_val.append({self._content[n]:)
    #     return ret_val
# TODO: With "for key, val" H

    def create(self): #TODO: Y
        pass

    def count(self, val) -> int: #TODO: Y
        pass

    def __len__(self):
        pass

# if __name__ == '__main__':
