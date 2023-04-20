# Scripts for downloading youtube videos
## USECASE 1:
List out the available formats for video in <url>:
>> python download_urllib.py <url> --formats
Out:
format_str - quality_lable - height
FORMATS:
video/mp4; codecs="avc1.42001E, mp4a.40.2" - 360p - 360p
video/mp4; codecs="avc1.64001F, mp4a.40.2" - 720p - 720p


## USECASE 2:
Download youtube video with a specified format:
>> python download_urllib.py <url> --format_str <> --quality <>
>> python download_urllib.py "https://www.youtube.com/watch?v=OTVE5iPMKLg&ab_channel=CGPGrey" --format_str "video/mp4;\ codecs=\"avc1.42001E,\ mp4a.40.2\"" --quality 360
>> python download_urllib.py "https://www.youtube.com/watch?v=OTVE5iPMKLg&ab_channel=CGPGrey" --format_str "video/mp4;\ codecs=\"avc1.64001F,\ mp4a.40.2\"" --quality 720