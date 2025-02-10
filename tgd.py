from pyrogram import Client
from pyrogram.types import User, Message
from os.path import exists
from typing import Tuple
from utils import (
    wait, progress, get_media_type, print_dowload_msg, configfile,
    print_examples, create_logging_config, log_media_details,
    get_chat_folder, random_delay, RateLimiter,
    log_api_request
)
from uuid import uuid4
import json
import logging
import os
import time
import re
import tempfile
import shutil


LINKS_FILE = "links.txt"


def setup_logging(settings: dict):
    if settings.get("logging", False):
        if not os.path.exists("logging.conf"):
            create_logging_config()

        from logging.config import fileConfig
        fileConfig("logging.conf", encoding="utf-8")
        logging.info("Logging has been enabled with logging.conf.")
    else:
        logging.basicConfig(level=logging.CRITICAL)


def preProcess() -> Tuple[str, str, str, dict]:
    if not exists(configfile):
        try:
            login = input(
                f"{configfile} not found, Do you wish to login? (y/n): ")
            if login.lower() != "y":
                wait()
            api_id = input("\nAPI ID: ")
            api_hash = input("API HASH: ")
            check = input(
                "Do you have already created Session? selecting 'no' will trigger session login and 'yes' will ask for Session String (y/n): ")
            if check.lower() == "y":
                ss = input("SESSION STRING: ")
            else:
                print()
                temp = Client("temp", api_id=api_id,
                              api_hash=api_hash, in_memory=True)
                with temp:
                    ss = temp.export_session_string()
                print()
            config_data = {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": ss,
                "settings": {
                    "enable_links_auto_read": False,
                    "logging": False,
                    "wait_seconds": 0,
                    "post_step": 1,
                    "max_requests_per_second": 5,
                    "random_delay_min": 1,
                    "random_delay_max": 5
                }
            }
            with open(configfile, "w") as file:
                json.dump(config_data, file, indent=4)
            setup_logging(config_data["settings"])
            return api_id, api_hash, ss, config_data["settings"]
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting...")
            wait()
        except Exception as e:
            print(e)
            wait()
    else:
        try:
            with open(configfile, "r") as file:
                config_data = json.load(file)
            api_id = config_data["api_id"]
            api_hash = config_data["api_hash"]
            ss = config_data["session_string"]
            settings = config_data.get("settings", {})
            
            logging.debug(f"Loaded settings: {settings}")
            
            settings["wait_seconds"] = max(settings.get("wait_seconds", 10), 0)
            settings["post_step"] = max(settings.get("post_step", 3), 1)
            setup_logging(settings)
            return api_id, api_hash, ss, settings
        except Exception as e:
            print("Error reading config file:", e)
            print("Retry... by deleting", configfile)
            wait()


def read_links() -> list[str]:
    if exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    return []


def clean_filename(filename):
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
    cleaned = cleaned.strip()
    return cleaned

def get_file_extension(media) -> str:
    if hasattr(media, "mime_type") and media.mime_type:
        mime = media.mime_type.split("/")[-1]
        if mime in ["mp4", "mpeg", "quicktime"]:
            return "mp4"
        elif mime == "webm":
            return "webm"
        elif mime == "ogg":
            return "ogg"
        elif mime == "x-wav":
            return "wav"
    
    if media.type == "audio":
        return "mp3"
    elif media.type == "video":
        return "mp4"
    elif media.type == "document":
        return "dat"
    else:
        return "dat"

