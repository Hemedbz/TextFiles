import unittest


class TestTextFile(unittest.TestCase):
    def setUp(self):
        # Create a sample file to use in the tests
        self.file_path = 'sample.txt'
        with open(self.file_path, 'w') as f:
            f.write('sample content')

    def test_get_content(self):
        # Test the get_content method
        t = TextFile(self.file_path)
        self.assertEqual(t.get_content(), 'sample content')

    def test_file_path(self):
        # Test the file_path property
        t = TextFile(self.file_path)
        self.assertEqual(t.file_path, self.file_path)

    def test_file_not_found(self):
        # Test the FileNotFoundError exception
        with self.assertRaises(FileNotFoundError):
            t = TextFile('not_existing.txt')

    def test_type_error(self):
        # Test the TypeError exception
        with self.assertRaises(TypeError):
            t = TextFile(self.file_path)
            t._ext = lambda: 'not_txt'
            t.get_content()


if __name__ == '__main__':
    unittest.main()
