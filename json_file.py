from text_file_parent import TextFile
import json
import re, os
from exceptions import FilePathNotExistsError


class JsonFile (TextFile):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.type = type(self.content)
        if self.type == 'dict':
            self.keys = [key for key in self.content]
            self.values = [self.content[key] for key in self.content]

    def _specific_content(self, fd, **kwargs):
        return json.load(fd)

    def _ext(self):
        return 'json'

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

    def add_data(self, content_locator=None, new_index=None, new_value=None, to_list=False): #TODO: TYPE CON-LOCATOR
        file_content = self.content()
        self.lock()
        content = file_content[content_locator]
        tyc = type(content)
        if tyc == dict:
            content = self._add_data_dict(content, new_index, new_value)
        elif tyc == list:
            content = self._add_data_list(content, new_value, new_index)
        elif tyc == str:
            content = self._add_data_str(content, new_value, to_list)
        elif tyc == float or tyc == int:
            content = self._add_data_num(content, new_value, to_list)
        elif tyc == bool:
            content = self._add_data_bool(content, new_value)
        elif tyc == None:
            content = self._add_data_none(content, new_value)

        file_content[content_locator] = content
        self.content = file_content

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

    @staticmethod
    def _add_data_dict(content, key, new_value):
        if key not in content:
            content[key] = new_value

        elif key in content:
            if type(content[key]) is list:
                content[key].append(new_value)
            else:
                content[key] = [content[key], new_value]
        return content

    @staticmethod
    def _add_data_list(content, new_value, index, inner_key, dict_index):
            content.insert(index, new_value)
            return content

    @staticmethod
    def _add_data_str(content, new_value, to_list):
        if type(new_value) is str and not to_list:
            content = content+f"\n " \
                                          f"{new_value}"
        else:
            content = [content, new_value]
        return content

    @staticmethod
    def _add_data_num(content, new_value, to_list=False):
        if type(new_value) in [int, float] and not to_list:
            content += new_value
        else:
            content = [content, new_value]
        return content

    @staticmethod
    def _add_data_bool(content, new_value):
        content = [content, new_value]
        return content

    @staticmethod
    def _add_data_none(content, new_value):
        content = new_value
        return content

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
