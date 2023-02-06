from pprint import pprint

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

    def add_data(self, content_locator, new_index, new_value, to_list=False):
        file_content = self.content()
        self.lock()
        content = content[content_locator]
        tyc = type(content)
        if tyc == dict:
            content = self._add_data_dict(content, new_index, new_value)
        elif tyc == list:
            content = self._add_data_list(content, new_value, new_index)
        elif tyc == str:
            content = self._add_data_str(content, new_value, to_list)
        elif tyc ==  float or tyc == int:
            content = self._add_data_num(content, new_value, to_list)
        elif tyc == bool:
            content = self._add_data_bool(content, new_value)
        elif tyc == None:
            content = self._add_data_none(content, new_value)

        file_content[content_locator] = content
        self.content = file_content

        self._dump_content()
        self.lock.release()



    # def add_data(self, new_value, key=None, index=-1, inner_key=None, dict_index=None, to_list=False):
    #
    #     self.get_content()
    #     self.lock.acquire()
    #
    #     if self.type is dict:
    #         self._add_data_dict(key, new_value)
    #     elif self.type is list:
    #         self._add_data_list(new_value, index, inner_key, dict_index)
    #     elif self.type is int:
    #         self._add_data_num(new_value, to_list)
    #     elif self.type is float:
    #         self._add_data_num(new_value, to_list)
    #     elif self.type is str:
    #         self._add_data_str(new_value, to_list)
    #     elif self.type is bool:
    #         self._add_data_bool(new_value)
    #     elif self.type is None:
    #         self._add_data_none(new_value)
    #
    #     self._dump_content()
    #     self.lock.release()

    # def _delete_from_list(self, value, key, index, content: list):
    #     if index is None:
    #         raise Exception() # -> cant delete from list without index
    #
    #     delete_inx = False
    #
    #     for inx, val in enumerate(content):
    #         if inx == index:
    #             if key is not None and type(val) == dict:
    #                 val = self._delete_from_dict(my_key=key, content=val, name_func='_delete_from_list')
    #             elif key is not None and type(val) != dict:
    #                 raise Exception() # -> When we are in the requested place in the list and the user entered KEY but there is no dictionary inside
    #             else:
    #                 delete_inx = True
    #
    #     if delete_inx:
    #         self.content.pop(index)


    def remove_data(self, content_locator: str, key: str | int = None, index: int = None): #TODO: H
        """
        removes specific data from json for type -> list, dict only

        """
        self.lock.acquire()
        if key is not None:
            if not re.findall(f"{key}']$", content_locator):
                raise Exception() # -> The key does not match the end of the string TODO: exception
        elif index is not None:
            if not re.findall(f"{index}]$", content_locator):
                raise Exception() # -> The index does not match the end of the string
        elif key is None and index is None:
            raise Exception()

        exec(f"del self.content{content_locator}")
        self._dump_content()
        self.lock.release()




        # if self.type == list:
        #     self._delete_from_list()
        # elif self.type == dict:
        #     self._delete_from_dict()


    #     if self.count(data) > 1:
    #         raise Exception #tell user data appears more than once, can do manually or remove all
    #
    #     self.lock.acquire()
    #     self.content()
    #
    #     if self.type == list:
    #         for item in self.content:
    #             if item == data:
    #                 self.content.remove(data)
    #             elif data in item:
    #                 raise Exception #tell user data is tied into other data and should be removed manually
    #     elif self.type == dict:
    #         for key, value in self.content:
    #             if key == data:
    #                 del self.content[key]
    #             elif value == data:
    #                 self.content[key] = None
    #             elif data in value:
    #                 self.content.value.remove(data)
    #
    #
    #     self._dump_content()
    #     self.lock.release()
    #     return self.content()
    #
    # # sub functions by json type

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
        for index, val in enumerate(given_list):
            if val == value:
                findings.append((index, val))
            elif isinstance(val, dict):
                findings.append(self._search_dict(value, val))
            elif isinstance(val, list):
                findings.extend(self._search_list(value, val))
        return findings

    def _search_identical(self, value):
        if value == self.content:
            return self.content
        else:
            return None

    def _search_str(self, value):
        return re.findall(value, self.content)

if __name__ == '__main__':
    my_json = JsonFile('D:\\Full_Stack_Python\\C10\\files\\example_2-Copy-Copy.json')
    # print(my_json.type)
    pprint(my_json.content)
    # print(my_json.search('Age'))
    # my_json.remove_data("[0]['ParentsNames'][0][0][1]", index=1)
    # for key in my_json:
    #     print(key)

    # with open('D:\\Full_Stack_Python\\C10\\files\\example_2-Copy-Copy.json', 'r') as js:
    #     j = json.load(js)
    #
    #     print(j)
    #
    # # exec(f"content = j[0]['Name']")
    # # print(content)
    # exec(f"content = j[0]['ParentsNames'][1]")
    # print(content)
    # # exec(f"del j[0]['Name']")
    # # print(j)
    # # exec(f"del j[0]['ParentsNames'][1]")
    # # print(j)
    #
    # with open('D:\\Full_Stack_Python\\C10\\files\\example_2-Copy-Copy.json', 'w') as js:
    #     json.dump(j, js)
