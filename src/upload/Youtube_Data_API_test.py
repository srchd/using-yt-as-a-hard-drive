import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials

import http.client
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

scopes = ["https://www.googleapis.com/auth/youtube",
					"https://www.googleapis.com/auth/youtube.force-ssl",
					"https://www.googleapis.com/auth/youtube.readonly",
					"https://www.googleapis.com/auth/youtubepartner",
					"https://www.googleapis.com/auth/youtubepartner-channel-audit"]


MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = [
	httplib2.HttpLib2Error, IOError, http.client.NotConnected,
	http.client.IncompleteRead, http.client.ImproperConnectionState,
	http.client.CannotSendRequest, http.client.CannotSendHeader,
	http.client.ResponseNotReady, http.client.BadStatusLine
]

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

VALID_PRIVACY_STATUSES = ["public", "private", "unlisted"]


def get_build():
	ORIGINAL_CLIENT_SECRETS_FILE = "YOUR_CLIENT_SECRET_FILE.json"
	GENERATED_CLIENT_SECRETS_FILE = "CLIENT_SECRETS_FILE.json"

	try:
		credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(GENERATED_CLIENT_SECRETS_FILE)
	except Exception as ex:
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(ORIGINAL_CLIENT_SECRETS_FILE, scopes)
		credentials = flow.run_console()
		with open(GENERATED_CLIENT_SECRETS_FILE, "w") as f:
			f.write(credentials.to_json())

	api_service_name = "youtube"
	api_version = "v3"

	youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

	return youtube

def initialize_upload(youtube, options):
	tags = None
	if options["keywords"]:
		tags = options["keywords"].split(",")

	body=dict(
		snippet=dict(
			title=options["title"],
			description=options["description"],
			tags=tags,
			categoryId=options["category"]
		),
		status=dict(
			privacyStatus=options["privacyStatus"]
		)
	)

	insert_request = youtube.videos().insert(
		part=",".join(body.keys()),
		body=body,
		media_body=MediaFileUpload(options["file"], chunksize=-1, resumable=True)
	)

	resumable_upload(insert_request)

def resumable_upload(insert_request):
	response = None
	error = None
	retry = 0
	while response is None:
		try:
			print("Uploading file...")
			status, response = insert_request.next_chunk()
			if response is not None:
				if 'id' in response:
					print(f"Video id '{response['id']}' was successfully uploaded.")
				else:
					exit(f"The upload failed with an unexpected response: {response}")
		except HttpError as ex:
			if ex.resp.status in RETRIABLE_STATUS_CODES:
				error = f"A retriable HTTP error {ex.resp.status} occurred:\n{ex.content}"
			else:
				raise
		except RETRIABLE_EXCEPTIONS as ex:
			error = f"A retriable error occurred: {ex}"

		if error is not None:
			print(error)
			retry += 1
			if retry > MAX_RETRIES:
				exit("No longer attempting to retry.")

			max_sleep = 2 ** retry
			sleep_seconds = random.random() * max_sleep
			print(f"Sleeping {sleep_seconds} seconds and then retrying...")
			time.sleep(sleep_seconds)


if __name__ == '__main__':
	file_path = "VIDEO_NAME.mp4"

	options = {
		"keywords": "Video keywords, comma separated",
		"title": "Asd",
		"description": "asd",
		"category": "22",
		"privacyStatus": "private",
		"file": file_path
	}

	if not os.path.exists(file_path):
		exit("Invalid path")

	youtube = get_build()
	try:
		initialize_upload(youtube, options)
	except HttpError as ex:
		print(f"An HTTP error {ex.resp.status} occurred:\n{ex.content}")
