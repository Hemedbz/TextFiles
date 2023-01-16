# import unittest
import csv, json, os
#
# class Tests(unittest.TestCase):
#     def test_add(self):

#TODO: UNITESTS

# with open('D:\\Full_Stack_Python\\C10\\files\\text-Copy.csv', 'r') as cv:
#     f = csv.reader(cv, delimiter=';')
#     print(f)
#     for row in f:
#         print(row)
#
#
# with open('D:\\Full_Stack_Python\\C10\\files\\text-Copy.csv', 'r') as cv:
#     f = csv.DictReader(cv, delimiter=';')
#     print(f)
#     for row in f:
#         print(row)
#
#
li = []
with open('D:\\Full_Stack_Python\\C10\\files\\text_4.csv', 'r') as cv:
    f = csv.reader(cv, delimiter=',')
    print(f)
    for row in f:
        li.append(row)
print(li)

l = []
with open('D:\\Full_Stack_Python\\C10\\files\\text_4.csv', 'r') as cv:
    f = csv.DictReader(cv, delimiter=',')
    print(f)
    for row in f:
        l.append(row)
print(l)


# def get_headers(content, header):
#     if header:
#         for row in content:
#             return row
#     return None
#
# if __name__ == '__main__':
#     with open('D:\\Full_Stack_Python\\C10\\files\\text_4.csv', 'r') as cv:
#         f = csv.reader(cv, delimiter=',')
#         # print(f)
#         # for row in f:
#         #     print(row)
#
#         print(get_headers(f, None))



#get con:
#   grt reder->N()
#   get D->T()