def handle_link(link: str, settings: dict):
    global rate_limiter
    
    if link.startswith("https://t.me/"):
        datas = link.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
        chatid = int("-100" + datas[4]) if link.startswith("https://t.me/c/") else datas[3]
    else:
        logging.warning(f"'{link}' - Not a Telegram Link")
        print(f"'{link}' - Not a Telegram Link")
        return
    
    chat = acc.get_chat(chatid)
    chat_folder = get_chat_folder(chat.id, chat.title)
    total = toID + 1 - fromID
    wait_seconds = settings.get("wait_seconds", 10)
    post_step = settings.get("post_step", 3)
    
    for i in range(fromID, toID + 1, post_step):
        group_end = min(i + post_step, toID + 1)
        for msgid in range(i, group_end):
            log_api_request("Fetching message", chat_id=chatid, message_id=msgid)
            
            rate_limiter.wait()
            
            random_delay(settings)
            
            msg: Message = acc.get_messages(chatid, msgid)
            if msg.empty:
                logging.info(f"Message not found: {chatid}/{msgid}, Skipping...")
                print("Message not found:", chatid, "/", msgid, "Skipping...\n")
                continue
            
            media = get_media_type(msg)
            if media:
                log_media_details(media, msgid, fromID, total)
                print_dowload_msg(media, msgid, fromID, total)
            else:
                logging.info(f"Text Content ({(msgid - fromID + 1)}/{total})")
                print("Text Content", f"({(msgid - fromID + 1)}/{total})")
            
            try:
                log_api_request("Downloading media", chat_id=chatid, message_id=msgid)

                temp_dir = tempfile.mkdtemp()

                if media:
                    if hasattr(media, 'file_name') and media.file_name:
                        file_name = clean_filename(media.file_name)
                    else:
                        extension = get_file_extension(media)
                        file_name = f"{msgid}_{media.__class__.__name__.lower()}.{extension}"

                    temp_file_path = os.path.join(temp_dir, file_name)

                    file = acc.download_media(
                        msg, 
                        file_name=temp_file_path,
                        progress=progress, 
                        progress_args=(uuid4(),)
                    )

                    if file:
                        final_file_path = os.path.join(chat_folder, file_name)
                        shutil.move(temp_file_path, final_file_path)
                        logging.info(f"File saved at: {final_file_path}")
                        print("\nSaved at", final_file_path, "\n")

                else:
                    txtfile = os.path.join(chat_folder, f"{str(msg.chat.id)[-10:]}-{msg.id}.txt")
                    with open(txtfile, "w", encoding="utf-8") as file:
                        file.write(str(msg.text) if msg.text else "[No Text Content]")
                    logging.info(f"Text content saved at: {txtfile}")
                    print("Saved at", txtfile, "\n")

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                print(f"\n{e}\nAn error occurred. Exiting...")
            finally:
                shutil.rmtree(temp_dir)

        
        if group_end <= toID:
            logging.info(f"Waiting for {wait_seconds} seconds before next group...")
            if wait_seconds != 0:
                print(f"Waiting for {wait_seconds} seconds before next group...\n")
                time.sleep(wait_seconds)


def main(settings: dict):
    try:
        logging.info("Starting the program.")
        print("Logging in...")
        with acc:
            me: User = acc.get_me()
            logging.info(f"Logged in as: {me.first_name} ({me.id})")
            print(
                f"Logged in as: {me.first_name}{(' ' + me.last_name) if me.last_name else ''}{(' - @' + me.username) if me.username else ''} ({me.id})")
            if settings.get("enable_links_auto_read", True):
                links = read_links()
                if links:
                    logging.info(f"Processing {len(links)} links from {LINKS_FILE}.")
                    print("Processing links from", LINKS_FILE)
                    for link in links:
                        handle_link(link, settings)
            else:
                logging.info("Automatic links reading is disabled in config.")
                print("Automatic links reading is disabled in config.")
            print_examples()
            while True:
                link = input("\nEnter a message/post link (or type 'exit' to quit): ")
                if link.lower() == "exit":
                    break
                logging.info(f"Handling link: {link}")
                handle_link(link, settings)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected. Exiting...")
        print("\nKeyboard interrupt detected. Exiting...")
        wait()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("\n", e, "\nAn error occurred. Exiting...")
        print("Retry... by deleting", configfile)
        wait()


if __name__ == "__main__":
    api_id, api_hash, ss, settings = preProcess()
    acc = Client("TGD", api_id=api_id, api_hash=api_hash, session_string=ss, in_memory=True)

    rate_limiter = RateLimiter(settings.get("max_requests_per_second", 5))

    main(settings)
    wait()
