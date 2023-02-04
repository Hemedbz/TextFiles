from text_file_parent import TextFile
import json
import re, os
from exceptions import FilePathNotExistsError


class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self._ext = 'json'
        self.type = type(self.content)
        if self.type == 'dict':
            self.keys = [key for key in self.content]
            self.values = [self.content[key] for key in self.content]

    def _specific_content(self, fd, **kwargs):
        return json.load(fd)

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

    def __iter__(self):
        if self.type in [dict, list, str]:
            return iter(self.content)
        else:
            raise TypeError("Non Iterable")

    def _dump_content(self):
        with open(self._file_path, 'w') as fd:
            json.dump(self.content, fd)

    def search(self, param) ->list:
        """
        search specific string or other content in json
        :param param: content to be searched
        :return: list of findings
        """

        if self.type is dict:
            return self._search_dict(param, dictionary=self.content)
        elif self.type is list:
            return self._search_list(param, l=self.content)
        elif self.type is str:
            return self._search_str(param)
        else:
            return self._search_identical(param)

    def count(self, param):
        """
        counts how many times parameter appears in file
        return: int
        """
        return len(self.search(param))

    def add_data(self, new_value, key=None, index=-1, inner_key=None, dict_index=None, to_list=False):

        self.get_content()
        self.lock.acquire()

        if self.type is dict:
            self._add_data_dict(key, new_value)
        elif self.type is list:
            self._add_data_list(new_value, index, inner_key, dict_index)
        elif self.type is int:
            self._add_data_num(new_value, to_list)
        elif self.type is float:
            self._add_data_num(new_value, to_list)
        elif self.type is str:
            self._add_data_str(new_value, to_list)
        elif self.type is bool:
            self._add_data_bool(new_value)
        elif self.type is None:
            self._add_data_none(new_value)

        self._dump_content()
        self.lock.release()

    def remove_data(self, data): #TODO: H
        """
        removes specific data from json

        """
        if self.count(data) > 1:
            raise Exception #tell user data appears more than once, can do manually or remove all

        self.lock.acquire()
        self.content()

        if self.type == list:
            for item in self.content:
                if item == data:
                    self.content.remove(data)
                elif data in item:
                    raise Exception #tell user data is tied into other data and should be removed manually
        elif self.type == dict:
            for key, value in self.content:
                if key == data:
                    del self.content[key]
                elif value == data:
                    self.content[key] = None
                elif data in value:
                    self.content.value.remove(data)





        self._dump_content()
        self.lock.release()
        return self.content()

    # sub functions by json type

    def _add_data_dict(self, key, new_value):
        if key not in self.content:
            self.content[key] = new_value

        elif key in self.content:
            if type(self.content[key]) is list:
                self.content[key].append(new_value)
            else:
                self.content[key] = [self.content[key], new_value]

    def _add_data_list(self, new_value, index, inner_key, dict_index):
        if type(self.content[dict_index]) == 'dict':
            if key in self.content[dict_index]:
                self.content[dict_index][inner_key] = [self.content[dict_index][inner_key], new_value]
            else:
                self.content[dict_index][inner_key] = new_value
        else:
            self.content.insert(index, new_value)

    def _add_data_str(self, new_value, to_list):
        if type(new_value) is str and not to_list:
            self.content = self.content+f"\n " \
                                          f"{new_value}"
        else:
            self.content = [self.content, new_value]

    def _add_data_num(self, new_value, to_list=False):
        if type(new_value) in [int, float] and not to_list:
            self.content += new_value
        else:
            self.content = [self._content, new_value]

    def _add_data_bool(self, new_value):
        self.content = [self._content, new_value]

    def _add_data_none(self, new_value):
        self.content = new_value

    def _search_dict(self, param, dictionary):
        findings = []
        for key, value in dictionary.items():
            if param == key or param in value:
                findings.append({key: value})
            elif isinstance(value, dict):
                findings.extend(self._search_dict(param, value))
        return findings

    def _search_list(self, value, given_list):
        findings = []
        for index, content in enumerate(given_list):
            if content == value:
                findings.append((index, content))
            elif isinstance(i, dict):
                findings.append(self._search_dict(value, i))
            elif isinstance(i, list):
                findings.extend(self._search_list(value, i))
        return findings

    def _search_identical(self, value):
        if value == self.content:
            return self.content
        else:
            return None

    def _search_str(self, value):
        return re.findall(value, self.content)

if __name__ == '__main__':
    my_json = JsonFile('tests_for_json.json')
    print(my_json.type)
    for key in my_json:
        print(key)
