import http.client
import httplib2

class ClientSettings:
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

class Credentials:
	ORIGINAL_CLIENT_SECRETS_FILE = "credentials/credentials.json"
	GENERATED_CLIENT_SECRETS_FILE = "credentials/user_file.json"
