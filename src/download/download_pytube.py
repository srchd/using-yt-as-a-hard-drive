import argparse
from pytube import YouTube
from pytube.cli import on_progress


def download_video_with_pytube(url, quality=None):
    yt = YouTube(url)

    if quality:
        stream = yt.streams.filter(
            progressive=True, file_extension="mp4", res=f"{quality}p"
        ).first()
    else:
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

    if not stream:
        print("No suitable stream found.")
        return

    print(f"Downloading: {yt.title}")
    stream.download()
    print(f"Downloaded '{yt.title}' as '{stream.default_filename}'")


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos using Pytube")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--quality",
        type=int,
        help="Preferred video quality (height in pixels), e.g., --quality 720",
    )

    args = parser.parse_args()

    download_video_with_pytube(args.url, quality=args.quality)


if __name__ == "__main__":
    main()