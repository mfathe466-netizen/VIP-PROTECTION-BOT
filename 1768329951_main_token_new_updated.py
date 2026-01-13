import os
import logging
import asyncio
import subprocess
import random
from pathlib import Path
import re
import shutil
import requests
import zipfile
from telethon import TelegramClient, events, Button
try:
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
    
except ImportError:
    print("python-telegram-bot is not installed. Installing it now...")
    try:
        subprocess.check_call(["pip3", "install", "python-telegram-bot"])
        print("python-telegram-bot has been successfully installed.")
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
    except Exception as e:
        try:
            subprocess.check_call(["pip", "install", "python-telegram-bot"])
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
            print("python-telegram-bot has been successfully installed using pip3.")
        except Exception as e:
            print("Failed to install python-telegram-bot with pip and pip3:", str(e))
            exit(0)
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
try:
    from telethon import TelegramClient, sync, functions, errors, events, types
    from telethon.tl.functions.channels import LeaveChannelRequest
except ImportError:
    print("telethon is not installed. Installing it now...")
    try:
        subprocess.check_call(["pip3", "install", "telethon"])
        print("telethon has been successfully installed.")
        from telethon import TelegramClient, sync, functions, errors, events, types
    except Exception as e:
        try:
            subprocess.check_call(["pip", "install", "telethon"])
            from telethon import TelegramClient, sync, functions, errors, events, types
            print("telethon has been successfully installed using pip.")
        except Exception as e:
            print("Failed to install telethon with pip and pip:", str(e))
            exit(0)
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest
from telethon.tl.functions.messages import SendReactionRequest
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.messages import GetHistoryRequest

try:
    import requests
except ImportError:
    print("requests is not installed. Installing it now...")
    try:
        subprocess.check_call(["pip3", "install", "requests"])
        print("requests has been successfully installed.")
        import requests
    except Exception as e:
        try:
            subprocess.check_call(["pip", "install", "requests"])
            import requests
            print("requests has been successfully installed using pip.")
        except Exception as e:
            print("Failed to install requests with pip and pip:", str(e))
            exit(0)
import json
API_ID = '21891434'
API_HASH = '13d9e20b29959754475e32dbae967cc8'
BOT_TOKEN = "8536356763:AAFLXUWPnYpzAHx1xVDWbAEbLWG3uz6mgAw"
running_processes = {}
SESSIONS_DIR = 'echo_ac'
try:
    with open("echo_data.json", "r") as json_file:
        info = json.load(json_file)
except FileNotFoundError:
    info = {}

if "token" not in info:
    while (True):
        BOT_TOKEN = "8536356763:AAFLXUWPnYpzAHx1xVDWbAEbLWG3uz6mgAw"
        response = requests.request(
            "GET", f"https://api.telegram.org/bot{bot_token}/getme")
        response_json = response.json()
        if (response_json["ok"] == True):
            info["token"] = bot_token
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
            break
        else:
            print("token is not correct !")
else:
    bot_token = info["token"]

if "sudo" not in info:
    info["sudo"] = 7418663073
    info["admins"] = {}
    with open("echo_data.json", "w") as json_file:
        json.dump(info, json_file)

from telethon.tl.functions.payments import CheckGiftCodeRequest 
from telethon.tl.types import MessageActionGiftCode




