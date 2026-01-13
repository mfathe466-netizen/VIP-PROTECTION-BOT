#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت استرجاع ملفات Python من الاستضافة
نسخة واحدة متكاملة
"""

import os
import json
import telebot
import logging
from datetime import datetime
from telebot import types
import zipfile
import io
import platform
import psutil

# ============= إعدادات البوت =============
TOKEN = "8560697098:AAEi5-YwdVEx7w79pWginwJPZ05rjWxxwK4"  # ضع توكن بوتك هنا
ADMIN_ID = 8326886483  # ضع ID الخاص بك هنا

# ============= تهيئة البوت =============
bot = telebot.TeleBot(TOKEN)

# ============= إعداد التسجيل =============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============= دوال البحث عن الملفات =============
def get_all_py_files(base_dir=None):
    """البحث عن جميع ملفات .py في المجلدات"""
    if base_dir is None:
        base_dir = os.getcwd()  # المسار الحالي
        
    py_files = []
    file_info = []
    
    logger.info(f"🔍 البحث في: {base_dir}")
    
    try:
        # البحث التكراري في جميع المجلدات
        for root, dirs, files in os.walk(base_dir):
            # استبعاد بعض المجلدات (اختياري)
            exclude_dirs = ['__pycache__', '.git', 'venv', 'env', 'node_modules', '.vscode']
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        # معلومات الملف
                        file_size = os.path.getsize(file_path)
                        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        # حساب المسار النسبي
                        relative_path = os.path.relpath(file_path, base_dir)
                        
                        py_files.append(file_path)
                        file_info.append({
                            'path': relative_path,
                            'size': file_size,
                            'modified': modified_time,
                            'full_path': file_path
                        })
                        
                    except Exception as e:
                        logger.error(f"خطأ في قراءة الملف {file_path}: {e}")
    
    except Exception as e:
        logger.error(f"خطأ في البحث عن الملفات: {e}")
    
    return py_files, file_info

def create_file_summary(file_info):
    """إنشاء ملخص للملفات التي تم العثور عليها"""
    if not file_info:
        return "لم يتم العثور على أي ملفات .py"
    
    summary = f"📊 **ملخص الملفات:**\n"
    summary += f"• العدد الإجمالي: {len(file_info)} ملف\n"
    
    # حجم الملفات
    total_size = sum(f['size'] for f in file_info)
    size_mb = total_size / (1024 * 1024)
    if size_mb > 1:
        summary += f"• الحجم الإجمالي: {size_mb:.2f} ميجابايت\n\n"
    else:
        summary += f"• الحجم الإجمالي: {total_size / 1024:.2f} كيلوبايت\n\n"
    
    # قائمة الملفات مع معلومات
    summary += "📁 **قائمة الملفات:**\n"
    for i, file in enumerate(file_info[:15], 1):  # أول 15 ملف فقط
        size_kb = file['size'] / 1024
        if size_kb > 1024:
            size_str = f"{size_kb/1024:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        summary += f"{i}. `{file['path']}` ({size_str})\n"
    
    if len(file_info) > 15:
        summary += f"\n... و {len(file_info) - 15} ملف آخر\n"
    
    return summary

def create_zip_from_files(py_files, file_info):
    """إنشاء أرشيف ZIP من الملفات"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path, info in zip(py_files, file_info):
            try:
                arcname = info['path']
                zipf.write(file_path, arcname)
            except Exception as e:
                logger.error(f"خطأ في إضافة الملف {file_path}: {e}")
    
    zip_buffer.seek(0)
    return zip_buffer

