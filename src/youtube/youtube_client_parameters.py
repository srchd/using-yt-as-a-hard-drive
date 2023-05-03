from __future__ import annotations
import http.client
import httplib2
from typing import Union


class ApiParameters:
	SCOPES = [
		"https://www.googleapis.com/auth/youtube",
		"https://www.googleapis.com/auth/youtube.force-ssl",
		"https://www.googleapis.com/auth/youtube.readonly",
		"https://www.googleapis.com/auth/youtubepartner",
		"https://www.googleapis.com/auth/youtubepartner-channel-audit"
	]

	MAX_RETRIES = 10

	RETRIABLE_EXCEPTIONS = [
		httplib2.HttpLib2Error, IOError, http.client.NotConnected,
		http.client.IncompleteRead, http.client.ImproperConnectionState,
		http.client.CannotSendRequest, http.client.CannotSendHeader,
		http.client.ResponseNotReady, http.client.BadStatusLine
	]

	RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

	VALID_PRIVACY_STATUSES = ["public", "private", "unlisted"]

	API_SERVICE_NAME = "youtube"
	API_VERSION = "v3"

class YTHDSettings:
	PATH_PREFIX = "Path: "
	YTHD_MARK = "#ythd"
	DELETED_MARK = "#deleted"

class Credentials:
	ORIGINAL_CLIENT_SECRETS_FILE = "youtube/credentials/credentials.json"
	GENERATED_CLIENT_SECRETS_FILE = "youtube/credentials/user_file.json"

class Path:
	def __init__(self, name, parent=None):
		self.name = name
		self.parent = parent

	@staticmethod
	def __str_with_circle_break(path: Path, ids=None):
		if ids is None:
			ids = set()
		if id(path) in ids:
			return ""
		else:
			ids.add(id(path))
			path_str = "" if path.parent is None else Path.__str_with_circle_break(path.parent, ids)
			if len(path_str) < 1 or path_str[-1] != "/":
				path_str += "/"
			path_str += path.name
			return path_str

	def __str__(self):
		if self.parent is None and not self.name:
			return ""
		else:
			return self.__str_with_circle_break(self, ids=None)

	def __repr__(self):
		return self.__str__()

	@staticmethod
	def string_to_path(string: str) -> Union[Path, None]:
		strings = string.strip().split("/")
		path = None
		for string in strings:
			if string:
				path = Path(name=string, parent=path)
		return path

	@staticmethod
	def description_to_path(description: str) -> Union[Path, None]:
		lines = description.split("\n")
		for line in lines:
			if line.startswith(YTHDSettings.PATH_PREFIX):
				return Path.string_to_path(string=line.replace(YTHDSettings.PATH_PREFIX, ""))
		return None
