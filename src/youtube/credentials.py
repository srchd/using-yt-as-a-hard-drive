from pathlib import Path
import os
from typing import Tuple
import logging
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from .youtube_client_parameters import ApiParameters, YTHDSettings


class DataStorage:

	HERE: Path = Path(__file__).parent
	CREDENTIALS_FOLDER: Path = HERE / "credentials"
	GENERATED_FOLDER: Path = CREDENTIALS_FOLDER / "generated"

	COMMON_CREDENTIALS_FILE_SUFFIX = "{original_file_name}_{file_index}.json"
	GENERATED_CREDENTIALS_SELECTOR: str = "generated_credentials"
	GENERATED_CREDENTIALS_FILE_BASE: str = GENERATED_CREDENTIALS_SELECTOR + "_" + COMMON_CREDENTIALS_FILE_SUFFIX
	COPIED_CREDENTIALS_SELECTOR: str = "copied_credentials"
	COPIED_CREDENTIALS_FILE_BASE: str = COPIED_CREDENTIALS_SELECTOR + "_" + COMMON_CREDENTIALS_FILE_SUFFIX

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.setLevel(logging.DEBUG)
		sh = logging.StreamHandler(stream=sys.stdout)
		formatter = logging.Formatter(YTHDSettings.LOG_FORMAT)
		sh.setFormatter(formatter)
		self.logger.addHandler(sh)

		self.logger.info("Created DataStorage")

	@staticmethod
	def get_file_name_from_path(path: str) -> str:
		return path.split("/")[-1].split("\\")[-1]

	@staticmethod
	def list_credential_files() -> list[str]:
		files = os.listdir(DataStorage.CREDENTIALS_FOLDER)
		secrets = [str(DataStorage.CREDENTIALS_FOLDER / f) for f in files if f.endswith(".json")]
		secrets.sort()
		return secrets

	@staticmethod
	def list_copied_files() -> list[str]:
		files = os.listdir(DataStorage.GENERATED_FOLDER)
		secrets = [str(DataStorage.GENERATED_FOLDER / f) for f in files if f.endswith(".json") and DataStorage.COPIED_CREDENTIALS_SELECTOR in f]
		secrets.sort()
		return secrets

	@staticmethod
	def list_generated_files() -> list[str]:
		files = os.listdir(DataStorage.GENERATED_FOLDER)
		secrets = [str(DataStorage.GENERATED_FOLDER / f) for f in files if f.endswith(".json") and DataStorage.GENERATED_CREDENTIALS_SELECTOR in f]
		secrets.sort()
		return secrets

	@staticmethod
	def read_file_content(path: str) -> str:
		with open(path, "r") as f:
			file_content = f.read()
		return file_content

	@staticmethod
	def write_file_content(path: str, file_content: str):
		with open(path, "w") as f:
			f.write(file_content)


class Credentials:

	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.setLevel(logging.DEBUG)
		sh = logging.StreamHandler(stream=sys.stdout)
		formatter = logging.Formatter(YTHDSettings.LOG_FORMAT)
		sh.setFormatter(formatter)
		self.logger.addHandler(sh)

		self.file_index = 0
		self.data_storage = DataStorage()

		self.logger.info("Created Credentials")

		self.logger.info("Getting already copied credential files")
		copied_files_dict, max_file_index = self.get_copied_credential_files()
		copied_file_contents = set(copied_files_dict.values())

		self.logger.info("Checking for new credential files")
		credential_files_dict = self.get_original_credential_files()
		self.logger.info("Copying new credential files")
		new_copied_files_dict, max_file_index = self.copy_credential_files(credential_files_dict, max_file_index, copied_file_contents)
		copied_files_dict = copied_files_dict | new_copied_files_dict

		self.logger.info("Generating credential files")
		self.generate_credential_files(copied_files_dict)

	def get_copied_credential_files(self) -> Tuple[dict, int]:
		copied_files = self.data_storage.list_copied_files()
		copied_files_dict = {}
		max_file_index = -1
		for path in copied_files:
			file_name = self.data_storage.get_file_name_from_path(path)
			file_content = self.data_storage.read_file_content(path)
			copied_files_dict[path] = file_content

			original_file_name, file_index = file_name.replace(".json", "").split("_")[-2:]
			file_index = int(file_index)
			if file_index > max_file_index:
				max_file_index = file_index

		self.logger.info(f"Already copied credential files: {max_file_index+1}")
		return copied_files_dict, max_file_index

	def get_original_credential_files(self) -> dict:
		credential_files = self.data_storage.list_credential_files()
		credential_files_dict = {}
		for path in credential_files:
			file_content = self.data_storage.read_file_content(path)
			credential_files_dict[path] = file_content

		self.logger.info(f"Original credential files: {len(credential_files)}")
		return credential_files_dict

	def copy_credential_files(self, credential_files_dict: dict, max_file_index: int, copied_file_contents: set[str]) -> Tuple[dict, int]:
		copied_files_dict = {}
		for path in credential_files_dict.keys():
			file_name = self.data_storage.get_file_name_from_path(path)
			file_content = self.data_storage.read_file_content(path)

			# if new file, copy it
			if file_content not in copied_file_contents:
				max_file_index += 1
				new_file_name = self.data_storage.COPIED_CREDENTIALS_FILE_BASE.format(original_file_name=file_name.replace(".json", ""), file_index=max_file_index)
				new_file_path = str(self.data_storage.GENERATED_FOLDER / new_file_name)
				self.data_storage.write_file_content(new_file_path, file_content)
				copied_files_dict[new_file_path] = file_content

		self.logger.info(f"Newly copied credential files: {len(copied_files_dict)}. New largest index: {max_file_index}")
		return copied_files_dict, max_file_index

	def generate_credential_files(self, copied_files_dict: dict):
		possible_generated_files_dict = {f.replace(self.data_storage.COPIED_CREDENTIALS_SELECTOR, self.data_storage.GENERATED_CREDENTIALS_SELECTOR): f for f in copied_files_dict.keys()}
		count = 0
		for path in possible_generated_files_dict.keys():
			generated_file_path = path
			copied_file_path = possible_generated_files_dict[path]
			if not os.path.isfile(generated_file_path):
				flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(copied_file_path, ApiParameters.SCOPES)
				credentials = flow.run_local_server(port=8090)
				self.data_storage.write_file_content(generated_file_path, credentials.to_json())
				count += 1
		self.logger.info(f"Newly generated credential files: {count}")

	def get_generated_file(self) -> google.oauth2.credentials:
		return google.oauth2.credentials.Credentials.from_authorized_user_file(self.data_storage.list_generated_files()[0])

	def switch_credentials(self):
		pass
