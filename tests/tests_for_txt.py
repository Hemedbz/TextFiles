import unittest
from old_ignore.src.txt_file import TxtFile


class TestTxtFile(unittest.TestCase):
    def setUp(self):
        # Create a sample file to use in the tests
        self.file_path = 'sample.txt'
        with open(self.file_path, 'w') as f:
            f.write('sample content')

    def test_words(self):
        # Test the words property
        t = TxtFile(self.file_path)
        self.assertEqual(t.words, ['sample', 'content'])

    def test_add(self):
        # Test the __add__ method
        t1 = TxtFile(self.file_path)
        t2 = TxtFile(self.file_path)
        t3 = t1 + t2
        self.assertEqual(t3.content, 'sample content')

    def tearDown(self):
        # Delete the sample file after the tests are done
        os.remove(self.file_path)



if __name__ == '__main__':
    unittest.main()
