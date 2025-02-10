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
    wait_seconds = settings.get("wait_seconds", 10)  # Используем значение из настроек
    post_step = settings.get("post_step", 3)         # Используем значение из настроек
    
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

                file = acc.download_media(
                    msg, 
                    file_name=os.path.join(chat_folder, ""),
                    progress=progress, 
                    progress_args=(uuid4(),)
                )
                if file:
                    file_size = os.path.getsize(file)
                    
                    logging.debug(f"Downloaded file: {file}, Size: {file_size} bytes")
                    
                    expected_size = msg.media.file_size if hasattr(msg.media, 'file_size') else None
                    if expected_size and file_size != expected_size:
                        logging.error(f"Incomplete download: Expected {expected_size} bytes, got {file_size} bytes.")
                        print(f"Incomplete download: Expected {expected_size} bytes, got {file_size} bytes.")
                        
                        file = acc.download_media(
                            msg,
                            file_name=os.path.join(chat_folder, ""),
                            progress=progress,
                            progress_args=(uuid4(),)
                        )
                        if file:
                            file_size = os.path.getsize(file)
                            if file_size != expected_size:
                                logging.error("Retry failed. File is still incomplete.")
                                print("Retry failed. File is still incomplete.")
                    else:
                        logging.info(f"File saved at: {file}")
                        print("\nSaved at", file, "\n")
            except ValueError as e:
                if str(e) == "This message doesn't contain any downloadable media":
                    txtfile = os.path.join(chat_folder, f"{str(msg.chat.id)[-10:]}-{msg.id}.txt")
                    with open(txtfile, "w", encoding="utf-8") as file:
                        file.write(str(msg.text))
                    logging.info(f"Text content saved at: {txtfile}")
                    print("Saved at", txtfile, "\n")
                else:
                    logging.error(f"Error downloading media: {e}")
                    print(e, "\n")
        
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