# ============= معالجة الأوامر =============
@bot.message_handler(commands=['start'])
def start_command(message):
    """بدء البوت"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا البوت للإدمن فقط")
        return
    
    markup = types.InlineKeyboardMarkup()
    
    # أزرار البحث في مسارات مختلفة
    current_dir_btn = types.InlineKeyboardButton('🔍 البحث في المسار الحالي', callback_data='scan_current')
    home_dir_btn = types.InlineKeyboardButton('🏠 البحث في /home', callback_data='scan_home')
    root_dir_btn = types.InlineKeyboardButton('💾 البحث في / (الجذر)', callback_data='scan_root')
    custom_dir_btn = types.InlineKeyboardButton('📂 بحث مخصص', callback_data='scan_custom')
    list_dirs_btn = types.InlineKeyboardButton('📁 عرض المجلدات', callback_data='list_dirs')
    
    markup.row(current_dir_btn)
    markup.row(home_dir_btn, root_dir_btn)
    markup.row(custom_dir_btn, list_dirs_btn)
    
    welcome_msg = (
        "🤖 **بوت استرجاع الملفات**\n\n"
        "هذا البوت يساعدك في استرجاع جميع ملفات Python (.py) من الاستضافة.\n\n"
        "اختر مكان البحث:"
    )
    
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['backup_all'])
def backup_all_command(message):
    """نسخ احتياطي لجميع ملفات .py"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا البوت للإدمن فقط")
        return
    
    bot.reply_to(message, "🔍 جاري البحث عن جميع ملفات Python في النظام...")
    
    # البحث في مسارات مختلفة
    search_paths = [
        os.getcwd(),  # المسار الحالي
        os.path.expanduser('~'),  # مجلد المستخدم
        '/var',  # مجلد var
        '/opt',  # مجلد opt
        '/home'  # مجلد home
    ]
    
    all_files = []
    all_info = []
    
    for path in search_paths:
        if os.path.exists(path):
            py_files, file_info = get_all_py_files(path)
            all_files.extend(py_files)
            all_info.extend(file_info)
    
    if not all_files:
        bot.send_message(message.chat.id, "❌ لم يتم العثور على أي ملفات .py")
        return
    
    # إنشاء أرشيف
    try:
        bot.send_chat_action(message.chat.id, 'upload_document')
        
        zip_buffer = create_zip_from_files(all_files, all_info)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"full_python_backup_{timestamp}.zip"
        
        summary = f"📦 **نسخة احتياطية كاملة**\n\n"
        summary += f"• إجمالي الملفات: {len(all_files)}\n"
        summary += f"• مجالات البحث: {len(search_paths)}\n"
        summary += f"• وقت الإنشاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        bot.send_document(
            message.chat.id,
            zip_buffer,
            visible_file_name=zip_name,
            caption=summary
        )
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
        bot.send_message(message.chat.id, f"❌ خطأ في إنشاء الأرشيف: {str(e)}")

@bot.message_handler(commands=['find_config'])
def find_config_command(message):
    """البحث عن ملفات تهيئة مهمة"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ هذا البوت للإدمن فقط")
        return
    
    bot.reply_to(message, "🔍 جاري البحث عن ملفات التهيئة...")
    
    config_files = []
    search_paths = [os.getcwd(), os.path.expanduser('~'), '/']
    
    config_patterns = [
        '*.py',
        'config*.py',
        'settings*.py',
        '*config*.json',
        '*settings*.json',
        '.env',
        'requirements.txt',
        'Procfile',
        'runtime.txt'
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=True):
                # استبعاد مجلدات كبيرة
                exclude_dirs = ['.git', '__pycache__', 'node_modules', 'venv', 'env']
                dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
                
                for file in files:
                    file_lower = file.lower()
                    if any(file_lower.endswith(pattern.replace('*', '')) for pattern in config_patterns):
                        file_path = os.path.join(root, file)
                        config_files.append(file_path)
    
    if not config_files:
        bot.send_message(message.chat.id, "❌ لم يتم العثور على ملفات تهيئة")
        return
    
    # إرسال قائمة الملفات
    file_list = "📋 **ملفات التهيئة التي تم العثور عليها:**\n\n"
    for i, file_path in enumerate(config_files[:15], 1):
        file_name = os.path.basename(file_path)
        file_list += f"{i}. `{file_name}`\n   `{file_path}`\n"
    
    if len(config_files) > 15:
        file_list += f"\n... و {len(config_files) - 15} ملف آخر"
    
    bot.send_message(message.chat.id, file_list, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    """عرض التعليمات"""
    help_text = """
