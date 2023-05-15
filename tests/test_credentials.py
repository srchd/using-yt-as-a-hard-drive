from mock import MagicMock
import unittest
from pathlib import Path
import logging
import shutil
import os

import google

from youtube import DataStorage, Credentials


class CredentialMock:
    def __init__(self):
        self.json = "{}"

    def to_json(self):
        return self.json


class TestCredentials(unittest.TestCase):
    @staticmethod
    def __create_credentials_from_original_file_mock(path: str, port: int = 8090):
        return CredentialMock()

    @staticmethod
    def __create_credentials_from_generated_file(path: str):
        return CredentialMock()

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

        DataStorage.HERE = Path(__file__).parent
        DataStorage.CREDENTIALS_FOLDER = DataStorage.HERE / "working_directory"
        DataStorage.GENERATED_FOLDER = DataStorage.CREDENTIALS_FOLDER / "generated"

        DataStorage.CREDENTIALS_FOLDER.mkdir(exist_ok=True)
        DataStorage.GENERATED_FOLDER.mkdir(exist_ok=True)

        Credentials._Credentials__create_credentials_from_original_file = MagicMock()
        Credentials._Credentials__create_credentials_from_original_file.side_effect = self.__create_credentials_from_original_file_mock
        Credentials._Credentials__create_credentials_from_generated_file = MagicMock()
        Credentials._Credentials__create_credentials_from_generated_file.side_effect = self.__create_credentials_from_generated_file

    def tearDown(self) -> None:
        shutil.rmtree(str(DataStorage.GENERATED_FOLDER))
        shutil.rmtree(str(DataStorage.CREDENTIALS_FOLDER))


