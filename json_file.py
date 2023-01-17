from text_file_parent import TextFile
import json
import re


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
        match self.type:
            case 'dict':
                self._search_dict(param, dictionary=self.content)
            case 'list':
                self._search_list(param, l=self.content)
            case 'int':
                self._search_identical(param)
            case 'float':
                self._search_identical(param)
            case 'str':
                self._search_str(param)
            case 'bool':
                self._search_identical(param)
            case 'None':
                self._search_identical(param)

    def add_data(self, new_value, key=None):
        self.get_content()

        match self.type:
            case 'dict':
                self._add_data_dict(key, new_value)
            case 'list':
                self._add_data_list(new_value)
            case 'int':
                self._add_data_num(new_value)
            case 'float':
                self._add_data_num(new_value)
            case 'str':
                self._add_data_str(new_value)
            case 'bool':
                self._add_data_bool(new_value)
            case 'None':
                self._add_data_none(new_value)

        self._dump_content()

    def _dump_content(self):
        with open(self._file_path, 'w') as fd:
            json.dump(self.content, fd)

    def count(self, val):
        return len(self.search(val))

    def delete_data(self, data):
        pass #TODO:

    # sub functions by json type

    def _add_data_dict(self, key, new_value):
        if key not in self.content:
            self.content[key] = new_value
        elif key in self.content:
            if type(self.content[key]) == 'list':
                self.content[key].append(new_value)
            else:
                self.content[key] = [self.content[key], new_value]

    def _add_data_list(self, new_value):
        self.content.append(new_value)

    def _add_data_str(self, new_value):
        if type(new_value) == 'str':
            self._content = self._content+f"\n" \
                                    f"{new_value}"
        else:
            self._content = [self._content, new_value]

    def _add_data_num(self, new_value):
        if type(new_value) in ['int', 'float']:
            self._content += new_value
        else:
            self._content = [self._content, new_value]

    def _add_data_bool(self, new_value):
        self._content = [self._content, new_value]

    def _add_data_none(self, new_value):
        self._content = new_value

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
