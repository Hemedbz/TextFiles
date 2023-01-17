# import unittest
import csv, json, os
#
# class Tests(unittest.TestCase):
#     def test_add(self):

#TODO: UNITESTS
file_path = 'D:\\Full_Stack_Python\\C10\\files\\example_2-Copy.json'

with open('D:\\Full_Stack_Python\\C10\\files\\example_2-Copy.json', 'r') as ph:
    content = json.load(ph)
print(content)


type_con = type(content)
type_con2 = type(content[0])
print(type_con)
print(type_con2)
print('Age' in content[0])
print(type_con is list)

def _add_data_dict(new_value, key):
    if key is None:
        raise Exception()
    if key not in content:
        content[key] = new_value
    elif key in content:
        if type(content[key]) is list:
            content[key].append(new_value)
        else:
            content[key] = [content[key], new_value]

def _add_data_dict_in_list(new_value, key, content_in_list):
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

def _add_data_list(new_value, key):
    key_in_val_flag = False
    for inx, val in enumerate(content):
        if type(val) is dict:
            if key in val:
                key_in_val_flag = True
                content[inx] = _add_data_dict_in_list(new_value, key, val)
    if not key_in_val_flag:
        content.append(new_value)


def _add_data_str(new_value, create_list):
    global content
    if type(new_value) is str and not create_list:
        content = content + f"\n " \
                            f"{new_value}"
    else:
        content = [content, new_value]


def _add_data_num(new_value, create_list):
    global content
    if type(new_value) in [int, float] and not create_list:
        content += new_value
    else:
        content = [content, new_value]


def _add_data_bool(new_value):
    global content
    content = [content, new_value]


def _add_data_none(new_value):
    content = new_value

def _dump_content():
    with open(file_path, 'w') as fd:
        json.dump(content, fd)


def add_data(new_value, key=None, create_list=False):
    # self.get_content()
    global type_con

    if type_con is dict:
        _add_data_dict(new_value, key)
    elif type_con is list:
        _add_data_list(new_value, key)
    elif type_con is int:
        _add_data_num(new_value, create_list)
    elif type_con is float:
        _add_data_num(new_value, create_list)
    elif type_con is str:
        _add_data_str(new_value, create_list)
    elif type_con is bool:
        _add_data_bool(new_value)
    elif type_con is None:
        _add_data_none(new_value)

    _dump_content()


add_data('hello', 'Login')