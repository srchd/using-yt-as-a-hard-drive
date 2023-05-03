from youtube.youtube_client import YoutubeClient
from youtube.youtube_client_parameters import Path
from pprint import pprint

youtube_client = YoutubeClient()  # create client object, this might sometimes open a browser window for you to log in

print("Your youtube videos:")
pprint(youtube_client.list_videos(list_deleted=False, list_only_ythd=True))  # list your videos, False, True default values

video_path = Path.string_to_path("/tmp_folder/another_folder")
# video_path = Path("another_folder", parent=Path("tmp_folder"))   # another way of doing it
print("Created path:", video_path)

# Upload a video
# I commented it out because due to API limits you can only upload ~6 videos per day. Working on a solution right now
# file_location = "youtube/upload_test_video.mp4"
# youtube_client.upload_video(file_location, "Some title", "some description", privacy_status="unlisted", path=video_path)

pprint(youtube_client.list_videos(list_deleted=False, list_only_ythd=True))
# As you can see, the path and the #ythd text gets added to the description
# We can store any information we want about the videos this way
# For example the YouTube Data API doesn't support deleting videos, however we can simply mark them #deleted and ignore them during querying

try:
    youtube_client.mark_video_deleted("put video id here")
except Exception:
    print("video doesn't exists")