class TestNoCredentials(TestCredentials):
    def setUp(self) -> None:
        super().setUp()
        self.credentials = Credentials()

        self.assertFalse(self.credentials._Credentials__create_credentials_from_original_file.called)
        self.assertFalse(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_init(self):
        self.assertEqual(0, self.credentials.current_credential_index)
        self.assertEqual(0, self.credentials.credential_count)
        self.assertListEqual([], self.credentials.credential_indices)

    def test_get_current_credentials(self):
        self.assertRaises(IndexError, self.credentials.get_current_credentials)

    def test_switch_credentials(self):
        self.credentials.switch_credentials()
        self.assertEqual(0, self.credentials.current_credential_index)


class TestOneNewCredential(TestCredentials):
    def setUp(self) -> None:
        super().setUp()

        self.file_path = str(DataStorage.CREDENTIALS_FOLDER / "asd.json")
        self.file_content = "asd"
        DataStorage.write_file_content(self.file_path, self.file_content)

        self.credentials = Credentials()

        self.assertTrue(self.credentials._Credentials__create_credentials_from_original_file.called)
        self.assertEqual(1, self.credentials._Credentials__create_credentials_from_original_file.call_count)
        self.assertFalse(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_init(self):
        self.assertEqual(0, self.credentials.current_credential_index)
        self.assertEqual(1, self.credentials.credential_count)
        self.assertListEqual([0], self.credentials.credential_indices)

        self.assertTrue(os.path.exists(self.file_path))
        self.assertEqual(self.file_content, DataStorage.read_file_content(self.file_path))

    def test_get_current_credentials(self):
        self.assertIsInstance(self.credentials.get_current_credentials(), CredentialMock)
        self.assertTrue(self.credentials._Credentials__create_credentials_from_generated_file.called)
        self.assertEqual(1, self.credentials._Credentials__create_credentials_from_generated_file.call_count)

    def test_switch_credentials(self):
        self.credentials.switch_credentials()
        self.assertEqual(0, self.credentials.current_credential_index)


class TestMultipleCredentials(TestCredentials):
    def setUp(self) -> None:
        super().setUp()

        self.file_path = str(DataStorage.CREDENTIALS_FOLDER / "asd.json")
        self.file_content = "asd"
        DataStorage.write_file_content(self.file_path, self.file_content)

        self.file_path2 = str(DataStorage.CREDENTIALS_FOLDER / "asd2.json")
        self.file_content2 = "asd"
        DataStorage.write_file_content(self.file_path2, self.file_content2)

        self.credentials = Credentials()

        self.assertTrue(self.credentials._Credentials__create_credentials_from_original_file.called)
        self.assertEqual(2, self.credentials._Credentials__create_credentials_from_original_file.call_count)
        self.assertFalse(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_init(self):
        self.assertEqual(0, self.credentials.current_credential_index)
        self.assertEqual(2, self.credentials.credential_count)
        self.assertListEqual([0, 1], self.credentials.credential_indices)

        self.assertTrue(os.path.exists(self.file_path))
        self.assertEqual(self.file_content, DataStorage.read_file_content(self.file_path))
        self.assertTrue(os.path.exists(self.file_path2))
        self.assertEqual(self.file_content2, DataStorage.read_file_content(self.file_path2))

    def test_get_current_credentials(self):
        self.assertIsInstance(self.credentials.get_current_credentials(), CredentialMock)
        self.assertTrue(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_switch_credentials(self):
        self.credentials.switch_credentials()
        self.assertEqual(1, self.credentials.current_credential_index)


class TestCopiedCredentialsExist(TestCredentials):
    def setUp(self) -> None:
        super().setUp()

        self.file_path = str(DataStorage.CREDENTIALS_FOLDER / "asd.json")
        self.file_content = "asd"
        DataStorage.write_file_content(self.file_path, self.file_content)

        self.file_path2 = str(DataStorage.CREDENTIALS_FOLDER / "asd2.json")
        self.file_content2 = "asd"
        DataStorage.write_file_content(self.file_path2, self.file_content2)

        self.copied_file_path = str(DataStorage.GENERATED_FOLDER / "copied_credentials_asd_0.json")
        self.copied_file_content = "asd"
        DataStorage.write_file_content(self.copied_file_path, self.copied_file_content)

        self.copied_file_path2 = str(DataStorage.GENERATED_FOLDER / "copied_credentials_asd2_1.json")
        self.copied_file_content2 = "asd"
        DataStorage.write_file_content(self.copied_file_path2, self.copied_file_content2)

        self.credentials = Credentials()

        self.assertTrue(self.credentials._Credentials__create_credentials_from_original_file.called)
        self.assertEqual(2, self.credentials._Credentials__create_credentials_from_original_file.call_count)
        self.assertFalse(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_init(self):
        self.assertEqual(0, self.credentials.current_credential_index)
        self.assertEqual(2, self.credentials.credential_count)
        self.assertListEqual([0, 1], self.credentials.credential_indices)

        self.assertTrue(os.path.exists(self.file_path))
        self.assertEqual(self.file_content, DataStorage.read_file_content(self.file_path))
        self.assertTrue(os.path.exists(self.file_path2))
        self.assertEqual(self.file_content2, DataStorage.read_file_content(self.file_path2))

    def test_get_current_credentials(self):
        self.assertIsInstance(self.credentials.get_current_credentials(), CredentialMock)
        self.assertTrue(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_switch_credentials(self):
        self.credentials.switch_credentials()
        self.assertEqual(1, self.credentials.current_credential_index)


class TestNoNewCredentials(TestCredentials):
    def setUp(self) -> None:
        super().setUp()

        self.file_path = str(DataStorage.CREDENTIALS_FOLDER / "asd.json")
        self.file_content = "asd"
        DataStorage.write_file_content(self.file_path, self.file_content)

        self.file_path2 = str(DataStorage.CREDENTIALS_FOLDER / "asd2.json")
        self.file_content2 = "asd"
        DataStorage.write_file_content(self.file_path2, self.file_content2)

        self.copied_file_path = str(DataStorage.GENERATED_FOLDER / "copied_credentials_asd_0.json")
        self.copied_file_content = "asd"
        DataStorage.write_file_content(self.copied_file_path, self.copied_file_content)

        self.copied_file_path2 = str(DataStorage.GENERATED_FOLDER / "copied_credentials_asd2_1.json")
        self.copied_file_content2 = "asd"
        DataStorage.write_file_content(self.copied_file_path2, self.copied_file_content2)

        self.generated_file_path = str(DataStorage.GENERATED_FOLDER / "generated_credentials_asd_0.json")
        self.generated_file_content = "asd"
        DataStorage.write_file_content(self.generated_file_path, self.generated_file_content)

        self.generated_file_path2 = str(DataStorage.GENERATED_FOLDER / "generated_credentials_asd2_1.json")
        self.generated_file_content2 = "asd"
        DataStorage.write_file_content(self.generated_file_path2, self.generated_file_content2)

        self.credentials = Credentials()

        self.assertFalse(self.credentials._Credentials__create_credentials_from_original_file.called)
        self.assertFalse(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_init(self):
        self.assertEqual(0, self.credentials.current_credential_index)
        self.assertEqual(2, self.credentials.credential_count)
        self.assertListEqual([0, 1], self.credentials.credential_indices)

        self.assertTrue(os.path.exists(self.file_path))
        self.assertEqual(self.file_content, DataStorage.read_file_content(self.file_path))
        self.assertTrue(os.path.exists(self.file_path2))
        self.assertEqual(self.file_content2, DataStorage.read_file_content(self.file_path2))

    def test_get_current_credentials(self):
        self.assertIsInstance(self.credentials.get_current_credentials(), CredentialMock)
        self.assertTrue(self.credentials._Credentials__create_credentials_from_generated_file.called)

    def test_switch_credentials(self):
        self.credentials.switch_credentials()
        self.assertEqual(1, self.credentials.current_credential_index)
