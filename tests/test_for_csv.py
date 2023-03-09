# class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

#
# if __name__ == '__main__':
#     unittest.main()

# with open ("/home/hemed/Desktop/fullstack_course/SQL/lesson_19_Jan_15th/imdb.csv", "r") as fh:
#     content = list(csv.reader(fh))
#     to_delete = content[223]
#     print(to_delete)
#     content.remove(to_delete)
#     print(content[223])

# with open("/home/hemed/Desktop/fullstack_course/SQL/lesson_19_Jan_15th/imdb.csv", "w") as fh:
#     writer = csv.writer(fh)
#     writer.writerows(content)

from old_ignore.largecsvfile import LargeCsvFile

file = LargeCsvFile("/home/hemed/Desktop/fullstack_course/SQL/lesson_19_Jan_15th/imdb.csv")
# for row in file.content:
#     print(row)
# print(file.search("8"))

print(file._file_size)


