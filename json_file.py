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

    def search(self, param) ->list:

        if self.type is dict:
            return self._search_dict(param, dictionary=self.content)
        elif self.type is list:
            return self._search_list(param, l=self.content)
        elif self.type is int:
            return self._search_identical(param)
        elif self.type is float:
            return self._search_identical(param)
        elif self.type is str:
            return self._search_str(param)
        elif self.type is bool:
            return self._search_identical(param)
        elif self.type is None:
            return self._search_identical(param)


    def add_data(self, new_value, key=None, create_list=False):
        """
        The function add data to all types of Jason files
        :param create_list: True if the user want to add new_value in list
                            else False if the user want to add the new_value
                            to the object that inside. type -> int, float, str.
                            the default fot type bool is creating list.
        """
        # self.get_content()

        if self.type is dict:
            self._add_data_dict(new_value, key)
        elif self.type is list:
            self._add_data_list(new_value, key)
        elif self.type is int:
            self._add_data_num(new_value, create_list)
        elif self.type is float:
            self._add_data_num(new_value, create_list)
        elif self.type is str:
            self._add_data_str(new_value, create_list)
        elif self.type is bool:
            self._add_data_bool(new_value)
        elif self.type is None:
            self._add_data_none(new_value)

        self._dump_content()

    def _dump_content(self):
        with open(self._file_path, 'w') as fd:
            json.dump(self.content, fd)

    def count(self, val):
        return len(self.search(val))

    def delete_data(self, key: int | str | None = None, index_in_list: int | None = None):
        # The user have to enter one of the value
        if (key, index_in_list) is None:
            raise Exception()
        pass #TODO: H

    # sub functions by json type

    def _add_data_dict(self, new_value, key):
        # if the json type is dict and the user didn't transfer a key
        if key is None:
            raise Exception()

        if key not in self.content:
            self.content[key] = new_value
        elif key in self.content:
            if type(self.content[key]) is list: # cant compared type to str
                self.content[key].append(new_value)
            else:
                self.content[key] = [self.content[key], new_value]
    @staticmethod
    def _add_data_dict_in_list(new_value, key, content_in_list):
        # if the json type is dict and the user didn't transfer a key
        if key is None:
            raise Exception()

        if key not in content_in_list:
            content_in_list[key] = new_value
        elif key in content_in_list:
            if type(content_in_list[key]) is list:
                content_in_list[key].append(new_value)
            else:
                content_in_list[key] = [content_in_list[key], new_value]
        return content_in_list

    def _add_data_list(self, new_value, key):
        key_in_val_flag = False
        for inx, val in enumerate(self.content):
            if type(val) is dict:
                if key in val:
                    key_in_val_flag = True
                    self.content[inx] = self._add_data_dict_in_list(new_value, key, val)
        if not key_in_val_flag:
            self.content.append(new_value)

    def _add_data_str(self, new_value, create_list):
        if type(new_value) is str and not create_list:
            self.content = self.content+f"\n " \
                                          f"{new_value}"
        else:
            self.content = [self.content, new_value]

    def _add_data_num(self, new_value, create_list):
        if type(new_value) in [int, float] and not create_list:
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

    def _search_list(self, value, l):
        findings = []
        for i in l:
            if i == value:
                findings.append(i)
            elif isinstance(i, dict):
                findings.append(self._search_dict(value, i))
            elif isinstance(i, list):
                findings.extend(self._search_list(value, i))
        return findings


    def _search_identical(self, param):
        if param == self.content:
            return self.content
        else:
            return None

    def _search_str(self, param):
        return re.findall(param, self.content)
