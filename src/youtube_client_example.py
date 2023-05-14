from youtube import YoutubeClient
from youtube import YTHDSettings
from youtube import Path
from pprint import pprint
from pprint import pformat
import logging
import sys

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(YTHDSettings.LOG_FORMAT)
sh.setFormatter(formatter)
logger.addHandler(sh)

youtube_client = YoutubeClient()  # create client object, this might sometimes open a browser window for you to log in

logger.info("Your youtube videos:")  # list your videos, False, True default values
logger.info(pformat(youtube_client.list_videos(list_deleted=False, list_only_ythd=True)))


video_path = Path.string_to_path("/tmp_folder/another_folder")
# video_path = Path("another_folder", parent=Path("tmp_folder"))   # another way of doing it
logger.info(f"Created path: {video_path}")

# Upload a video
# I commented it out because due to API limits you can only upload ~6 videos per day. Working on a solution right now
file_location = "youtube/upload_test_video.mp4"
youtube_client.upload_video(file_location, "Some title", "some description", privacy_status="unlisted", path=video_path)

logger.info(pformat(youtube_client.list_videos(list_deleted=False, list_only_ythd=True)))
# As you can see, the path and the #ythd text gets added to the description
# We can store any information we want about the videos this way
# For example the YouTube Data API doesn't support deleting videos, however we can simply mark them #deleted and ignore them during querying

try:
    youtube_client.mark_video_deleted("<put video id here>")
except Exception:
    logger.info("video doesn't exists")






