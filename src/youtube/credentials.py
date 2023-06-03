import traceback
from pathlib import Path
import os
from typing import Tuple
import logging
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials
import oauthlib.oauth2.rfc6749.errors
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

		if not DataStorage.CREDENTIALS_FOLDER.exists():
			DataStorage.CREDENTIALS_FOLDER.mkdir(exist_ok=True)
		if not DataStorage.GENERATED_FOLDER.exists():
			DataStorage.GENERATED_FOLDER.mkdir(exist_ok=True)

	@staticmethod
	def get_file_name_from_path(path: str) -> str:
		return path.split("/")[-1].split("\\")[-1]

	@staticmethod
	def get_index_from_file_name(file_name: str) -> int:
		_, file_index = file_name.replace(".json", "").split("_")[-2:]
		file_index = int(file_index)
		return file_index

	@staticmethod
	def get_original_file_name_from_file_name(file_name: str) -> str:
		original_file_name, _ = file_name.replace(".json", "").split("_")[-2:]
		return original_file_name

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

	def __init__(self, force_renew: bool = False):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.logger.setLevel(logging.DEBUG)
		sh = logging.StreamHandler(stream=sys.stdout)
		formatter = logging.Formatter(YTHDSettings.LOG_FORMAT)
		sh.setFormatter(formatter)
		self.logger.addHandler(sh)

		self.force_renew = force_renew

		self.current_credential_index = 0
		self.credential_indices = []
		self.credential_count = 0

		self.data_storage = DataStorage()

		self.logger.info("Created Credentials")

		self.logger.info("Getting already copied credential files")
		copied_files_dict, max_file_index = self.__get_copied_credentials()
		copied_file_contents = set(copied_files_dict.values())

		self.logger.info("Checking for new credential files")
		credential_files_dict = self.__get_original_credentials()
		self.logger.info("Copying new credential files")
		new_copied_files_dict, max_file_index = self.__copy_credentials(credential_files_dict, max_file_index, copied_file_contents)
		copied_files_dict = copied_files_dict | new_copied_files_dict

		self.logger.info("Generating credential files")
		self.credential_indices = self.__generate_credentials(copied_files_dict)
		self.credential_count = len(self.credential_indices)

	def __get_copied_credentials(self) -> Tuple[dict, int]:
		copied_files = self.data_storage.list_copied_files()
		copied_files_dict = {}
		max_file_index = -1
		for path in copied_files:
			file_name = self.data_storage.get_file_name_from_path(path)
			file_content = self.data_storage.read_file_content(path)
			copied_files_dict[path] = file_content

			file_index = self.data_storage.get_index_from_file_name(file_name)
			if file_index > max_file_index:
				max_file_index = file_index

		self.logger.info(f"Already copied credential files: {max_file_index+1}")
		return copied_files_dict, max_file_index

	def __get_original_credentials(self) -> dict:
		credential_files = self.data_storage.list_credential_files()
		credential_files_dict = {}
		for path in credential_files:
			file_content = self.data_storage.read_file_content(path)
			credential_files_dict[path] = file_content

		self.logger.info(f"Original credential files: {len(credential_files)}")
		return credential_files_dict

	def __copy_credentials(self, credential_files_dict: dict, max_file_index: int, copied_file_contents: set[str]) -> Tuple[dict, int]:
		copied_files_dict = {}
		for path in credential_files_dict.keys():
			file_name = self.data_storage.get_file_name_from_path(path).replace("_", "-")
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

	def __generate_credentials(self, copied_files_dict: dict):
		copied_files_keys = sorted(copied_files_dict.keys(), key=lambda p: self.data_storage.get_index_from_file_name(self.data_storage.get_file_name_from_path(p)))
		possible_generated_files_dict = {f.replace(self.data_storage.COPIED_CREDENTIALS_SELECTOR, self.data_storage.GENERATED_CREDENTIALS_SELECTOR): f for f in copied_files_keys}
		count = 0
		credential_indices = []
		for path in possible_generated_files_dict.keys():
			file_name = self.data_storage.get_file_name_from_path(path)
			file_index = self.data_storage.get_index_from_file_name(file_name)

			generated_file_path = path
			copied_file_path = possible_generated_files_dict[path]
			if not self.force_renew and os.path.isfile(generated_file_path):
				credential_indices.append(file_index)
			else:
				retries = 10
				while retries > 0:
					try:
						credentials = Credentials.__create_credentials_from_original_file(copied_file_path, 8090 + count + (10 - retries))
						self.data_storage.write_file_content(generated_file_path, credentials.to_json())
					except oauthlib.oauth2.rfc6749.errors.MismatchingStateError:
						self.logger.warning(f"Couldn't generate credential file {file_name}, retrying")
						retries -= 1
					except Exception:
						self.logger.error(f"Couldn't generate credential file {file_name}")
						self.logger.error(traceback.format_exc())
						retries = 0
					else:
						count += 1
						retries = 0
						credential_indices.append(file_index)

		self.logger.info(f"Newly generated credential files: {count}")
		return credential_indices

	def __get_generated_credentials(self) -> list[str]:
		credential_list = self.data_storage.list_generated_files()
		credential_list = sorted(credential_list, key=lambda path: self.data_storage.get_index_from_file_name(self.data_storage.get_file_name_from_path(path)))
		return credential_list

	@staticmethod
	def __create_credentials_from_original_file(path: str, port: int = 8090) -> google.oauth2.credentials:
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(path, ApiParameters.SCOPES)
		credentials = flow.run_local_server(port=port)
		return credentials

	@staticmethod
	def __create_credentials_from_generated_file(path: str) -> google.oauth2.credentials:
		return google.oauth2.credentials.Credentials.from_authorized_user_file(path)

	def get_current_credentials(self) -> google.oauth2.credentials:
		credential_list = self.__get_generated_credentials()
		current_credential_file = credential_list[self.current_credential_index]
		return Credentials.__create_credentials_from_generated_file(current_credential_file)

	def switch_credentials(self):
		self.logger.info("Switching credentials")
		self.current_credential_index += 1
		if self.current_credential_index >= self.credential_count:
			self.logger.info("Looped back to credential 0")
			self.current_credential_index = 0