clients = {}
async def background_task(phonex, bot_username, sudo, send_to):
    global clients
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"جاري الاتصال بالرقم : {phonex}"
    })
    clients[f"{phonex}-{sudo}"] = TelegramClient(f"echo_ac/{sudo}/{phonex}", API_ID, API_HASH, device_model="Devloper : @DaD22DD")
    clientx = clients[f"{phonex}-{sudo}"]
    try:
        @clientx.on(events.NewMessage)
        async def handle_new_message(event):
            if event.is_channel:
                await clientx(GetMessagesViewsRequest(
                    peer=event.chat_id,
                    id=[event.message.id],
                    increment=True
                ))
        await clientx.connect()
        await clientx(UpdateStatusRequest(offline=False))
        if not await clientx.is_user_authorized():
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": sudo,
                "text": f"الحساب غير مسجل بالبوت : {phonex}"
            })
            await clientx.disconnect()
            stop_background_task(phonex, sudo)
            return 0
    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"حدث خطا في الحساب : {phonex}"
        })
        await clientx.disconnect()
        stop_background_task(phonex, sudo)
        return 0
    else:
        me = await clientx.get_me()
        user_id = me.id
        if (send_to == "انا"):
            send_to = sudo
        elif (send_to == "حساب"):
            send_to = user_id
        await clientx.send_message(bot_username,'/start')
        response = requests.request(
            "GET", f"https://bot.keko.dev/api/?login={user_id}&bot_username={bot_username}")
        response_json = response.json()
        if response_json.get("ok", False):
            echo_token = response_json.get("token", "")
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": sudo,
                "text": f"- تم تسجيل الدخول الى رقم بنجاح ✅\n\n- الرقم : {phonex} \n\n- ستيم ارسال نقاط الى : {send_to}"
            })
            
            print('ffggg')
            
            while True:
                response = requests.request(
                    "GET", f"https://bot.keko.dev/api/?token={echo_token}")
                response_json = response.json()
                if not response_json.get("ok", False):
                    
                    await asyncio.sleep(20)
                    continue
                if (response_json.get("canleave", False)):
                    for chat in response_json["canleave"]: 
                        try:
                            await clientx.delete_dialog(chat)
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": sudo,
                                "text": "- تم مغادرة : "+str(chat)+" -> بسبب انتهاء مده الاشتراك"+f" \n\n- {phonex}"
                            })
                            await asyncio.sleep(random.randint(3,10))
                        except Exception as e:
                            print(f"Error: {str(e)}")

                if response_json.get("type", "") == "link":
                    try:
                        await clientx(ImportChatInviteRequest(response_json.get("tg", "")))
                        await asyncio.sleep(random.randint(2,5))
                        messages = await clientx.get_messages(
                            int(response_json.get("return", "")), limit=20)
                        MSG_IDS = [message.id for message in messages]
                        await asyncio.sleep(random.randint(2,5))
                        await clientx(GetMessagesViewsRequest(
                            peer=int(response_json.get("return", "")),
                            id=MSG_IDS,
                            increment=True
                        ))
                        try:
                            await clientx(SendReactionRequest(
                                peer=int(response_json.get("return", "")),
                                msg_id=messages[0].id,
                                big=True,
                                add_to_recent=True,
                                reaction=[types.ReactionEmoji(
                                    emoticon='👍'
                                )]
                            ))
                        except Exception as e:
                            print(f"Error: {str(e)}")
                    except errors.FloodWaitError as e:
                        timeoutt = random.randint(e.seconds,e.seconds+1000)
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- تم حظر الرقم لمدة {timeoutt} ثانيه \n\n- {phonex}"
                        })
                        try:
                            await clientx(UpdateStatusRequest(offline=True))
                            await clientx.disconnect()
                            await asyncio.sleep(timeoutt)
                            await clientx.connect()
                            await clientx(UpdateStatusRequest(offline=False))
                        except Exception as e:
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": sudo,
                                "text": f"حدث خطا في الحساب : {phonex}"
                            })
                            stop_background_task(phonex, sudo)
                            return 0
                        continue
                    except Exception as e:
                        timeoutt = random.randint(200,400)
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- انتظر {timeoutt} ثانيه \n\n{str(e)}\n\n- رقم الحساب : {phonex}"
                        })
                        await asyncio.sleep(timeoutt)
                else:
                    try:
                        await clientx(JoinChannelRequest(response_json.get("return", "")))
                        await asyncio.sleep(random.randint(2,5))
                        entity = await clientx.get_entity(response_json.get("return", ""))
                        await asyncio.sleep(random.randint(2,5))
                        messages = await clientx.get_messages(entity, limit=10)
                        await asyncio.sleep(random.randint(2,5))
                        MSG_IDS = [message.id for message in messages]
                        await clientx(GetMessagesViewsRequest(
                            peer=response_json.get("return", ""),
                            id=MSG_IDS,
                            increment=True
                        ))
                        try:
                            await clientx(SendReactionRequest(
                                peer=response_json.get("return", ""),
                                msg_id=messages[0].id,
                                big=True,
                                add_to_recent=True,
                                reaction=[types.ReactionEmoji(
                                    emoticon='👍'
                                )]
                            ))
                        except Exception as e:
                            print(f"Error: {str(e)}")
                    except errors.FloodWaitError as e:
                        timeoutt = random.randint(e.seconds,e.seconds+1000)
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- تم حظر الرقم لمدة {timeoutt} ثانيه \n\n- {phonex}"
                        })
                        try:
                            await clientx(UpdateStatusRequest(offline=True))
                            await clientx.disconnect()
                            await asyncio.sleep(timeoutt)
                            await clientx.connect()
                            await clientx(UpdateStatusRequest(offline=False))
                        except Exception as e:
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": sudo,
                                "text": f"حدث خطا في الحساب : {phonex}"
                            })
                            stop_background_task(phonex, sudo)
                            return 0
                        continue
                    except Exception as e:
                        timeoutt = random.randint(200,400)
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": sudo,
                            "text": f"- خطا : انتظار {timeoutt} ثانيه \n\n{str(e)}\n\n- {phonex}"
                        })
                        try:
                            await clientx(UpdateStatusRequest(offline=True))
                            await clientx.disconnect()
                            await asyncio.sleep(timeoutt)
                            await clientx.connect()
                            await clientx(UpdateStatusRequest(offline=False))
                        except Exception as e:
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": sudo,
                                "text": f"حدث خطا في الحساب : {phonex}"
                            })
                            stop_background_task(phonex, sudo)
                            return 0
                        continue
                response = requests.request(
                    "GET", f"https://bot.keko.dev/api/?token={echo_token}&to_id={send_to}&done="+response_json.get("return", ""))
                response_json = response.json()
                timeoutt = random.randint(int(info["sleeptime"]),(int(info["sleeptime"])*1.3))
                if not response_json.get("ok", False):
                                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": f"- "+response_json.get("msg", "")+f" \n\n- {phonex}"
                    })
                else:
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": f"تم الاشتراك في قناة جديده 👥\n\n يمكنك مغادرة القنوات بعد : " + str(response_json.get("timeout", "")) +  f" ثانيه\n• التجميع يعمل 🤍"
                    })
            

                try:
                    await clientx(UpdateStatusRequest(offline=True))
                    await clientx.disconnect()
                    await asyncio.sleep(timeoutt)
                    await clientx.connect()
                    await clientx(UpdateStatusRequest(offline=False))
                except Exception as e:
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": sudo,
                        "text": f"حدث خطا في الحساب : {phonex}"
                    })
                    stop_background_task(phonex, sudo)
                    return 0
        else:
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                "chat_id": sudo,
                "text": f"- "+response_json.get("msg", "")+f" \n\n- {phonex}"
            })
        await clientx.disconnect()
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": sudo,
            "text": f"- تم ايقاف التجميع بهذا الرقم : {phonex}"
        })
        stop_background_task(phonex, sudo)

def start_background_task(phone, bot_username, chat_id, send_to):
    chat_id = str(chat_id)
    phone = str(phone)
    stop_background_task(phone, chat_id)
    if chat_id not in running_processes:
        running_processes[chat_id] = {}
    if phone not in running_processes[chat_id]:
        task = asyncio.create_task(background_task(phone, bot_username, chat_id,send_to))
        running_processes[chat_id][phone] = task

def stop_all_background_tasks(chat_id):
    chat_id = str(chat_id)
    if chat_id in running_processes:
        for phone, task in running_processes[chat_id].items():
            if not task.done():
                task.cancel()
                clients[f"{phone}-{chat_id}"].disconnect()
                del clients[f"{phone}-{chat_id}"]
                print(f"Stopped background task for phone {phone} and chat_id {chat_id}")
            else:
                print(f"Background task for phone {phone} and chat_id {chat_id} is not running.")
        running_processes.pop(chat_id, None)
    else:
        print(f"No running tasks found for chat_id {chat_id}.")

