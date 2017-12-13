import json
import requests
import time
import urllib
import os
from dbhelper import DBhelper

db = DBhelper()
token = os.environ['TELEGRAM_TOKEN']
last_update_id = None
url = "https://api.telegram.org/bot{}/".format(token)

def get_url(URL):
    response = requests.get(URL)
    content = response.content.decode("utf8")
    return content
def get_json_from_url(URL):
    content = get_url(URL)
    js = json.loads(content)
    return js
def get_updates(offset=None):
    Url = url + "getUpdates?timeout=100"
    if offset:
        Url += "&offset={}".format(offset)
    js = get_json_from_url(Url)
    return js
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        URL += "&reply_markup={}".format(reply_markup)
    get_url(URL)
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
def register_db(chat_id,Name,Id):
    db.add_item([chat_id,Name,Id])
    return
def build_keyboard(items):
    keyboard = {"/reg":items[0],items[1]:"/get"}
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
def isUpdate(updates):
    global last_update_id
    last = get_last_update_id(updates)
    counter = 0
    while counter <= 60 :
        refresh = get_updates(last)
        if len(refresh["result"]) > 0:
            last_update_id = last + 1
            return True
        counter += 1
        time.sleep(1)
    return False
def register(updates,chat_id):
    Name = ""
    ID = ""
    send_message("نام و نام خانوادگی خود را وارد کنید",chat_id)
    if isUpdate(updates) :
        updates = get_updates(last_update_id)
        for update in updates["result"]:
            if update["message"]["chat"]["id"]==chat_id :
                Name = update["message"]["text"]
    else:
        return False
    send_message(" شماره دانشجویی خود را وارد کنید",chat_id)
    if isUpdate(updates) :
        updates = get_updates(last_update_id)
        for update in updates["result"]:
            if update["message"]["chat"]["id"]==chat_id :
                ID = update["message"]["text"]
    else:
        return False
    register_db(chat_id,Name,ID)
    return True
def get_report(chat_id):
    item = db.get_item()
    for i in item :
        send_message(str(i),chat_id)
def main():
    db.setup()
    global last_update_id
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            for update in updates["result"]:
                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]
                if text == "/start":
                    key = build_keyboard(["ثبت نام","اطلاعات ثب شده"])
                    send_message("به ربات ثبت نام خوش امدین",chat_id,key)
                elif text == "/reg":
                    if register(updates,chat_id) :
                        send_message("😉ثبت نام شما انجام شد",chat_id)
                        last_update_id += 1
                elif text == "/get":
                    get_report(chat_id)
                else:
                    send_message("پیام شما قابل مفهوم نیست",chat_id)
        time.sleep(0.5)
if __name__ == '__main__':
    main()