🤖 **بوت استرجاع ملفات Python** - التعليمات

**الأوامر المتاحة:**
/start - بدء البوت وعرض القائمة
/backup_all - نسخة احتياطية لجميع ملفات .py في النظام
/find_config - البحث عن ملفات التهيئة المهمة
/help - عرض هذه التعليمات

**مميزات البوت:**
• البحث عن جميع ملفات .py في أي مجلد
• تحميل ملفات فردية أو مجمعة في أرشيف ZIP
• التنقل بين المجلدات
• عرض معلومات مفصلة عن الملفات
• دعم المسارات المختلفة (الحالي، /home، /، الخ)

**نصائح:**
1. ابدأ بـ `/start` للبحث في المسار الحالي
2. استخدم `/backup_all` لأخذ نسخة احتياطية شاملة
3. يمكنك التنقل بين المجلدات باستخدام الأزرار
4. الملفات الكبيرة ستضغط تلقائياً في أرشيف ZIP
"""
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# ============= معالجة Callback Queries =============
@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    """معالجة جميع Callback Queries"""
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ هذا البوت للإدمن فقط")
        return
    
    data = call.data
    
    if data.startswith('scan_'):
        handle_scan_callback(call)
    elif data == 'list_dirs':
        handle_list_dirs(call)
    elif data.startswith('enter_'):
        handle_enter_dir(call)
    elif data.startswith('file_'):
        handle_file_download(call)
    elif data.startswith('zip_'):
        handle_zip_download(call)
    elif data.startswith('download_'):
        handle_zip_download(call)
    elif data.startswith('scanpath_'):
        target_dir = data[9:]
        scan_directory(call.message, target_dir, call.message.message_id)

def handle_scan_callback(call):
    """معالجة طلب البحث"""
    scan_type = call.data.split('_')[1]
    
    if scan_type == 'current':
        target_dir = os.getcwd()
    elif scan_type == 'home':
        target_dir = os.path.expanduser('~')
    elif scan_type == 'root':
        target_dir = '/'
    elif scan_type == 'custom':
        bot.send_message(call.message.chat.id, "📂 أرسل المسار الذي تريد البحث فيه:")
        bot.register_next_step_handler(call.message, process_custom_scan)
        bot.answer_callback_query(call.id, "أدخل المسار المطلوب")
        return
    else:
        target_dir = scan_type
    
    bot.answer_callback_query(call.id, f"جار البحث في {target_dir}")
    scan_directory(call.message, target_dir, call.message.message_id)

def process_custom_scan(message):
    """معالجة المسار المخصص"""
    target_dir = message.text.strip()
    
    if not os.path.exists(target_dir):
        bot.send_message(message.chat.id, f"❌ المسار `{target_dir}` غير موجود")
        return
    
    if not os.path.isdir(target_dir):
        bot.send_message(message.chat.id, f"❌ `{target_dir}` ليس مجلد")
        return
    
    bot.send_message(message.chat.id, f"🔍 جاري البحث في `{target_dir}`...")
    scan_directory(message, target_dir)

def handle_list_dirs(call):
    """عرض المجلدات المتاحة"""
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    
    try:
        # عرض المجلدات الفرعية
        items = os.listdir(current_dir)
        dirs = [d for d in items if os.path.isdir(os.path.join(current_dir, d))]
        files = [f for f in items if os.path.isfile(os.path.join(current_dir, f))]
        
        markup = types.InlineKeyboardMarkup()
        
        # زر الانتقال للأعلى
        if parent_dir != current_dir:
            markup.add(types.InlineKeyboardButton('⬆️ المجلد الأعلى', callback_data=f'enter_{parent_dir}'))
        
        # عرض المجلدات
        for directory in dirs[:15]:  # أول 15 مجلد فقط
            full_path = os.path.join(current_dir, directory)
            btn_text = f"📁 {directory}"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f'enter_{full_path}'))
        
        # زر البحث في هذا المجلد
        markup.add(types.InlineKeyboardButton('🔍 بحث هنا', callback_data=f'scan_{current_dir}'))
        
        info_msg = (
            f"📁 **المسار الحالي:** `{current_dir}`\n\n"
            f"📂 **المجلدات:** {len(dirs)}\n"
            f"📄 **الملفات:** {len(files)}\n\n"
            f"اختر مجلد للدخول إليه:"
        )
        
        bot.edit_message_text(
            info_msg,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"خطأ: {str(e)}")

def handle_enter_dir(call):
    """الدخول إلى مجلد"""
    target_dir = call.data[6:]  # إزالة 'enter_'
    
    if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        bot.answer_callback_query(call.id, "المجلد غير موجود")
        return
    
    try:
        # عرض محتويات المجلد الجديد
        items = os.listdir(target_dir)
        dirs = [d for d in items if os.path.isdir(os.path.join(target_dir, d))]
        files = [f for f in items if os.path.isfile(os.path.join(target_dir, f))]
        
        markup = types.InlineKeyboardMarkup()
        
        # زر الانتقال للأعلى
        parent_dir = os.path.dirname(target_dir)
        if parent_dir != target_dir:
            markup.add(types.InlineKeyboardButton('⬆️ المجلد الأعلى', callback_data=f'enter_{parent_dir}'))
        
        # عرض المجلدات
        for directory in dirs[:15]:  # أول 15 مجلد فقط
            full_path = os.path.join(target_dir, directory)
            btn_text = f"📁 {directory}"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f'enter_{full_path}'))
        
        # أزرار التحكم
        markup.add(types.InlineKeyboardButton('🔍 بحث هنا', callback_data=f'scan_{target_dir}'))
        markup.add(types.InlineKeyboardButton('📦 تحميل ملفات .py', callback_data=f'download_{target_dir}'))
        
        info_msg = (
            f"📁 **المسار الحالي:** `{target_dir}`\n\n"
            f"📂 **المجلدات:** {len(dirs)}\n"
            f"📄 **الملفات:** {len(files)}\n\n"
            f"اختر مجلد للدخول إليه أو:"
        )
        
        bot.edit_message_text(
            info_msg,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"خطأ: {str(e)}")

def scan_directory(message, target_dir, message_id=None):
    """البحث عن ملفات .py في مجلد"""
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # البحث عن الملفات
        py_files, file_info = get_all_py_files(target_dir)
        
        if not py_files:
            msg_text = f"❌ لم يتم العثور على أي ملفات .py في `{target_dir}`"
            if message_id:
                bot.edit_message_text(msg_text, message.chat.id, message_id, parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, msg_text, parse_mode='Markdown')
            return
        
        # إنشاء الملخص
        summary = create_file_summary(file_info)
        
        # إنشاء أزرار التحكم
        markup = types.InlineKeyboardMarkup()
        
        # خيارات التحميل
        markup.add(types.InlineKeyboardButton('📦 تحميل جميع الملفات (ZIP)', callback_data=f'zip_{target_dir}'))
        
        # زر إعادة البحث
        markup.add(types.InlineKeyboardButton('🔄 بحث في مسار آخر', callback_data='scan_current'))
        
        # رسالة النتيجة
        result_msg = f"✅ **تم العثور على {len(py_files)} ملف .py**\n\n{summary}"
        
        if message_id:
            bot.edit_message_text(
                result_msg,
                message.chat.id,
                message_id,
                reply_markup=markup,
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                message.chat.id,
                result_msg,
                reply_markup=markup,
                parse_mode='Markdown'
            )
        
    except Exception as e:
        logger.error(f"خطأ في البحث: {e}")
        error_msg = f"❌ حدث خطأ أثناء البحث: {str(e)}"
        if message_id:
            bot.edit_message_text(error_msg, message.chat.id, message_id)
        else:
            bot.send_message(message.chat.id, error_msg)

def handle_file_download(call):
    """تحميل ملف فردي"""
    file_path = call.data[5:]  # إزالة 'file_'
    
    if not os.path.exists(file_path):
        bot.answer_callback_query(call.id, "الملف غير موجود")
        return
    
    try:
        bot.answer_callback_query(call.id, "جار تحميل الملف...")
        
        with open(file_path, 'rb') as file:
            file_name = os.path.basename(file_path)
            bot.send_document(call.message.chat.id, file, caption=f"📄 {file_name}")
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"خطأ: {str(e)[:50]}")
        logger.error(f"خطأ في تحميل الملف {file_path}: {e}")

def handle_zip_download(call):
    """تحميل جميع الملفات كأرشيف ZIP"""
    target_dir = call.data[4:] if call.data.startswith('zip_') else call.data[9:]
    
    try:
        bot.answer_callback_query(call.id, "جار إنشاء الأرشيف...")
        bot.send_chat_action(call.message.chat.id, 'upload_document')
        
        # البحث عن الملفات
        py_files, file_info = get_all_py_files(target_dir)
        
        if not py_files:
            bot.send_message(call.message.chat.id, "❌ لم يتم العثور على ملفات لتحميلها")
            return
        
        # إنشاء الأرشيف
        zip_buffer = create_zip_from_files(py_files, file_info)
        
        # اسم الأرشيف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"python_backup_{timestamp}.zip"
        
        # إرسال الأرشيف
        bot.send_document(
            call.message.chat.id,
            zip_buffer,
            visible_file_name=zip_name,
            caption=f"📦 **أرشيف ملفات Python**\n\n"
                   f"• عدد الملفات: {len(py_files)}\n"
                   f"• المسار: `{target_dir}`\n"
                   f"• وقت الإنشاء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء الأرشيف: {e}")
        bot.answer_callback_query(call.id, f"خطأ: {str(e)[:50]}")

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """معالجة الرسائل غير المعروفة"""
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "🤔 لم أفهم الرسالة. استخدم /start للبدء")
    else:
        bot.reply_to(message, "⛔ هذا البوت للإدمن فقط")

# ============= تشغيل البوت =============
def display_system_info():
    """عرض معلومات النظام"""
    current_dir = os.getcwd()
    logger.info("🚀 بدء تشغيل بوت استرجاع الملفات...")
    logger.info(f"📁 المسار الحالي: {current_dir}")
    
    try:
        system_info = f"""