def stop_background_task(phone, chat_id):
    chat_id = str(chat_id)
    phone = str(phone)
    if chat_id in running_processes and phone in running_processes[chat_id]:
        task = running_processes[chat_id][phone]
        clients[f"{phone}-{chat_id}"].disconnect()
        del clients[f"{phone}-{chat_id}"]
        if not task.done():
            task.cancel()
            print(f"Stopped background task for phone {phone} and chat_id {chat_id}")
        else:
            print(f"Background task for phone {phone} and chat_id {chat_id} is not running.")
        running_processes[chat_id].pop(phone, None)
    else:
        print(f"No background task found for phone {phone} and chat_id {chat_id}.")

logging.basicConfig(
    format="%(asctime)s%(name)s%(levelname)s%(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
if not os.path.isdir("echo_ac"):
    os.makedirs("echo_ac")
what_need_to_do_echo = {}
if "sleeptime" not in info:
    info["sleeptime"] = 30

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    if update.message and update.message.chat.type == "private":
        if (str(update.message.chat.id) == str(info["sudo"])):
            if not os.path.isdir("echo_ac/"+str(update.message.chat.id)):
                os.makedirs("echo_ac/"+str(update.message.chat.id))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضف رقم ➕", callback_data="addecho"),
                    InlineKeyboardButton(
                        "حذف رقم ➖", callback_data="delecho")
                ],
                [
                    InlineKeyboardButton("ارقامك 🗃", callback_data="myecho"),
                ],
                [
                    InlineKeyboardButton(
                        "تشغيل التجميع 🟢", callback_data="runall"),
                    InlineKeyboardButton(
                        "ايقاف التجميع 🔴", callback_data="stopall")
                ], 
                [
                    InlineKeyboardButton("اوامر تحويلات النقاط 🔃", callback_data="reloadcoin"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر الادمن 👨‍✈️", callback_data="anaaaaa"),
                    InlineKeyboardButton(
                        "تحويل تلمبر 🛗", callback_data="templer"),
                ], 
                [
                    InlineKeyboardButton(
                        "جلب مميز 🌟", callback_data='giftcode'),
                    InlineKeyboardButton(
                        "اوامر التحكم ⏺", callback_data='dellecho'),
                ],
                [
                    InlineKeyboardButton(
                        "جلب ملف الارقام 📥", callback_data="copynumper"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر المميز 🏅", callback_data="gifts"),
                ],
                [
                    InlineKeyboardButton(
                        "قناة المطور ⚜️", url="t.me/DaD22DD"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("""مرحبآ بك في بوت المخضرم.البوت مخصص بتجميع نقاط جميع البوتات وبخدمات ومنيزات رائعه داخل البوت\n\nDev : @DaD22DD""", reply_markup=reply_markup)
        elif str(update.message.chat.id) in info["admins"]:
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضف رقم ➕", callback_data="addecho"),
                    InlineKeyboardButton(
                        "حذف رقم ➖", callback_data="delecho")
                ],
                [
                    InlineKeyboardButton("ارقامك 🗃", callback_data="myecho"),
                ],
                [
                    InlineKeyboardButton(
                        "تشغيل التجميع 🟢", callback_data="runall"),
                    InlineKeyboardButton(
                        "ايقاف التجميع 🔴", callback_data="stopall")
                ], 
                [
                    InlineKeyboardButton("اوامر تحويلات النقاط 🔃", callback_data="reloadcoin"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر الادمن 👨‍✈️", callback_data="anaaaaa"),
                    InlineKeyboardButton(
                        "تحويل تلمبر 🛗", callback_data="templer"),
                ], 
                [
                    InlineKeyboardButton(
                        "جلب مميز 🌟", callback_data='giftcode'),
                    InlineKeyboardButton(
                        "اوامر التحكم ⏺", callback_data='dellecho'),
                ],
                [
                    InlineKeyboardButton(
                        "جلب ملف الارقام 📥", callback_data="copynumper"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر المميز 🏅", callback_data="gifts"),
                ],
                [
                    InlineKeyboardButton(
                        "قناة المطور ⚜️", url="t.me/DaD22DD"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("مرحبآ بك في بوت المخضرم.البوت مخصص بتجميع نقاط جميع البوتات وبخدمات ومنيزات رائعه داخل البوت\n\nDev : @DaD22DD", reply_markup=reply_markup)

def contact_validate(text):
    text = str(text)  
    if len(text) > 0:
        if text[0] == '+':
            if text[1:].isdigit():
                return True
    return False

import os
import requests
import asyncio





async def delall(chat_id):
    directory=f'echo_ac/{chat_id}'
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": f"الرقم : {file}\n تم حذفه"
                }
            )
            os.remove(file_path)  
async def copynum(chat_id):
    print('ghhhhhh')
    directory = f'echo_ac/{chat_id}'
    zip_filename = f"{directory}.zip"

    shutil.make_archive(directory, 'zip', directory)

    await send_file(bot_token, chat_id, zip_filename)

async def send_file(bot_token, chat_id, file_path):
    print('gggehnfkgjvhg')
    with open(file_path, 'rb') as f:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendDocument",
            data={
                "chat_id": chat_id,
                "caption": "نسخة احتياطيه بجميع حساباتك 👥"
            },
            files={
                "document": f
            }
        )
    print('ggkpwpdn')
    return response.json()

async def userbackup(chat_id):
    print('نقل الملفات شغال...')
    directory = f'echo_ac/{chat_id}'
    zip_filename = f"{chat_id}_accounts.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), file)
    await send_file(bot_token, chat_id, zip_filename)

async def send_file(bot_token, chat_id, file_name):
    print('رفع الملفات شغال...')
    with open(file_name, 'rb') as f:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendDocument",
            data={"chat_id": chat_id},
            files={"document": (file_name, f)}
        )
    print('الملفات اترفعت!')
    return response.json()
    
async def joinchn(id, chn):
    directory_path = Path(f"echo_ac/{id}")
    file_list = [
        file.name for file in directory_path.iterdir()
        if file.is_file() and file.name.endswith('.session')
    ]

    for file in file_list:
        print(file)
        file = file.replace('.session', '')
        async with TelegramClient(f"echo_ac/{id}/{file}", API_ID, API_HASH, device_model="Devloper : @DaD22DD") as client:
            try:
                if not await client.is_user_authorized():
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": id,
                        "text": f"الرقم : {file} غير صالح"
                    })
                    return
                else:
                    client.lang_code = 'ar'
                    await client.connect()

                    await client(JoinChannelRequest(chn))

                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                        "chat_id": id,
                        "text": f"الرقم : {file}\nتم الانضمام في  {chn}"
                    })

            except Exception as e:
                print(f"حدث خطأ: {e}")
                return


