import re

def print_dict_keys(d, indent=0):
    for key in d:
        print(" " * indent + str(key))
        if isinstance(d[key], dict):
            print_dict_keys(d[key], indent + 4)

def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if not match:
        raise Exception("Could not extract video ID from URL")
    return match.group(1)