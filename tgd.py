from pyrogram import Client
from pyrogram.types import User, Message
from os.path import exists
from typing import Tuple
from utils import wait, progress, get_media_type, print_dowload_msg, configfile, print_examples
from uuid import uuid4
import json


LINKS_FILE = "links.txt"


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
                    "enable_links_auto_read": True
                }
            }

            with open(configfile, "w") as file:
                json.dump(config_data, file, indent=4)

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


def handle_link(link: str):
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
        print(f"'{link}' - Not a Telegram Link")
        return

    total = toID + 1 - fromID
    for msgid in range(fromID, toID + 1):
        msg: Message = acc.get_messages(chatid, msgid)
        if msg.empty:
            print("Message not found:", chatid, "/", msgid, "Skipping...\n")
            continue

        media = get_media_type(msg)
        if media:
            print_dowload_msg(media, msgid, fromID, total)
        else:
            print("Text Content", f"({(msgid - fromID + 1)}/{total})")
        try:
            file = acc.download_media(
                msg, progress=progress, progress_args=(uuid4(),))
            print("\nSaved at", file, "\n")
        except ValueError as e:
            if str(e) == "This message doesn't contain any downloadable media":
                txtfile = f"downloads/{str(msg.chat.id)[-10:]}-{msg.id}.txt"
                with open(txtfile, "w", encoding="utf-8") as file:
                    file.write(str(msg.text))
                print("Saved at", txtfile, "\n")
            else:
                print(e, "\n")


def main(settings: dict):
    try:
        print("Logging in...")
        with acc:
            me: User = acc.get_me()
            print(
                f"Logged in as: {me.first_name}{(' ' + me.last_name) if me.last_name else ''}{(' - @' + me.username) if me.username else ''} ({me.id})")

            if settings.get("enable_links_auto_read", True):
                links = read_links()
                if links:
                    print("Processing links from", LINKS_FILE)
                    for link in links:
                        handle_link(link)
            else:
                print("Automatic links reading is disabled in config.")

            print_examples()
            while True:
                link = input("\nEnter a message/post link (or type 'exit' to quit): ")
                if link.lower() == "exit":
                    break
                handle_link(link)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting...")
        wait()
    except Exception as e:
        print("\n", e, "\nAn error occurred. Exiting...")
        print("Retry... by deleting", configfile)
        wait()


if __name__ == "__main__":
    api_id, api_hash, ss, settings = preProcess()
    acc = Client("TGD", api_id=api_id, api_hash=api_hash, session_string=ss, in_memory=True)
    main(settings)
    wait()