🖥️ **معلومات النظام:**
• النظام: {platform.system()} {platform.release()}
• المسار الحالي: {current_dir}
• معالج: {platform.processor()}
        """
        
        # معلومات المساحة
        try:
            disk_usage = psutil.disk_usage('/')
            system_info += f"• المساحة الكلية: {disk_usage.total // (1024**3)} GB\n"
            system_info += f"• المساحة المستخدمة: {disk_usage.used // (1024**3)} GB\n"
            system_info += f"• المساحة الحرة: {disk_usage.free // (1024**3)} GB"
        except:
            pass
            
        logger.info(system_info)
    except Exception as e:
        logger.error(f"خطأ في عرض معلومات النظام: {e}")

if __name__ == '__main__':
    display_system_info()
    
    print("=" * 50)
    print("🤖 بوت استرجاع ملفات Python جاهز للعمل")
    print("=" * 50)
    print(f"👤 الأدمن: {ADMIN_ID}")
    print(f"📁 المسار الحالي: {os.getcwd()}")
    print("=" * 50)
    print("📝 الأوامر المتاحة:")
    print("  /start - بدء البوت")
    print("  /backup_all - نسخة احتياطية كاملة")
    print("  /find_config - البحث عن ملفات تهيئة")
    print("  /help - المساعدة")
    print("=" * 50)
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("\n🛑 إيقاف البوت...")
        logger.info("إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}")
        print(f"❌ خطأ: {e}")