async def echoMaker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    if not update.message or update.message.chat.type != "private":
        return 0
    if (str(update.message.chat.id) != str(info["sudo"]) and str(update.message.chat.id) not in info["admins"]):
        return 0
    if update.message.text and update.message.text.startswith("/run "):
        filename = update.message.text.split(" ")[1]
        what_need_to_do_echo[str(update.message.chat.id)] = f"run:{filename}"
        await update.message.reply_text(f"ارسل معرف البوت الذي تريد للحساب التجميع منه : \n\n- {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif update.message.text and update.message.text.startswith("/join "):
        chn = update.message.text.split(" ")[1]
        id = update.message.chat.id
        print(id)
        
        await update.message.reply_text(f"انتظر جاري الانضمام", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        await joinchn(id,chn)
        
    elif update.message.text and update.message.text.startswith("/stop "):
        filename = update.message.text.split(" ")[1]
        await update.message.reply_text(f"تم ايقاف تشغيل الرقم : {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        stop_background_task(filename, update.message.chat.id)
    elif (update.message.text and (str(update.message.chat.id) in what_need_to_do_echo)):
        if (what_need_to_do_echo[str(update.message.chat.id)] == "addecho"):
            if (not contact_validate(update.message.text)):
                await update.message.reply_text(f"ارسل رقم صحيح ", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                return
            client = TelegramClient(
                f"echo_ac/{update.message.chat.id}/{update.message.text}", API_ID, API_HASH, device_model="Devloper : @DaD22DD")
            try:
                await client.connect()
                what_need_to_do_echo[str(
                    update.message.chat.id)+":phone"] = update.message.text
                eeecho = await client.send_code_request(update.message.text)
                what_need_to_do_echo[str(
                    update.message.chat.id)+":phone_code_hash"] = eeecho.phone_code_hash
                await update.message.reply_text(f"تم ارسال رمز تحقق الى الحساب .. ارسله لي 💬", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = "echocode"
            except Exception as e:
                await client.log_out()
                what_need_to_do_echo[str(update.message.chat.id)] = ""
                await update.message.reply_text(f"حدث خطأ غير متوقع: {str(e)}", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
            await client.disconnect()
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "sleeptime"):
            info["sleeptime"] = int(update.message.text)
            await update.message.reply_text(f"تم الحفظ بنجاح.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
            what_need_to_do_echo[str(update.message.chat.id)] = ""
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "deladminecho"):
            if os.path.isdir("echo_ac/"+str(update.message.text)):
                os.rmdir("echo_ac/"+str(update.message.text))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if "admins" not in info:
                info["admins"] = {}
            if str(update.message.text) in info["admins"]:
                del running_processes[str(update.message.text)]
                with open("echo_data.json", "w") as json_file:
                    json.dump(info, json_file)
                await update.message.reply_text(f"تم مسح الادمن بنجاح.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                stop_all_background_tasks(str(update.message.chat.id))
            else:
                await update.message.reply_text(f"لا يوجد هكذا ادمن.", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "addadminecho"):
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if not os.path.isdir("echo_ac/"+str(update.message.text)):
                os.makedirs("echo_ac/"+str(update.message.text))
            if "admins" not in info:
                info["admins"] = {}
            info["admins"][str(update.message.text)] = str(50)
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
            await update.message.reply_text(f"تم اضافه ادمن جديد بنجاح.\n\n- يمكن للادمن اضافه 50 حسابات (يمكنك تعديل ذالك من قسم الادمنيه)", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "echocode"):
            what_need_to_do_echo[str(update.message.chat.id)] = "anthercode"
            what_need_to_do_echo[str(
                update.message.chat.id)+"code"] = update.message.text
            await update.message.reply_text(f"ارسل رمز تحقق بخطوتين (اذا لم يكن هناك رمز ارسل اي شيء): ")
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "anthercode"):
            client = TelegramClient(f"echo_ac/{update.message.chat.id}/"+str(
                what_need_to_do_echo[str(update.message.chat.id)+":phone"]), API_ID, API_HASH, device_model="Devloper : @DaD22DD")
            await client.connect()
            try:
                await client.sign_in(phone=what_need_to_do_echo[str(update.message.chat.id)+":phone"], code=what_need_to_do_echo[str(update.message.chat.id)+"code"], phone_code_hash=what_need_to_do_echo[str(update.message.chat.id)+":phone_code_hash"])
                await update.message.reply_text(f"تم تسجيل الدخول بنجاح : "+str(what_need_to_do_echo[str(update.message.chat.id)+":phone"]), reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = ""
            except errors.SessionPasswordNeededError:
                await client.sign_in(password=update.message.text, phone_code_hash=what_need_to_do_echo[str(update.message.chat.id)+":phone_code_hash"])
                await update.message.reply_text(f"تم تسجيل الدخول بنجاح \n\n- "+str(what_need_to_do_echo[str(update.message.chat.id)+":phone"]), reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
                what_need_to_do_echo[str(update.message.chat.id)] = ""
            except Exception as e:
                await client.log_out()
                what_need_to_do_echo[str(update.message.chat.id)] = ""
                await update.message.reply_text(f"حدث خطأ غير متوقع: {str(e)}", reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ]))
            await client.disconnect()
        elif (what_need_to_do_echo[str(update.message.chat.id)].startswith("setlimt:")):
            admin = what_need_to_do_echo[str(
                update.message.chat.id)].split(":")[1]
            await update.message.reply_text(f"تم تعين عدد الحسابات المسموحه لهذه الادمن !\n\n- {admin}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="myadminsecho")],
            ]))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
            if "admins" not in info:
                info["admins"] = {}
            info["admins"][str(admin)] = str(update.message.text)
            with open("echo_data.json", "w") as json_file:
                json.dump(info, json_file)
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "runall"):
            await update.message.reply_text(f"ارسل ايدي الحساب الذي تريد التجميع له نقاط :\n\n- ارسل : انا : لارسال نقاط لهذه حسابك\n- ارسل : حساب : لارسال النقاط الى نفس الحساب", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            what_need_to_do_echo[str(update.message.chat.id)] = "runall2"
            what_need_to_do_echo[str(
                update.message.chat.id)+"code"] = update.message.text
        elif (what_need_to_do_echo[str(update.message.chat.id)] == "runall2"):
            await update.message.reply_text(f"تم بدء عملية التجميع بنجاح!", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            directory_path = Path(f"echo_ac/{update.message.chat.id}")
            file_list = [file.name for file in directory_path.iterdir(
            ) if file.is_file() and file.name.endswith('.session')]
            file_list = list(set(file_list))
            for filename in file_list:
                filename = filename.split(".")[0]
                start_background_task(
                    str(filename), str(what_need_to_do_echo[str(
                update.message.chat.id)+"code"]), str(update.message.chat.id), str(update.message.text))
            what_need_to_do_echo[str(update.message.chat.id)] = ""
        elif (what_need_to_do_echo[str(update.message.chat.id)].startswith("run:")):
            filename = what_need_to_do_echo[str(
                update.message.chat.id)].split(":")[1]
            await update.message.reply_text(f"ارسل ايدي الحساب الذي تريد التجميع له نقاط :\n\n- ارسل : انا : لارسال نقاط لهذه حسابك\n- ارسل : حساب : لارسال النقاط الى نفس الحساب", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            what_need_to_do_echo[str(update.message.chat.id)] = "run2:"+str(filename)
            what_need_to_do_echo[str(
                update.message.chat.id)+"code"] = update.message.text
        elif (what_need_to_do_echo[str(update.message.chat.id)].startswith("run2:")):
            filename = what_need_to_do_echo[str(
                update.message.chat.id)].split(":")[1]
            await update.message.reply_text(f"تم بدء العمل !\n\n- {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="sudohome")],
            ]))
            start_background_task(
                    str(filename), str(what_need_to_do_echo[str(
                update.message.chat.id)+"code"]), str(update.message.chat.id), str(update.message.text))
            what_need_to_do_echo[str(update.message.chat.id)] = ""


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global what_need_to_do_echo
    query = update.callback_query
    await query.answer()
    
    if not query.message or query.message.chat.type != "private":
        return 0
    
    if str(query.message.chat.id) != str(info["sudo"]) and str(query.message.chat.id) not in info["admins"]:
        return 0
    
    if query.data == "addecho":
        if str(query.message.chat.id) == str(info["sudo"]):
            
            what_need_to_do_echo[str(query.message.chat.id)] = query.data
            await query.edit_message_text(
                text="ارسل رقم الحساب الان :",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                ])
            )
        elif str(query.message.chat.id) in info["admins"]:
            directory_path = Path(f"echo_ac/{query.message.chat.id}")
            file_list = [
                file.name for file in directory_path.iterdir()
                if file.is_file() and file.name.endswith('.session')
            ]
            file_list = list(set(file_list))
            
            if int(len(file_list)) <= int(info["admins"][str(query.message.chat.id)]):
                what_need_to_do_echo[str(query.message.chat.id)] = query.data
                await query.edit_message_text(
                    text="ارسل رقم الحساب الان :",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                    ])
                )
            else:
                await query.edit_message_text(
                    text="لا يمكنك اضافه المزيد من الحسابات !",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("رجوع", callback_data="sudohome")],
                    ])
                )
    elif query.data == "leavechn":
        await query.edit_message_text(text=f"جار مغادرة القنوات", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        id = query.message.chat.id
        directory_path = Path(f"echo_ac/{id}")
        file_list = [
            file.name for file in directory_path.iterdir()
            if file.is_file() and file.name.endswith('.session')
        ]
        for file in file_list:
            print(file)
            file = file.replace('.session','')
            client = TelegramClient(
                f"echo_ac/{id}/{file}", API_ID, API_HASH, device_model="Devloper : @DaD22DD"
            )
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": id,
            "text": f"الرقم : {file} غير صالح"
    })
                    client.disconnect()
                else:
                    client.lang_code = 'ar'
                    await client.connect()
                    dialogs = await client.get_dialogs()
                    count = 0
                    for dialog in dialogs:
                        if dialog.is_channel:
                            await client(LeaveChannelRequest(dialog.entity))
                            count += 1
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": id,
            "text": f"الرقم : {file}\nتم مغادرة {count}"
    })
                    await client.disconnect()
            except Exception as e:
                print(f"حدث خطأ: {e}")
                await client.disconnect()
                
    elif query.data == "leavechnel":
        await query.edit_message_text(text="أدخل يوزر القناة التي تريد مغادرتها (بدون @):", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        id = query.message.chat.id

        @bot.message_handler(func=lambda message: True)
        async def handle_channel_username(message):
            if not message.text.startswith('@'):
                await bot.send_message(message.chat.id, "يرجى إدخال يوزر القناة بشكل صحيح، بدءاً بـ @")
                return

            channel_username = message.text
            directory_path = Path(f"echo_ac/{id}")
            file_list = [
                file.name for file in directory_path.iterdir()
                if file.is_file() and file.name.endswith('.session')
            ]
            for file in file_list:
                print(file)
                file = file.replace('.session', '')
                client = TelegramClient(
                    f"echo_ac/{id}/{file}", API_ID, API_HASH, device_model="Devloper : @DaD22DD"
                )
                try:
                    await client.connect()
                    if not await client.is_user_authorized():
                        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                            "chat_id": id,
                            "text": f"الرقم : {file} غير صالح"
                        })
                        await client.disconnect()
                    else:
                        client.lang_code = 'ar'
                        await client.connect()
                        try:
                            await client(LeaveChannelRequest(channel_username))
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": id,
                                "text": f"تم مغادرة القناة: {channel_username} للرقم: {file}"
                            })
                        except (ChannelInvalidError, UserNotParticipantError):
                            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                                "chat_id": id,
                                "text": f"خطأ: لا يمكن مغادرة القناة {channel_username}. قد تكون غير مشترك فيها أو القناة غير صالحة."
                            })
                        await client.disconnect()
                except Exception as e:
                    print(f"حدث خطأ: {e}")
                    await client.disconnect()

    elif query.data == "templer":
        await query.edit_message_text(text=f"حسنا جاري بدأ العملية", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        id = query.message.chat.id
        directory_path = Path(f"echo_ac/{id}")
        file_list = [
            file.name for file in directory_path.iterdir()
            if file.is_file() and file.name.endswith('.session')
        ]
        for file in file_list:
            print(file)
            file = file.replace('.session','')
            client = TelegramClient(
                f"echo_ac/{id}/{file}", API_ID, API_HASH, device_model="Devloper : @DaD22DD"
            )
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": id,
            "text": f"الرقم : {file} غير صالح"
    })
                    client.disconnect()
                else:
                    client.lang_code = 'ar'
                    await client.connect()
                    await temp(client)
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": id,
            "text": f"الرقم : {file}\nتم تحويله تمبلر"
    })
                    await client.disconnect()
            except Exception as e:
                print(f"حدث خطأ: {e}")
                await client.disconnect()
    elif query.data == "giftcode":
        await query.edit_message_text(text=f"حسنا جاري بدأ العملية", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        id = query.message.chat.id
        directory_path = Path(f"echo_ac/{id}")
        file_list = [
            file.name for file in directory_path.iterdir()
            if file.is_file() and file.name.endswith('.session')
        ]
        for file in file_list:
            print(file)
            file = file.replace('.session','')
            client = TelegramClient(
                f"echo_ac/{id}/{file}", API_ID, API_HASH, device_model="Devloper : @DaD22DD"
            )
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": id,
            "text": f"الرقم : {file} غير صالح"
    })
                    client.disconnect()
                else:
                        async for msg in client.iter_messages(777000):
                                if isinstance(msg.action, MessageActionGiftCode):
                                    m = msg.action
                                    months = m.months
                                    slug = m.slug

                                    
                                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": id, "text": f"الرقم : {file}\nفاز بالسحب\nالمدة : {months}\nالرابط : https://t.me/giftcode/{slug}"})

                    
                        await client.disconnect()
            except Exception as e:
                print(f"حدث خطأ: {e}")
                await client.disconnect()
