from pathlib import Path
import os

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

from .youtube_client_parameters import ApiParameters

class Credentials:
	__HERE = Path(__file__).parent
	__CREDENTIALS_FOLDER = __HERE / "credentials"
	__GENERATED_FOLDER = __CREDENTIALS_FOLDER / "generated"

	ORIGINAL_CLIENT_SECRETS_FILE = str(__CREDENTIALS_FOLDER / "credentials.json")
	GENERATED_CLIENT_SECRETS_FILE = str(__GENERATED_FOLDER / "user_file.json")

	__USER_FILE_BASE = "user_file_{file_index}.json"

	@staticmethod
	def list_secret_files():
		files = os.listdir(Credentials.__CREDENTIALS_FOLDER)
		secrets = [str(Credentials.__CREDENTIALS_FOLDER / f) for f in files if f.endswith(".json")]
		return secrets

	def __init__(self):
		self.file_index = 0

	def advance_file_index(self):
		self.file_index += 1
		secret_count = len(Credentials.list_secret_files())
		if self.file_index > secret_count - 1:
			self.file_index = 0

	def get_generated_file(self):
		return google.oauth2.credentials.Credentials.from_authorized_user_file(str(Credentials.__GENERATED_FOLDER / Credentials.__USER_FILE_BASE.format(file_index=self.file_index)))

	def __get_flow(self):
		secrets = self.list_secret_files()
		return google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(secrets[self.file_index], ApiParameters.SCOPES)

	@staticmethod
	def __get_credentials_from_flow(flow: google_auth_oauthlib.flow) -> google.oauth2.credentials:
		return flow.run_local_server(port=8090)

	def __save_credentials(self, credentials: google.oauth2.credentials):
		with (Credentials.__GENERATED_FOLDER / Credentials.__USER_FILE_BASE.format(file_index=self.file_index)).open(mode="w") as f:
			f.write(credentials.to_json())

	def create_credentials(self) -> google.oauth2.credentials:
		flow = self.__get_flow()
		credentials = self.__get_credentials_from_flow(flow)
		self.__save_credentials(credentials)
		return credentials
