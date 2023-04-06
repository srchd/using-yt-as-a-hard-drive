import re
import json
import urllib.request
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import string
from utils import extract_video_id

def get_video_info(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    with urllib.request.urlopen(video_url) as response:
        html = response.read().decode("utf-8")

    match = re.search(r"ytInitialPlayerResponse\s*=\s*({.*?});", html)
    if not match:
        raise Exception("Could not find ytInitialPlayerResponse in HTML")

    video_info = json.loads(match.group(1))

    return video_info


def extract_video_url(video_info, preferred_quality=None, format_string=None):
    formats = video_info["streamingData"]["formats"]
    adaptive_formats = video_info["streamingData"]["adaptiveFormats"]
    all_formats = formats + adaptive_formats
    video_url = None

    if format_string:
        for format in all_formats:
            if format["mimeType"].startswith(format_string) and (
                preferred_quality is None or format.get("height") == preferred_quality
            ):
                video_url = format["url"]
                break

    if not video_url:
        for format in all_formats:
            if format["mimeType"].startswith("video/mp4"):
                video_url = format["url"]
                break

    if not video_url:
        raise Exception("Could not find video URL")

    return video_url


def download_video(video_url, file_name):
    response = urllib.request.urlopen(video_url)
    file_size = int(response.getheader("Content-Length"))
    chunk_size = 1 * 1024**2

    with open(file_name, "wb") as out_file:
        for chunk in tqdm(
            iter(lambda: response.read(chunk_size), b""),
            total=file_size // chunk_size,
            unit="KB",
        ):
            out_file.write(chunk)


def download_chunk(url, start_byte, end_byte, chunk_index):
    req = urllib.request.Request(url)
    req.headers["Range"] = f"bytes={start_byte}-{end_byte}"

    with urllib.request.urlopen(req) as response:
        chunk_data = response.read()
        return chunk_index, chunk_data


def download_video_parallel(video_url, file_name, num_threads=4):
    req = urllib.request.Request(video_url, method="HEAD")
    with urllib.request.urlopen(req) as response:
        file_size = int(response.getheader("Content-Length"))

    chunk_size = file_size // num_threads
    futures = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            start_byte = i * chunk_size
            end_byte = (
                (i + 1) * chunk_size - 1 if i != num_threads - 1 else file_size - 1
            )
            futures.append(
                executor.submit(download_chunk, video_url, start_byte, end_byte, i)
            )

        # Create a progress bar
        progress_bar = tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Downloading"
        )

    with open(file_name, "wb") as out_file:
        for future in as_completed(futures):
            chunk_index, chunk_data = future.result()
            out_file.seek(chunk_index * chunk_size)
            out_file.write(chunk_data)
            # print(f"Downloaded chunk {chunk_index + 1} of {num_threads}")

            # Update the progress bar with the size of the downloaded chunk
            progress_bar.update(len(chunk_data))

    progress_bar.close()



def list_formats(video_info):
    formats = video_info["streamingData"]["formats"]
    adaptive_formats = video_info["streamingData"]["adaptiveFormats"]

    print(f"format_str - quality_lable - height")
    print("FORMATS:")
    for format in formats:
        height = format.get("height", "N/A")
        quality_label = format.get("qualityLabel", "N/A")
        print(f"{format['mimeType']} - {quality_label} - {height}p")

    print("ADAPTIVE FORMATS:")
    for format in adaptive_formats:
        height = format.get("height", "N/A")
        quality_label = format.get("qualityLabel", "N/A")
        print(f"{format['mimeType']} - {quality_label} - {height}p")


def sanitize_file_name(file_name):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized_file_name = "".join(c for c in file_name if c in valid_chars)
    return sanitized_file_name


# thread = 50
# s = measure_download(video_url, file_name, num_threads=thread)
# print(f"download with thread #={thread}: {s} sec")
def measure_download(video_url, file_name, num_threads):
    t = time.time()
    download_video_parallel(video_url, file_name, num_threads)
    return time.time() - t


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos. Example: python example_urllib.py "url" --format 720'
    )
    parser.add_argument(
        "url",
        help="YouTube video URL.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=64,
        help="Number of threads to use (default: 64). Example: --threads 32",
    )
    parser.add_argument(
        "--formats",
        action="store_true",
        help="List available formats instead of downloading. Example: --formats",
    )
    parser.add_argument(
        "--format",
        type=int,
        help="Preferred video format (height in pixels). Example: --format 720",
    )
    parser.add_argument(
        "--format_str",
        type=str,
        help="Preferred video format string (e.g., 'video/mp4; codecs=\"avc1.640028\"')",
    )

    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    video_info = get_video_info(video_id)
    video_title = video_info["videoDetails"]["title"]

    if args.formats:
        list_formats(video_info)
    else:
        video_url = extract_video_url(
            video_info, preferred_quality=args.format, format_string=args.format_str
        )
        print(video_url)
        file_name = sanitize_file_name(f"{video_title}.mp4")
        download_video_parallel(video_url, file_name, num_threads=args.threads)
        print(f"Downloaded '{video_title}' as '{file_name}'")


if __name__ == "__main__":
    main()

# speed with threads: (3MB video)
# download with thread #=1: 55.3245325088501 sec
# download with thread #=4: 13.866512775421143 sec
# download with thread #=16: 3.632211208343506 sec
# download with thread #=32: 2.129448890686035 sec
# download with thread #=50: 1.7260501384735107 sec
### download with thread #=64: 1.6896257400512695 sec ###
# download with thread #=80: 1.8468973636627197 sec
# download with thread #=100: 1.9939064979553223 sec
# download with thread #=128: 2.0553581714630127 sec
