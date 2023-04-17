import http.client
import httplib2
import os
import random
import sys
import time
import logging
import typing

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

from globals import ClientSettings
from globals import Credentials

class YoutubeClient:
    def __init__(self):
        self.client = YoutubeClient.get_build()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

    @staticmethod
    def get_build():
        try:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(Credentials.GENERATED_CLIENT_SECRETS_FILE)
        except Exception as ex:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(Credentials.ORIGINAL_CLIENT_SECRETS_FILE, ClientSettings.SCOPES)
            credentials = flow.run_local_server(port=8090)
            with open(Credentials.GENERATED_CLIENT_SECRETS_FILE, "w") as f:
                f.write(credentials.to_json())

        client = googleapiclient.discovery.build(ClientSettings.API_SERVICE_NAME, ClientSettings.API_VERSION, credentials=credentials)

        return client

    def upload_video(self, file_path, title="", description="", category="22", privacyStatus="private", tags=None):
        if tags is None:
            tags = []

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacyStatus
            }
        }

        request = self.client.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )

        self.__upload_video(request)

    def __upload_video(self, request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                self.logger.info("Uploading file...")
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        self.logger.info(f"Video id '{response['id']}' was successfully uploaded.")
                    else:
                        self.logger.error(f"The upload failed with an unexpected response: {response}")
                        return
            except HttpError as ex:
                if ex.resp.status in ClientSettings.RETRIABLE_STATUS_CODES:
                    error = ex
                    self.logger.warning(f"A retriable HTTP error {ex.resp.status} occurred:\n{ex.content}")
                else:
                    raise ex
            except ClientSettings.RETRIABLE_EXCEPTIONS as ex:
                error = ex
                self.logger.warning(f"A retriable error occurred: {ex}")

            if error is not None:
                self.logger.error(error)
                retry += 1
                if retry > ClientSettings.MAX_RETRIES:
                    self.logger.error("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                self.logger.warning(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)
