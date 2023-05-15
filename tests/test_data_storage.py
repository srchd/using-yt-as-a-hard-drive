import mock
import unittest
from pathlib import Path
import logging
import shutil
import os

from youtube import DataStorage


class TestDataStorage(unittest.TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

        DataStorage.HERE = Path(__file__).parent
        DataStorage.CREDENTIALS_FOLDER = DataStorage.HERE / "working_directory"
        DataStorage.GENERATED_FOLDER = DataStorage.CREDENTIALS_FOLDER / "generated"

        DataStorage.CREDENTIALS_FOLDER.mkdir(exist_ok=True)
        DataStorage.GENERATED_FOLDER.mkdir(exist_ok=True)

        self.data_storage = DataStorage()

    def tearDown(self) -> None:
        shutil.rmtree(str(DataStorage.GENERATED_FOLDER))
        shutil.rmtree(str(DataStorage.CREDENTIALS_FOLDER))


class TestStringFunctions(TestDataStorage):
    def test_get_file_name_from_path(self):
        self.assertEqual("asd", self.data_storage.get_file_name_from_path("asd"))
        self.assertEqual("asd", self.data_storage.get_file_name_from_path("/asd"))
        self.assertEqual("asd", self.data_storage.get_file_name_from_path("//asd"))
        self.assertEqual("asd", self.data_storage.get_file_name_from_path("\\"*1 + "asd"))
        self.assertEqual("asd", self.data_storage.get_file_name_from_path("\\"*2 + "asd"))

    def test_get_index_from_file_name(self):
        # wrong file name
        self.assertRaises(Exception, self.data_storage.get_index_from_file_name, "asd")
        # file name with index
        self.assertEqual(42, self.data_storage.get_index_from_file_name("asd_42"))
        # file name with index and extension
        self.assertEqual(42, self.data_storage.get_index_from_file_name("asd_42.json"))

    def test_get_original_file_name_from_file_name(self):
        # wrong file name
        self.assertRaises(Exception, self.data_storage.get_original_file_name_from_file_name, "asd")
        # file name with index
        self.assertEqual("asd", self.data_storage.get_original_file_name_from_file_name("asd_42"))
        # file name with index and extension
        self.assertEqual("asd", self.data_storage.get_original_file_name_from_file_name("asd_42.json"))


class TestNoFiles(TestDataStorage):
    def test_list_credential_files(self):
        self.assertListEqual([], self.data_storage.list_credential_files())

    def test_list_copied_files(self):
        self.assertListEqual([], self.data_storage.list_copied_files())

    def test_list_generated_files(self):
        self.assertListEqual([], self.data_storage.list_generated_files())

    def test_read_file_content(self):
        self.assertRaises(FileNotFoundError, self.data_storage.read_file_content, str(DataStorage.CREDENTIALS_FOLDER / "credentials") + ".json")

    def test_write_file_content(self):
        file_path = str(DataStorage.CREDENTIALS_FOLDER / "asd")
        file_content = "asd"
        self.data_storage.write_file_content(file_path, file_content)
        self.assertTrue(os.path.exists(file_path))


class TestWithFiles(TestDataStorage):
    def setUp(self) -> None:
        super().setUp()

        example_file_content = "asd"

        self.original_example_file_path = str(DataStorage.CREDENTIALS_FOLDER / "orig_asd_0.json")
        self.copied_example_file_path = str(DataStorage.GENERATED_FOLDER / "copied_credentials_asd_0.json")
        self.generated_example_file_path = str(DataStorage.GENERATED_FOLDER / "generated_credentials_asd_0.json")

        self.data_storage.write_file_content(self.original_example_file_path, example_file_content)
        self.data_storage.write_file_content(self.copied_example_file_path, example_file_content)
        self.data_storage.write_file_content(self.generated_example_file_path, example_file_content)

    def test_list_credential_files(self):
        self.assertListEqual([self.original_example_file_path], self.data_storage.list_credential_files())

    def test_list_copied_files(self):
        self.assertListEqual([self.copied_example_file_path], self.data_storage.list_copied_files())

    def test_list_generated_files(self):
        self.assertListEqual([self.generated_example_file_path], self.data_storage.list_generated_files())

    def test_read_file_content(self):
        self.assertRaises(FileNotFoundError, self.data_storage.read_file_content, str(DataStorage.CREDENTIALS_FOLDER / "credentials") + ".json")

    def test_write_file_content(self):
        file_path = self.copied_example_file_path
        file_content = "asd2"
        self.data_storage.write_file_content(file_path, file_content)
        self.assertTrue(os.path.exists(file_path))
        read_file_content = self.data_storage.read_file_content(file_path)
        self.assertEqual(file_content, read_file_content)
