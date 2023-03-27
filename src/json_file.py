from text_file_parent import TextFile
import json
import re
from src.exceptions import *


class JsonFile(TextFile):

    def __init__(self, file_path: str):
        """

        :param file_path: str
        """
        super().__init__(file_path)
        self.type = type(self.content)

        # if the type of the file is dict -> save list of key and list of value
        if self.type == 'dict':
            self.keys = [key for key in self.content]
            self.values = [self.content[key] for key in self.content]

    def _specific_content(self, fd):
        return json.load(fd)

    def _ext(self):
        return 'json'

    # def __contains__(self, item: str | int) -> bool:
    #     """
    #     Checks if value in json file
    #     :param item
    #     :return:
    #     """
    #     if self.type == dict and self._search_dict(item, dictionary=self.content) != [] or \
    #             self.type == list and self._search_list(item, given_list=self.content) != []:
    #         return True
    #     elif item == self.content:
    #         return True
    #     return False

    def __iter__(self):
        if self.type in [dict, list, str]:
            return iter(self.content)
        else:
            raise TypeError("Non Iterable")

    def __str__(self):
        return f"{self.file_name}\n" \
               f"file creation time: {self.creation_time}\n" \
               f"file last modified: {self.last_modified}"

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
            return self._search_list(param, given_list=self.content)
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

    def _locator(self, locator: str) -> int | str | list | dict | bool | float:
        dict_locator = {}
        exec(f"dict_locator[content] = self.content{locator}")
        return dict_locator[content]

    def add_data(self, content_locator: str = None, new_index: int = None, new_key: str = None,
                 new_value: int | str | list | dict | bool | float = None, to_list=False):
        """
        The function allows adding values, index or keys to a JSON file.
        :param content_locator: str -> The path to the item you want to add to. -> [0]['Name]...
                If the content locator is None, then the item is added to the file without hierarchy
        :param new_index: int -> the place where you want to input the variable.
                If the item is a list, it must include an index
        :param new_key: str -> the key that you want to add or an existing key that you want to add a value to.
                If the item is a dictionary, it must include a key
        :param new_value: The value that you want to add.
        :param to_list: True, if you want to add the value to a list, otherwise False -
                False is the default. -> only if type - only if the type is str, int, or float.
        """

        file_content = self.content
        self.lock.acquire()

        # check if content_locator is None - if True insert to content the whole content
        if content_locator is None:
            content = self.content
        else:
            content = self._locator(content_locator)

        # content = file_content[content_locator]
        tyc = type(content)
        if tyc == dict:
            if new_key is None:
                raise KeyError("For dictionary type must insert a key")
            content = self._add_data_dict(content, new_key, new_value)
        elif tyc == list:
            content = self._add_data_list(content, new_index, new_value)
        elif tyc == str:
            content = self._add_data_str(content, new_value, to_list)
        elif tyc == float or tyc == int:
            content = self._add_data_num(content, new_value, to_list)
        elif tyc == bool:
            content = self._add_data_bool(content, new_value)
        elif content is None:
            content = new_value
            # self._add_data_none(content, new_value)

        exec(f"file_content{content_locator} = content\nself._content = file_content")

        self._dump_content()
        self.lock.release()

    def remove_data(self, content_locator: str, key: str | int = None, index: int = None):
        """
        removes specific data from json for type -> list, dict only
        :param content_locator: str -> The path to the item you want to delete. -> [0]['Name]...
        Can't be None
        :param key: If the item is a dictionary, it must include a key
        :param index: If the item is a list, it must include an index
        """
        pattern = f"{key}']$" + f'|{key}"]$'
        self.lock.acquire()
        if key is not None:
            if not re.findall(pattern, content_locator):
                raise KeyValueError('The key does not match the path content_locator')
        elif index is not None:
            if not re.findall(f"{index}]$", content_locator):
                raise IndexValueError('The index does not match the path content_locator')
        elif key is None and index is None:
            raise ValueError("Must enter a key if it's a dictionary or enter an index if it's a list.")

        exec(f"del self.content{content_locator}")
        self._dump_content()
        self.lock.release()

    @staticmethod
    def _add_data_dict(content: dict, key: str, new_value: int | str | list | dict | bool | float) -> dict:
        if key not in content:
            content[key] = new_value

        # if the key already exist
        elif key in content:
            if type(content[key]) is list:
                content[key].append(new_value)
            else:
                content[key] = [content[key], new_value]
        return content

    @staticmethod
    def _add_data_list(content: list, index: int, new_value: int | str | list | dict | bool | float) -> list:
        content.insert(index, new_value)
        return content

    @staticmethod
    def _add_data_str(content: str, new_value: int | str | list | dict | bool | float, to_list: bool) -> str | list:
        if type(new_value) is str and not to_list:
            content = content + f"\n " \
                                f"{new_value}"
        else:
            content = [content, new_value]
        return content

    @staticmethod
    def _add_data_num(content: int | float, new_value: int | str | list | dict | bool | float,
                      to_list: bool) -> int | float | list:

        if type(new_value) in [int, float] and not to_list:
            content += new_value
        else:
            content = [content, new_value]
        return content

    @staticmethod
    def _add_data_bool(content: bool, new_value: int | str | list | dict | bool | float) -> list:
        content = [content, new_value]
        return content

    # def _add_data_none(content: None, new_value):
    #     content = new_value
    #     return content

    def _search_dict(self, param, dictionary):
        findings = []
        for key, value in dictionary.items():
            if param == key or param in value:
                findings.append({key: value})
            elif isinstance(value, list):
                if param in value:
                    findings.append(value, value.index())
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

    def _search_identical(self, value: str | int | float | bool | None) -> list:
        if value == self.content:
            return [self.content]
        else:
            return []

    def _search_str(self, value: str | int | float | bool | None) -> list:
        return re.findall(value, self.content)

