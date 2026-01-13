
import os, telebot, requests, base64, zipfile, json
from datetime import datetime

bot = telebot.TeleBot("8268817683:AAGNU1p5v3kTchNvLX2ukqruJLujBGhSTa8")
GITHUB_TOKEN = "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"
GITHUB_USER = "mfathe466-netizen"
GITHUB_REPO = "MR"

def upload_to_github(file_path):
    file_name = os.path.basename(file_path)
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{file_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        get_res = requests.get(url, headers=headers)
        sha = get_res.json().get('sha') if get_res.status_code == 200 else None
        data = {"message": f"Bot Upload {datetime.now().strftime('%H:%M')}", "content": content}
        if sha: data["sha"] = sha
        res = requests.put(url, data=json.dumps(data), headers=headers)
        return f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/raw/main/{file_name}" if res.status_code in [200, 201] else None
    except: return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 أهلاً يا مصري! ارسل لي أي ملف وسأرفعه لك على GitHub MR كملف ZIP.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    msg = bot.reply_to(message, "⏳ جاري المعالجة...")
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    orig_name = message.document.file_name
    zip_name = "VIP_UPLOAD.zip"
    with open(orig_name, 'wb') as f: f.write(downloaded)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z: z.write(orig_name)
    link = upload_to_github(zip_name)
    if link: bot.edit_message_text(f"✅ تم الرفع!\n🔗 الرابط:\n`{link}`", message.chat.id, msg.message_id, parse_mode='Markdown')
    else: bot.edit_message_text("❌ فشل الرفع.", message.chat.id, msg.message_id)
    for f in [orig_name, zip_name]: 
        if os.path.exists(f): os.remove(f)

print("Bot is alive...")
bot.infinity_polling()