#hello

    elif (query.data == "deladminecho"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        await query.edit_message_text(text=f"ارسل ايدي الادمن الان :", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif (query.data == "delall"):
    	await delall(query.message.chat.id)

    elif (query.data == "copynum"):
    	await copynum(query.message.chat.id)
    elif (query.data == "joinchn"):       
        await query.edit_message_text(text=f"ارسل الامر \n /join + يوزر القناة", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif (query.data == "addadminecho"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        await query.edit_message_text(text=f"ارسل ايدي الادمن الان :", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif (query.data == "sudohome"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (str(query.message.chat.id) == str(info["sudo"])):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضف رقم ➕", callback_data="addecho"),
                    InlineKeyboardButton(
                        "حذف رقم ➖", callback_data="delecho")
                ],
                [
                    InlineKeyboardButton("ارقامك 🗃", callback_data="myecho"),
                ],
                [
                    InlineKeyboardButton(
                        "تشغيل التجميع 🟢", callback_data="runall"),
                    InlineKeyboardButton(
                        "ايقاف التجميع 🔴", callback_data="stopall")
                ], 
                [
                    InlineKeyboardButton("اوامر تحويلات النقاط 🔃", callback_data="reloadcoin"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر الادمن 👨‍✈️", callback_data="anaaaaa"),
                    InlineKeyboardButton(
                        "تحويل تلمبر 🛗", callback_data="templer"),
                ], 
                [
                    InlineKeyboardButton(
                        "جلب مميز 🌟", callback_data='giftcode'),
                    InlineKeyboardButton(
                        "اوامر التحكم ⏺", callback_data='dellecho'),
                ],
                [
                    InlineKeyboardButton(
                        "جلب ملف الارقام 📥", callback_data="copynumper"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر المميز 🏅", callback_data="gifts"),
                ],
                [
                    InlineKeyboardButton(
                        "قناة المطور ⚜️", url="t.me/DaD22DD"),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبآ بك في بوت المخضرم.البوت مخصص بتجميع نقاط جميع البوتات وبخدمات ومنيزات رائعه داخل البوت\n\nDev : @DaD22DD", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "اضف رقم ➕", callback_data="addecho"),
                    InlineKeyboardButton(
                        "حذف رقم ➖", callback_data="delecho")
                ],
                [
                    InlineKeyboardButton("ارقامك 🗃", callback_data="myecho"),
                ],
                [
                    InlineKeyboardButton(
                        "تشغيل التجميع 🟢", callback_data="runall"),
                    InlineKeyboardButton(
                        "ايقاف التجميع 🔴", callback_data="stopall")
                ], 
                [
                    InlineKeyboardButton("اوامر تحويلات النقاط 🔃", callback_data="reloadcoin"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر الادمن 👨‍✈️", callback_data="anaaaaa"),
                    InlineKeyboardButton(
                        "تحويل تلمبر 🛗", callback_data="templer"),
                ], 
                [
                    InlineKeyboardButton(
                        "جلب مميز 🌟", callback_data='giftcode'),
                    InlineKeyboardButton(
                        "اوامر التحكم ⏺", callback_data='dellecho'),
                ],
                [
                    InlineKeyboardButton(
                        "جلب ملف الارقام 📥", callback_data="copynumper"),
                ],
                [
                    InlineKeyboardButton(
                        "اوامر المميز 🏅", callback_data="gifts"),
                ],
                [
                    InlineKeyboardButton(
                        "قناة المطور ⚜️", url="t.me/DaD22DD"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبآ بك في بوت المخضرم.البوت مخصص بتجميع نقاط جميع البوتات وبخدمات ومنيزات رائعه داخل البوت\n\nDev : @DaD22DD", reply_markup=reply_markup)
    elif (query.data == "dellecho"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (str(query.message.chat.id) == str(info["sudo"])):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة كل القنوات ⦆", callback_data="leavechn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة قناة ⦆", callback_data="leavechnel"),
                    InlineKeyboardButton("⦅ انضمام لقناة ⦆", callback_data="joinchn"),
                ],
                [
                    InlineKeyboardButton("⦅ سرعة التجميع ⦆", callback_data="sleeptime")
                ],
                [
                    InlineKeyboardButton(
                        "⦅ حذف الحسابات ⦆", callback_data="delall"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم التحكم\n\n• تحكم في حساباتك من هذا القسم", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة كل القنوات ⦆", callback_data="leavechn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة قناة ⦆", callback_data="leavechnel"),
                    InlineKeyboardButton("⦅ انضمام لقناة ⦆", callback_data="joinchn"),
                ],
                [
                    InlineKeyboardButton("⦅ سرعة التجميع ⦆", callback_data="sleeptime")
                ],
                [
                    InlineKeyboardButton(
                        "⦅ حذف الحسابات ⦆", callback_data="delall"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم الحسابات\n\n• تحكم في حساباتك من هذا القسم", reply_markup=reply_markup)
    elif (query.data == "copynumper"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (str(query.message.chat.id) == str(info["sudo"])):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ جلب نسخه احتياطيه ⦆", callback_data="copynum"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ رفع نسخه احتياطيه ⦆", callback_data="userbackup"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم النسخه الاحتياطيه", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ جلب نسخه احتياطيه ⦆", callback_data="copynum"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ رفع نسخه احتياطيه ⦆", callback_data="userbackup"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم النسخه الاحتياطيه", reply_markup=reply_markup)
    elif (query.data == "gifts"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (str(query.message.chat.id) == str(info["sudo"])):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ انضمام لـ قناه ⦆", callback_data="joinchn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة قناة ⦆", callback_data="leavechnel"),
                    InlineKeyboardButton(
                        "⦅ مغادرة القنوات ⦆", callback_data="leavechn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ جلب الروابط ⦆", callback_data="giftcode"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم جلب روابط المميز \n- انضم لقنوات وقم بجلب الروابط الذي ربحها احد الحسابات من زر جلب الروابط", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton(
                        "⦅ انضمام لـ قناه ⦆", callback_data="joinchn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ مغادرة قناة ⦆", callback_data="leavechnel"),
                    InlineKeyboardButton(
                        "⦅ مغادرة القنوات ⦆", callback_data="leavechn"),
                ],
                [
                    InlineKeyboardButton(
                        "⦅ جلب الروابط ⦆", callback_data="giftcode"),
                ],
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data="sudohome"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم جلب روابط المميز \n- انضم لقنوات وقم بجلب الروابط الذي ربحها احد الحسابات من زر جلب الروابط", reply_markup=reply_markup)
    elif (query.data == "anaaaaa"):
        what_need_to_do_echo[str(query.message.chat.id)] = ""
        if (str(query.message.chat.id) == str(info["sudo"])):
            keyboard = [
                [
                    InlineKeyboardButton("⦅ اضف ادمن ⦆", callback_data="addadminecho"),
                    InlineKeyboardButton("⦅ مسح ادمن ⦆", callback_data="deladminecho"),
                ],
                [
                InlineKeyboardButton("⦅ الادمنيه ⦆", callback_data="myadminsecho"),
                ], 
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data='sudohome'),
                ],
            ]
                    
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم ادمن البوت \n- للتحكم في عدد اضافة حسابات الادمن اضغط على ايدي الادمن", reply_markup=reply_markup)
        elif (str(query.message.chat.id) in info["admins"]):
            keyboard = [
                [
                    InlineKeyboardButton("⦅ اضف ادمن ⦆", callback_data="addadminecho"),
                    InlineKeyboardButton("⦅ مسح ادمن ⦆", callback_data="deladminecho"),
                ],
                [
                InlineKeyboardButton("⦅ الادمنيه ⦆", callback_data="myadminsecho"),
                ],
                [
                    InlineKeyboardButton(
                        "- رجــوع 🔙", callback_data="sudohome"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("مرحبا بك في قسم ادمن البوت \n- للتحكم في عدد اضافة حسابات الادمن اضغط على ايدي الادمن", reply_markup=reply_markup)
    elif (query.data == "userbackup"):
        await event.respond("ارسل ملف النسخه الاحتياطيه لرفعها الى ملفك 🚀 (ZIP)")
        @client.on(events.NewMessage(incoming=True))
        async def handle_received_backup(event):
            if event.message.file and event.message.file.name.endswith('.zip'):
                backup_path = f'backups/{event.message.file.name}'
                await event.download_media(backup_path)
                await event.reply("تمام، جاري فك الضغط...")

                temp_directory = f'temp/{event.sender_id}'
                os.makedirs(temp_directory, exist_ok=True)
                
                with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_directory)

                user_directory = f'echo_ac/{event.sender_id}'
                os.makedirs(user_directory, exist_ok=True)

                for root, dirs, files in os.walk(temp_directory):
                    for file in files:
                        shutil.move(os.path.join(root, file), user_directory)

                shutil.rmtree(temp_directory)

                await event.reply("تم رفع النسخه الاحتياطيه بنجاح ✅.")
            else:
                await event.reply("هذا الملف ليس .zip.")
    elif (query.data == "sleeptime"):
        await query.edit_message_text(f"يرجى إرسال العدد الذي ترغب فيه من الثواني لانتظار البوت للاشتراك في القناة التالية :", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="anaaaaa")],
        ]))
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
    elif (query.data == "myadminsecho"):
        if "admins" not in info:
            info["admins"] = {}
        keyboard = []
        for key, value in info["admins"].items():
            button = InlineKeyboardButton(
                f"{key}", callback_data=f"setlimt:{key}")
            button2 = InlineKeyboardButton(
                str(value), callback_data=f"setlimt:{key}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="anaaaaa")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الادمنيه في البوت : \n\n- اضغط على ايدي لتعديل عدد الحسابات المسموح ", reply_markup=reply_markup)
    elif query.data.startswith("setlimt:"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        admin = query.data.split(":")[1]
        await query.edit_message_text(f"ارسل عدد الحسابات المسموحه لهذه الشخص : \n\n- {admin}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="myadminsecho")],
        ]))
    elif (query.data == "delecho"):
        directory_path = Path(f"echo_ac/{query.message.chat.id}")
        file_list = [file.name for file in directory_path.iterdir(
        ) if file.is_file() and file.name.endswith('.session')]
        file_list = list(set(file_list))
        keyboard = []
        for filename in file_list:
            filename = filename.split(".")[0]
            button = InlineKeyboardButton(
                f"{filename}", callback_data=f"del:{filename}")
            button2 = InlineKeyboardButton(
                f"❌", callback_data=f"del:{filename}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="sudohome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الحسابات الخاصه بك : \n\n- اضغط على ❌ للمسح ", reply_markup=reply_markup)
    elif query.data.startswith("del:"):
        filename = query.data.split(":")[1]
        stop_background_task(filename, query.message.chat.id)
        try:
            client = TelegramClient(
                f"echo_ac/{query.message.chat.id}/{filename}", API_ID, API_HASH, device_model="Devloper : @DaD22DD")
            await client.connect()
            await client.log_out()
            await client.disconnect()
            what_need_to_do_echo[str(query.message.chat.id)] = ""
            await query.edit_message_text(f"تم تسجيل الخروج من رقم : {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="delecho")],
            ]))
        except:
            os.remove(f"echo_ac/{query.message.chat.id}/{filename}.session")
            await query.edit_message_text(f"لا يوجد هكذا رقم : {filename}", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="delecho")],
            ]))
    elif (query.data == "myecho"):
        directory_path = Path(f"echo_ac/{query.message.chat.id}")
        file_list = [file.name for file in directory_path.iterdir(
        ) if file.is_file() and file.name.endswith('.session')]
        file_list = list(set(file_list))
        keyboard = []
        if str(query.message.chat.id) not in running_processes:
            running_processes[str(query.message.chat.id)] = {}
        keyboard.append([InlineKeyboardButton(
            "تشغيل الكل", callback_data="runall"),InlineKeyboardButton(
            "ايقاف الكل", callback_data="stopall")])
        for filename in file_list:
            filename = filename.split(".")[0]
            if str(filename) in running_processes[str(query.message.chat.id)]:
                button = InlineKeyboardButton(
                    f"{filename}", callback_data=f"stop:{filename}")
                button2 = InlineKeyboardButton(
                    f"✅ | اضغط للايقاف", callback_data=f"stop:{filename}")
            else:
                button = InlineKeyboardButton(
                    f"{filename}", callback_data=f"run:{filename}")
                button2 = InlineKeyboardButton(
                    f"❌ | اضغط للتشغيل", callback_data=f"run:{filename}")
            keyboard.append([button, button2])
        keyboard.append([InlineKeyboardButton(
            "رجوع", callback_data="sudohome")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("الحسابات الخاصه بك : \n\n- ✅ = يعمل \n- ❌ = متوقف \n\nيمكنك تشغيل رقم من خلال امر :\n/run +201211000000\n لليقاف : \n/stop +201211000000", reply_markup=reply_markup)
    elif query.data == "runall":
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        await query.edit_message_text(f"ارسل معرف البوت الذي تريد لجميع الحسابات التجميع منه : ", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif query.data == "stopall":
        await query.edit_message_text(f"تم ايقاف عمل جميع الارقام !", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        stop_all_background_tasks(str(query.message.chat.id))
    elif query.data.startswith("run:"):
        what_need_to_do_echo[str(query.message.chat.id)] = query.data
        filename = query.data.split(":")[1]
        await query.edit_message_text(f"ارسل معرف البوت الذي تريد للحساب التجميع منه : \n\n- {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
    elif query.data.startswith("stop:"):
        filename = query.data.split(":")[1]
        await query.edit_message_text(f"تم ايقاف عمل الرقم : {filename}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="sudohome")],
        ]))
        stop_background_task(filename, query.message.chat.id)

    pass

async def temp(client):
    channel_username = 'Zqqqk'
    channel = await client.get_entity(channel_username)  
    posts = await client(GetHistoryRequest(peer=channel, limit=100, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
    photo_posts = [post for post in posts.messages if post.media and post.media.photo]
    random_photo_post = random.choice(photo_posts)
    photo = await client.download_media(random_photo_post.media.photo)
    print('ttt')
    pfile = await client.upload_file(photo)
    print('frhgt')
    await client(UploadProfilePhotoRequest(file=pfile))
    print('fryukloolllllooooogt')
    caption = random_photo_post.message
    first_name, bio = caption.split('\n', 1)
    await client(UpdateProfileRequest(first_name=first_name, about=bio))



def main() -> None:
    global what_need_to_do_echo
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, echoMaker))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()