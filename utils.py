from sys import exit
from pyrogram.types import Message
from pyrogram import enums
import time
from os import system, name as osname
import os
import logging
import random

class RateLimiter:
    def __init__(self, max_requests_per_second):
        self.max_requests_per_second = max_requests_per_second
        self.last_request_time = 0

    def wait(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time
        if elapsed_time < 1 / self.max_requests_per_second:
            time.sleep((1 / self.max_requests_per_second) - elapsed_time)
        self.last_request_time = current_time

def random_delay(settings):
    delay = random.uniform(
        settings.get("random_delay_min", 1),
        settings.get("random_delay_max", 5)
    )
    time.sleep(delay)

def wait():
    try:
        input("Press enter to exit...")
    except KeyboardInterrupt:
        pass
    finally:
        exit(0)

SPEED_DATA = {}

def progress(current, total, uuid):
    try:
        current_time = time.time()
        length = 50
        
        if uuid in SPEED_DATA:
            elapsed_time = current_time - SPEED_DATA[uuid]["last_time"]
            speed = (current - SPEED_DATA[uuid]["progress"]) / elapsed_time if elapsed_time > 0 else 0
        else:
            speed = 0
        
        SPEED_DATA[uuid] = {"last_time": current_time, "progress": current}
        
        progress_percent = current * 100 / total
        completed = int(length * current / total)
        bar = f"[{'#' * completed}{' ' * (length - completed)}] {progress_percent:.1f} % - {convert_bytes(speed)}/s - {convert_bytes(current)}"
        
        print(f"\r{bar}", end="")
        
        if current == total:
            print()
    except Exception as e:
        logging.error(f"Error in progress function: {e}")
        print(f"\nError in progress function: {e}")

available_media = ("audio", "document", "photo", "sticker",
                   "animation", "video", "voice", "video_note")

def get_media_type(message: Message) -> enums.MessageMediaType:
    if isinstance(message, Message):
        for kind in available_media:
            media = getattr(message, kind, None)
            if media is not None:
                return media
        else:
            return None

def convert_bytes(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    suffix_index = 0
    while size >= 1024 and suffix_index < len(suffixes) - 1:
        suffix_index += 1
        size /= 1024.0
    return f"{size:.{precision}f} {suffixes[suffix_index]}"

def get_file_name(media: enums.MessageMediaType) -> str:
    try:
        return media.file_name
    except:
        return media.file_unique_id

def print_dowload_msg(media: enums.MessageMediaType, msgid: int, fromID: int, total: int):
    print(
        f"{get_file_name(media)} -",
        f"{media.__class__.__name__} -",
        f"{convert_bytes(media.file_size)}",
        f"({(msgid - fromID + 1)}/{total})",
    )

def create_logging_config():
    config_content = """
[loggers]
keys=root
[handlers]
keys=fileHandler,consoleHandler
[formatters]
keys=genericFormatter
[logger_root]
level=DEBUG
handlers=fileHandler,consoleHandler
[handler_fileHandler]
class=FileHandler
formatter=genericFormatter
args=('app.log', 'a')
[handler_consoleHandler]
class=StreamHandler
formatter=genericFormatter
args=(sys.stdout,)
[formatter_genericFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
"""
    with open("logging.conf", "w") as config_file:
        config_file.write(config_content.strip())

def log_media_details(media, msgid: int, fromID: int, total: int):
    try:
        media_info = {
            "type": media.__class__.__name__,
            "file_name": getattr(media, "file_name", "N/A"),
            "file_size": convert_bytes(getattr(media, "file_size", 0)),
            "mime_type": getattr(media, "mime_type", "N/A"),
            "duration": getattr(media, "duration", "N/A"),
            "width": getattr(media, "width", "N/A"),
            "height": getattr(media, "height", "N/A"),
        }
        logging.info(f"Media details for message {msgid} ({(msgid - fromID + 1)}/{total}): {media_info}")
    except Exception as e:
        logging.error(f"Failed to log media details: {e}")

def get_chat_folder(chat_id: int, chat_title: str) -> str:
    folder_name = chat_title or str(chat_id)
    folder_name = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in folder_name)
    folder_path = os.path.join("downloads", folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    
    return folder_path

def log_api_request(action: str, chat_id: int = None, message_id: int = None):
    log_message = f"API Request: {action}"
    if chat_id is not None:
        log_message += f", Chat ID: {chat_id}"
    if message_id is not None:
        log_message += f", Message ID: {message_id}"
    logging.info(log_message)

def print_examples():
    print("""
Examples:
    https://t.me/xxxx/1423
    https://t.me/c/xxxx/10
    https://t.me/xxxx/1001-1010
    https://t.me/c/xxxx/101 - 120"""
          )

configfile = "config.json"
TGD = """
  ▄██████▄    ▄██████▄    ████████▄
 ██▀▀███▀▀██  ███    ███  ███   ▀███
     ███      ███    █▀   ███    ███
     ███     ▄███         ███    ███
     ███    ▀▀███ ████▄   ███    ███
     ███      ███    ███  ███    ███
     ███      ███    ███  ███   ▄███
    ▄████    ████████▀   ████████▀
"""
VERSION = "1.4.M"
system("cls" if osname == "nt" else "clear")
print(TGD)
print("	TeleGram Downloader")
print(f"	    Version {VERSION}\n")