import unittest
import os
import json
from utils.read_write_file import ReadWriteFile  #


class TestReadWriteFile(unittest.TestCase):
    def setUp(self):
        self.file_path = "../test_data/test_file.txt"
        self.json_file_path = "../test_data/test_file.json"
        self.content = "Hello, World!"
        self.json_content = {"message": "Hello, World!"}

    def test_read_file(self):
        ReadWriteFile(self.file_path).write_file(self.content)
        self.assertEqual(ReadWriteFile(self.file_path).read_file(), self.content)

    def test_write_file(self):
        ReadWriteFile(self.file_path).write_file(self.content)
        with open(self.file_path, 'r') as f:
            self.assertEqual(f.read(), self.content)

    def test_append_to_file(self):
        ReadWriteFile(self.file_path).append_to_file(self.content)
        with open(self.file_path, 'r') as f:
            self.assertEqual(f.read(), self.content + self.content)

    def test_read_from_json_file(self):
        ReadWriteFile(self.json_file_path).write_to_json_file(self.json_content)
        self.assertEqual(ReadWriteFile(self.json_file_path).read_from_json_file(), self.json_content)

    def test_write_to_json_file(self):
        ReadWriteFile(self.json_file_path).write_to_json_file(self.json_content)
        with open(self.json_file_path, 'r') as f:
            self.assertEqual(json.load(f), self.json_content)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)


if __name__ == "__main__":
    unittest.main()
