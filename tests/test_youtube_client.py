from mock import MagicMock
import unittest
from pathlib import Path
import logging
import shutil
import os

import google

from youtube import DataStorage, Credentials
from youtube import YoutubeClient, YTHDSettings, ApiParameters


class CredentialMock:
    def __init__(self):
        self.json = "{}"

    def to_json(self):
        return self.json


class TestYoutubeClient(unittest.TestCase):
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

        YoutubeClient._YoutubeClient__test_client = MagicMock()
        YoutubeClient.get_build = MagicMock()


