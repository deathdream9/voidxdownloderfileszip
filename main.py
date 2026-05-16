import os
import telebot
from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True
import yt_dlp
import requests
import threading
import time
import random
import string
import hashlib
import base64
import json
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

OWNER = "DEATH DREAM"
BOT_NAME = "voidxdownloder"
CHANNEL_TG = "https://t.me/HACKERQUEEN9"
CHANNEL_TG_ID = "@HACKERQUEEN9"
CHANNEL_WA = "https://whatsapp.com/channel/0029Vb7MViI0VycACP8CUI32"
OWNER_ID = None  # Will be set on first /setowner command

HACKER_FONT = {
    'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽',
    'G': '𝔾', 'H': 'ℍ', 'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃',
    'M': '𝕄', 'N': 'ℕ', 'O': '𝕆', 'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ',
    'S': '𝕊', 'T': '𝕋', 'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏',
    'Y': '𝕐', 'Z': 'ℤ',
    'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗',
    'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝',
    'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣',
    's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩',
    'y': '𝕪', 'z': '𝕫'
}

def hacker_text(text):
    return ''.join(HACKER_FONT.get(c, c) for c in text)

WELCOME_ART = """
╔══════════════════════════════╗
║   𝕧𝕠𝕚𝕕𝕩𝕕𝕠𝕨𝕟𝕝𝕠𝕕𝕖𝕣   ║
╚══════════════════════════════╝
"""

def check_channel_membership(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_TG_ID, user_id)
        return status.status in ['member', 'administrator', 'creator']
    except:
        return False

def channel_join_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Join Telegram Channel", url=CHANNEL_TG))
    markup.add(InlineKeyboardButton("📱 Join WhatsApp Channel", url=CHANNEL_WA))
    markup.add(InlineKeyboardButton("✅ I Joined - Check Again", callback_data="check_join"))
    return markup

def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎵 TikTok", callback_data="menu_tiktok"),
        InlineKeyboardButton("📺 YouTube", callback_data="menu_youtube"),
        InlineKeyboardButton("📸 Instagram", callback_data="menu_instagram"),
        InlineKeyboardButton("👤 Facebook", callback_data="menu_facebook"),
        InlineKeyboardButton("🔧 Hacker Tools", callback_data="menu_hacker"),
        InlineKeyboardButton("🛠️ Random Tools", callback_data="menu_tools"),
        InlineKeyboardButton("ℹ️ Help", callback_data="menu_help"),
        InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin"),
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not check_channel_membership(user_id):
        bot.send_message(
            message.chat.id,
            f"""⛔ *Access Denied!*

{WELCOME_ART}

To use *{hacker_text('voidxdownloder')}*, you must join our channels first!

📢 Join Telegram + WhatsApp channel then click ✅ below.""",
            parse_mode="Markdown",
            reply_markup=channel_join_markup()
        )
        return
    send_welcome(message.chat.id, message.from_user.first_name)

def send_welcome(chat_id, name):
    welcome_msg = f"""
{WELCOME_ART}
🖤 *Welcome to {hacker_text('voidxdownloder')}* 🖤

👋 Hello *{name}*!

━━━━━━━━━━━━━━━━━━━━
🎯 *Download videos WITHOUT watermark from:*
▸ TikTok | YouTube | Instagram | Facebook

⚡ *Special Features:*
▸ 🔓 Password Generator
▸ 🌐 IP Tracker
▸ 📡 Port Scanner Info
▸ 🔐 Hash Cracker
▸ 🕵️ Username Lookup
▸ 💀 Fake Identity Generator
▸ 🔑 Base64 Encode/Decode
▸ 📊 And 15+ more tools!

━━━━━━━━━━━━━━━━━━━━
👑 *Owner:* {hacker_text(OWNER)}
📢 *Channel:* {CHANNEL_TG}

🔰 *Use /help for all commands*
━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(chat_id, welcome_msg, parse_mode="Markdown", reply_markup=main_menu_markup())

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    user_id = call.from_user.id
    if check_channel_membership(user_id):
        bot.answer_callback_query(call.id, "✅ Verified! Welcome!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message.chat.id, call.from_user.first_name)
    else:
        bot.answer_callback_query(call.id, "❌ Please join the channel first!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def menu_callback(call):
    action = call.data.replace("menu_", "")
    if action == "tiktok":
        bot.send_message(call.message.chat.id, "🎵 *TikTok Downloader*\n\nSend me a TikTok video link!\nExample: `https://www.tiktok.com/@user/video/123`", parse_mode="Markdown")
    elif action == "youtube":
        bot.send_message(call.message.chat.id, "📺 *YouTube Downloader*\n\nSend me a YouTube link!\nExample: `https://youtu.be/xxxxx`", parse_mode="Markdown")
    elif action == "instagram":
        bot.send_message(call.message.chat.id, "📸 *Instagram Downloader*\n\nSend me an Instagram post/reel link!\nExample: `https://www.instagram.com/p/xxxxx`", parse_mode="Markdown")
    elif action == "facebook":
        bot.send_message(call.message.chat.id, "👤 *Facebook Downloader*\n\nSend me a Facebook video link!", parse_mode="Markdown")
    elif action == "hacker":
        show_hacker_tools(call.message.chat.id)
    elif action == "tools":
        show_random_tools(call.message.chat.id)
    elif action == "help":
        send_help(call.message.chat.id)
    elif action == "admin":
        send_admin_panel(call.message.chat.id, call.from_user.id)
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    send_help(message.chat.id)

def send_help(chat_id):
    help_text = """
╔══════════════════════════╗
║      𝕳𝕰𝕷𝕻 𝕄𝔼ℕ𝕌      ║
╚══════════════════════════╝

📥 *VIDEO DOWNLOADERS:*
/tiktok - TikTok video downloader
/youtube - YouTube video downloader
/instagram - Instagram downloader
/facebook - Facebook video downloader

🔧 *HACKER TOOLS:*
/ip <ip> - IP Address Tracker
/portscan <host> - Port Scanner Info
/hash <text> - Generate Hash (MD5/SHA)
/decode <b64> - Base64 Decode
/encode <text> - Base64 Encode
/passgen <length> - Password Generator
/username <name> - Username Availability
/whoami - Your Info Lookup
/fakeid - Fake Identity Generator
/phish - Phishing Awareness Tool

🛠️ *RANDOM TOOLS:*
/calc <expr> - Calculator
/weather <city> - Weather Info
/joke - Random Hacker Joke
/quote - Hacker Quote
/coin - Coin Flip
/dice - Roll Dice
/uuid - Generate UUID
/qr <text> - QR Code Generator
/short <url> - URL Shortener
/ping <host> - Ping Tool
/time - World Time Zones
/crypto - Crypto Prices
/wiki <topic> - Wikipedia Search
/color - Random Color Code
/fact - Random Tech Fact
/ascii <text> - ASCII Art Text
/morse <text> - Morse Code
/binary <text> - Text to Binary
/hex <text> - Text to Hex
/reverse <text> - Reverse Text

👑 *ADMIN COMMANDS:*
/setowner - Set yourself as owner
/broadcast <msg> - Broadcast message
/stats - Bot statistics
/ban <user_id> - Ban a user
/unban <user_id> - Unban a user

━━━━━━━━━━━━━━━━━━━━
👑 Owner: """ + hacker_text(OWNER) + """
📢 Channel: @HACKERQUEEN9
"""
    bot.send_message(chat_id, help_text, parse_mode="Markdown")

def show_hacker_tools(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🌐 IP Tracker", callback_data="tool_ip"),
        InlineKeyboardButton("🔐 Hash Gen", callback_data="tool_hash"),
        InlineKeyboardButton("🔑 Base64", callback_data="tool_b64"),
        InlineKeyboardButton("🔓 PassGen", callback_data="tool_pass"),
        InlineKeyboardButton("🕵️ Username Lookup", callback_data="tool_user"),
        InlineKeyboardButton("💀 Fake ID", callback_data="tool_fakeid"),
        InlineKeyboardButton("📡 Port Info", callback_data="tool_port"),
        InlineKeyboardButton("⚡ Phish Info", callback_data="tool_phish"),
    )
    bot.send_message(chat_id, """
💀 *HACKER TOOLS MENU* 💀
━━━━━━━━━━━━━━━━━━━━
Select a tool or use commands directly:

🔧 Available: /ip /hash /encode /decode /passgen /username /fakeid /whoami /phish
━━━━━━━━━━━━━━━━━━━━
""", parse_mode="Markdown", reply_markup=markup)

def show_random_tools(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎲 Dice", callback_data="rtool_dice"),
        InlineKeyboardButton("🪙 Coin", callback_data="rtool_coin"),
        InlineKeyboardButton("😂 Joke", callback_data="rtool_joke"),
        InlineKeyboardButton("💬 Quote", callback_data="rtool_quote"),
        InlineKeyboardButton("🌈 Color", callback_data="rtool_color"),
        InlineKeyboardButton("💡 Fact", callback_data="rtool_fact"),
        InlineKeyboardButton("🆔 UUID", callback_data="rtool_uuid"),
        InlineKeyboardButton("⏰ Time", callback_data="rtool_time"),
    )
    bot.send_message(chat_id, """
🛠️ *RANDOM TOOLS MENU* 🛠️
━━━━━━━━━━━━━━━━━━━━
Quick fun & utility tools!

More: /calc /wiki /ascii /morse /binary /hex /reverse /crypto
━━━━━━━━━━━━━━━━━━━━
""", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("rtool_"))
def rtool_callback(call):
    action = call.data.replace("rtool_", "")
    if action == "dice":
        result = random.randint(1, 6)
        bot.send_message(call.message.chat.id, f"🎲 *Dice Roll Result:* `{result}`", parse_mode="Markdown")
    elif action == "coin":
        result = random.choice(["Heads 🪙", "Tails 🔄"])
        bot.send_message(call.message.chat.id, f"🪙 *Coin Flip:* `{result}`", parse_mode="Markdown")
    elif action == "joke":
        send_joke(call.message.chat.id)
    elif action == "quote":
        send_quote(call.message.chat.id)
    elif action == "color":
        send_color(call.message.chat.id)
    elif action == "fact":
        send_fact(call.message.chat.id)
    elif action == "uuid":
        import uuid
        uid = str(uuid.uuid4())
        bot.send_message(call.message.chat.id, f"🆔 *Generated UUID:*\n`{uid}`", parse_mode="Markdown")
    elif action == "time":
        send_time(call.message.chat.id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tool_"))
def tool_callback(call):
    action = call.data.replace("tool_", "")
    if action == "ip":
        bot.send_message(call.message.chat.id, "🌐 *IP Tracker*\nUsage: `/ip <ip_address>`\nExample: `/ip 8.8.8.8`", parse_mode="Markdown")
    elif action == "hash":
        bot.send_message(call.message.chat.id, "🔐 *Hash Generator*\nUsage: `/hash <text>`\nExample: `/hash hello world`", parse_mode="Markdown")
    elif action == "b64":
        bot.send_message(call.message.chat.id, "🔑 *Base64*\nEncode: `/encode <text>`\nDecode: `/decode <base64>`", parse_mode="Markdown")
    elif action == "pass":
        bot.send_message(call.message.chat.id, "🔓 *Password Generator*\nUsage: `/passgen <length>`\nExample: `/passgen 16`", parse_mode="Markdown")
    elif action == "user":
        bot.send_message(call.message.chat.id, "🕵️ *Username Lookup*\nUsage: `/username <name>`\nExample: `/username hacker123`", parse_mode="Markdown")
    elif action == "fakeid":
        generate_fake_id(call.message.chat.id)
    elif action == "port":
        bot.send_message(call.message.chat.id, "📡 *Port Scanner Info*\nUsage: `/portscan <host>`\nExample: `/portscan google.com`", parse_mode="Markdown")
    elif action == "phish":
        send_phish_info(call.message.chat.id)
    bot.answer_callback_query(call.id)

# ══════════════════════════════════════
# VIDEO DOWNLOADERS
# ══════════════════════════════════════

def download_video(url, chat_id, platform):
    msg = bot.send_message(chat_id, f"⏳ *Downloading from {platform}...*\nPlease wait!", parse_mode="Markdown")
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '/tmp/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            title = info.get('title', 'Video')

        bot.edit_message_text(f"✅ *Downloaded!* Sending now...", chat_id, msg.message_id, parse_mode="Markdown")

        with open(file_path, 'rb') as video:
            bot.send_video(
                chat_id, video,
                caption=f"🎬 *{title}*\n\n📥 Downloaded by {hacker_text('voidxdownloder')}\n👑 Owner: {hacker_text(OWNER)}\n📢 {CHANNEL_TG}",
                parse_mode="Markdown"
            )
        os.remove(file_path)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ *Download Failed!*\nError: `{str(e)[:200]}`\n\nMake sure the link is valid and public.", chat_id, msg.message_id, parse_mode="Markdown")

@bot.message_handler(commands=['tiktok'])
def tiktok_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "🎵 *TikTok Downloader*\nUsage: `/tiktok <url>`\nExample: `/tiktok https://vm.tiktok.com/xxxxx`", parse_mode="Markdown")
        return
    threading.Thread(target=download_video, args=(args[1].strip(), message.chat.id, "TikTok")).start()

@bot.message_handler(commands=['youtube'])
def youtube_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "📺 *YouTube Downloader*\nUsage: `/youtube <url>`\nExample: `/youtube https://youtu.be/xxxxx`", parse_mode="Markdown")
        return
    threading.Thread(target=download_video, args=(args[1].strip(), message.chat.id, "YouTube")).start()

@bot.message_handler(commands=['instagram'])
def instagram_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "📸 *Instagram Downloader*\nUsage: `/instagram <url>`\nExample: `/instagram https://www.instagram.com/p/xxxxx`", parse_mode="Markdown")
        return
    threading.Thread(target=download_video, args=(args[1].strip(), message.chat.id, "Instagram")).start()

@bot.message_handler(commands=['facebook'])
def facebook_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "👤 *Facebook Downloader*\nUsage: `/facebook <url>`", parse_mode="Markdown")
        return
    threading.Thread(target=download_video, args=(args[1].strip(), message.chat.id, "Facebook")).start()

# Auto detect URL
@bot.message_handler(func=lambda m: m.text and ('tiktok.com' in m.text or 'youtu' in m.text or 'instagram.com' in m.text or 'facebook.com' in m.text or 'fb.watch' in m.text))
def auto_download(message):
    if not check_channel_membership(message.from_user.id):
        bot.reply_to(message, "⛔ Join our channel first!", reply_markup=channel_join_markup())
        return
    url = message.text.strip()
    platform = "Video"
    if 'tiktok' in url: platform = "TikTok"
    elif 'youtu' in url: platform = "YouTube"
    elif 'instagram' in url: platform = "Instagram"
    elif 'facebook' in url or 'fb.watch' in url: platform = "Facebook"
    threading.Thread(target=download_video, args=(url, message.chat.id, platform)).start()

# ══════════════════════════════════════
# HACKER TOOLS
# ══════════════════════════════════════

@bot.message_handler(commands=['ip'])
def ip_tracker(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/ip <ip_address>`\nExample: `/ip 8.8.8.8`", parse_mode="Markdown")
        return
    ip = args[1].strip()
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if r['status'] == 'success':
            result = f"""
🌐 *IP TRACKER RESULT*
━━━━━━━━━━━━━━━━━━
🎯 *IP:* `{r.get('query', 'N/A')}`
🌍 *Country:* {r.get('country', 'N/A')} {r.get('countryCode', '')}
🏙️ *City:* {r.get('city', 'N/A')}
📍 *Region:* {r.get('regionName', 'N/A')}
📮 *ZIP:* {r.get('zip', 'N/A')}
📡 *ISP:* {r.get('isp', 'N/A')}
🏢 *Org:* {r.get('org', 'N/A')}
🗺️ *Lat/Lon:* {r.get('lat', 'N/A')}, {r.get('lon', 'N/A')}
⏰ *Timezone:* {r.get('timezone', 'N/A')}
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
            bot.reply_to(message, result, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Invalid IP address or private IP.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: `{str(e)}`", parse_mode="Markdown")

@bot.message_handler(commands=['whoami'])
def whoami(message):
    user = message.from_user
    result = f"""
🕵️ *YOUR INFO LOOKUP*
━━━━━━━━━━━━━━━━━━
🆔 *User ID:* `{user.id}`
👤 *Name:* {user.first_name} {user.last_name or ''}
📛 *Username:* @{user.username or 'None'}
🌐 *Language:* {user.language_code or 'Unknown'}
🤖 *Is Bot:* {user.is_bot}
💬 *Chat ID:* `{message.chat.id}`
📱 *Chat Type:* {message.chat.type}
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
    bot.reply_to(message, result, parse_mode="Markdown")

@bot.message_handler(commands=['hash'])
def hash_gen(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/hash <text>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha1 = hashlib.sha1(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    sha512 = hashlib.sha512(text.encode()).hexdigest()
    result = f"""
🔐 *HASH GENERATOR*
━━━━━━━━━━━━━━━━━━
📝 *Input:* `{text}`

🔑 *MD5:*
`{md5}`

🔒 *SHA1:*
`{sha1}`

🛡️ *SHA256:*
`{sha256}`

💀 *SHA512:*
`{sha512}`
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
    bot.reply_to(message, result, parse_mode="Markdown")

@bot.message_handler(commands=['encode'])
def b64_encode(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/encode <text>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    encoded = base64.b64encode(text.encode()).decode()
    bot.reply_to(message, f"🔑 *Base64 Encoded:*\n`{encoded}`", parse_mode="Markdown")

@bot.message_handler(commands=['decode'])
def b64_decode(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/decode <base64>`", parse_mode="Markdown")
        return
    try:
        decoded = base64.b64decode(args[1].strip()).decode()
        bot.reply_to(message, f"🔓 *Base64 Decoded:*\n`{decoded}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid Base64 string!")

@bot.message_handler(commands=['passgen'])
def passgen(message):
    args = message.text.split(' ', 1)
    length = 16
    if len(args) > 1:
        try:
            length = int(args[1].strip())
            if length > 64: length = 64
            if length < 4: length = 4
        except:
            pass
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ''.join(random.choice(chars) for _ in range(length))
    result = f"""
🔓 *PASSWORD GENERATOR*
━━━━━━━━━━━━━━━━━━
📏 *Length:* {length}
🔑 *Password:*
`{password}`

💪 *Strength:* {'🟢 Strong' if length >= 12 else '🟡 Medium' if length >= 8 else '🔴 Weak'}
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
    bot.reply_to(message, result, parse_mode="Markdown")

@bot.message_handler(commands=['username'])
def username_lookup(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/username <name>`", parse_mode="Markdown")
        return
    name = args[1].strip()
    platforms = {
        "GitHub": f"https://github.com/{name}",
        "Twitter/X": f"https://twitter.com/{name}",
        "Instagram": f"https://instagram.com/{name}",
        "TikTok": f"https://tiktok.com/@{name}",
        "Reddit": f"https://reddit.com/u/{name}",
        "YouTube": f"https://youtube.com/@{name}",
        "Telegram": f"https://t.me/{name}",
        "Pinterest": f"https://pinterest.com/{name}",
    }
    result = f"🕵️ *Username Lookup: `{name}`*\n━━━━━━━━━━━━━━━━━━\n"
    for platform, url in platforms.items():
        result += f"▸ [{platform}]({url})\n"
    result += f"\n━━━━━━━━━━━━━━━━━━\n🔰 {hacker_text('voidxdownloder')}"
    bot.reply_to(message, result, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['fakeid'])
def fakeid_cmd(message):
    generate_fake_id(message.chat.id)

def generate_fake_id(chat_id):
    first_names = ["Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley", "Dakota", "Skyler", "Avery", "Quinn"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]
    cities = ["New York", "London", "Tokyo", "Berlin", "Paris", "Sydney", "Toronto", "Dubai", "Singapore", "Mumbai"]
    emails = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "proton.me"]

    fname = random.choice(first_names)
    lname = random.choice(last_names)
    age = random.randint(18, 65)
    city = random.choice(cities)
    email = f"{fname.lower()}.{lname.lower()}{random.randint(100,999)}@{random.choice(emails)}"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    dob = f"{random.randint(1960,2005)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    ssn = f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    cc = f"{random.randint(4000,4999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

    result = f"""
💀 *FAKE IDENTITY GENERATOR*
━━━━━━━━━━━━━━━━━━
👤 *Name:* {fname} {lname}
🎂 *DOB:* {dob} (Age: {age})
🏙️ *City:* {city}
📧 *Email:* `{email}`
📱 *Phone:* `{phone}`
🪪 *SSN (Fake):* `{ssn}`
💳 *Card (Fake):* `{cc}`
━━━━━━━━━━━━━━━━━━
⚠️ _For educational purposes only!_
🔰 {hacker_text('voidxdownloder')}
"""
    bot.send_message(chat_id, result, parse_mode="Markdown")

@bot.message_handler(commands=['portscan'])
def portscan_info(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/portscan <host>`", parse_mode="Markdown")
        return
    host = args[1].strip()
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    result = f"📡 *PORT INFO for:* `{host}`\n━━━━━━━━━━━━━━━━━━\n"
    for port, service in common_ports.items():
        result += f"▸ Port `{port}` — {service}\n"
    result += f"\n━━━━━━━━━━━━━━━━━━\n⚠️ _Use responsibly. Unauthorized scanning is illegal._\n🔰 {hacker_text('voidxdownloder')}"
    bot.reply_to(message, result, parse_mode="Markdown")

@bot.message_handler(commands=['phish'])
def send_phish_info(chat_id_or_msg):
    chat_id = chat_id_or_msg if isinstance(chat_id_or_msg, int) else chat_id_or_msg.chat.id
    tips = """
⚡ *PHISHING AWARENESS GUIDE*
━━━━━━━━━━━━━━━━━━
🎣 *What is Phishing?*
Phishing is a cyber attack where hackers trick you into giving your password/data.

🔴 *Red Flags:*
▸ Urgent messages ("Your account will be deleted!")
▸ Suspicious links (check the URL carefully)
▸ Requests for passwords via email/SMS
▸ Offers that seem too good to be true
▸ Fake login pages

🛡️ *How to Stay Safe:*
▸ Always check the URL before clicking
▸ Use 2FA on all accounts
▸ Never share passwords
▸ Use a password manager
▸ Keep software updated
▸ Report suspicious emails

━━━━━━━━━━━━━━━━━━
⚠️ _Educational purposes only!_
🔰 """ + hacker_text('voidxdownloder')
    bot.send_message(chat_id, tips, parse_mode="Markdown")

# ══════════════════════════════════════
# RANDOM TOOLS
# ══════════════════════════════════════

@bot.message_handler(commands=['joke'])
def joke_cmd(message):
    send_joke(message.chat.id)

def send_joke(chat_id):
    jokes = [
        "Why do hackers prefer dark mode? Because light attracts bugs! 🐛",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' 😄",
        "I told my wife she should embrace her mistakes. She gave me a hug. 🤗",
        "Why do programmers prefer iOS development? Because they hate Windows! 🖥️",
        "How many programmers does it take to change a light bulb? None – that's a hardware problem! 💡",
        "Why did the hacker break up with the internet? Too many phishing attempts! 🎣",
        "There are 10 types of people: those who understand binary and those who don't. 0️⃣1️⃣",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings! 😢",
    ]
    bot.send_message(chat_id, f"😂 *Hacker Joke:*\n\n_{random.choice(jokes)}_", parse_mode="Markdown")

@bot.message_handler(commands=['quote'])
def quote_cmd(message):
    send_quote(message.chat.id)

def send_quote(chat_id):
    quotes = [
        "\"The quieter you become, the more you are able to hear.\" - Kali Linux",
        "\"Hackers are breaking the systems for profit. Before, it was about intellectual curiosity.\" - Kevin Mitnick",
        "\"The only secure computer is one that's unplugged.\" - Unknown",
        "\"Hacking is not a crime, it's an art.\" - Anonymous",
        "\"In cyberspace, everyone can hear you scream... and record it.\" - Unknown",
        "\"Knowledge is power. Guard it well.\" - Warhammer 40K",
        "\"The best defense is a good offense.\" - Sun Tzu",
        "\"Privacy is not for the timid.\" - Anonymous",
    ]
    bot.send_message(chat_id, f"💬 *Hacker Quote:*\n\n_{random.choice(quotes)}_", parse_mode="Markdown")

@bot.message_handler(commands=['coin'])
def coin_cmd(message):
    result = random.choice(["Heads 🪙", "Tails 🔄"])
    bot.reply_to(message, f"🪙 *Coin Flip Result:* `{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['dice'])
def dice_cmd(message):
    result = random.randint(1, 6)
    bot.reply_to(message, f"🎲 *Dice Roll:* `{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['uuid'])
def uuid_cmd(message):
    import uuid
    uid = str(uuid.uuid4())
    bot.reply_to(message, f"🆔 *Generated UUID:*\n`{uid}`", parse_mode="Markdown")

@bot.message_handler(commands=['calc'])
def calc_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/calc <expression>`\nExample: `/calc 2+2*10`", parse_mode="Markdown")
        return
    try:
        expr = args[1].strip()
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters")
        result = eval(expr)
        bot.reply_to(message, f"🧮 *Calculator*\n`{expr}` = `{result}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid expression!")

@bot.message_handler(commands=['time'])
def time_cmd(message):
    send_time(message.chat.id)

def send_time(chat_id):
    from datetime import datetime, timezone, timedelta
    zones = {
        "🇺🇸 New York (EST)": -5, "🇬🇧 London (GMT)": 0,
        "🇩🇪 Berlin (CET)": 1, "🇦🇪 Dubai (GST)": 4,
        "🇮🇳 India (IST)": 5.5, "🇨🇳 China (CST)": 8,
        "🇯🇵 Tokyo (JST)": 9, "🇦🇺 Sydney (AEST)": 10,
        "🇵🇰 Pakistan (PKT)": 5,
    }
    now_utc = datetime.now(timezone.utc)
    result = "⏰ *WORLD TIME ZONES*\n━━━━━━━━━━━━━━━━━━\n"
    for zone, offset in zones.items():
        tz = timezone(timedelta(hours=offset))
        local = now_utc.astimezone(tz)
        result += f"{zone}: `{local.strftime('%H:%M:%S')}`\n"
    result += f"━━━━━━━━━━━━━━━━━━\n🔰 {hacker_text('voidxdownloder')}"
    bot.send_message(chat_id, result, parse_mode="Markdown")

@bot.message_handler(commands=['color'])
def color_cmd(message):
    send_color(message.chat.id)

def send_color(chat_id):
    r, g, b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    hex_color = f"#{r:02X}{g:02X}{b:02X}"
    bot.send_message(chat_id, f"🌈 *Random Color*\n\n🎨 *HEX:* `{hex_color}`\n🔴 R: `{r}` | 🟢 G: `{g}` | 🔵 B: `{b}`", parse_mode="Markdown")

@bot.message_handler(commands=['fact'])
def fact_cmd(message):
    send_fact(message.chat.id)

def send_fact(chat_id):
    facts = [
        "The first computer virus was created in 1983 by Fred Cohen! 🦠",
        "The word 'hacker' originally meant someone skilled at programming, not a criminal! 💻",
        "There are over 4.5 billion internet users worldwide! 🌐",
        "Google processes over 8.5 billion searches per day! 🔍",
        "The first email was sent in 1971 by Ray Tomlinson to himself! 📧",
        "Python was named after Monty Python, not the snake! 🐍",
        "The first computer bug was an actual bug (a moth) found in 1947! 🦗",
        "About 90% of the world's currency exists only on computers! 💰",
        "Linux powers 96.3% of the world's top 1 million servers! 🐧",
        "The average person has 100 passwords to remember! 🔑",
    ]
    bot.send_message(chat_id, f"💡 *Tech Fact:*\n\n_{random.choice(facts)}_", parse_mode="Markdown")

@bot.message_handler(commands=['ascii'])
def ascii_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/ascii <text>`", parse_mode="Markdown")
        return
    text = args[1].strip()[:10]
    result = hacker_text(text)
    bot.reply_to(message, f"🔤 *Hacker Font:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['morse'])
def morse_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/morse <text>`", parse_mode="Markdown")
        return
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.'
    }
    text = args[1].upper().strip()
    result = ' '.join(morse_code.get(c, '?') for c in text if c != ' ')
    bot.reply_to(message, f"📡 *Morse Code:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['binary'])
def binary_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/binary <text>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    result = ' '.join(format(ord(c), '08b') for c in text)
    bot.reply_to(message, f"💻 *Binary:*\n`{result[:500]}`", parse_mode="Markdown")

@bot.message_handler(commands=['hex'])
def hex_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/hex <text>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    result = ' '.join(format(ord(c), '02X') for c in text)
    bot.reply_to(message, f"🔢 *Hex:*\n`{result[:500]}`", parse_mode="Markdown")

@bot.message_handler(commands=['reverse'])
def reverse_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/reverse <text>`", parse_mode="Markdown")
        return
    result = args[1].strip()[::-1]
    bot.reply_to(message, f"🔄 *Reversed:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['wiki'])
def wiki_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/wiki <topic>`", parse_mode="Markdown")
        return
    topic = args[1].strip().replace(' ', '_')
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    try:
        r = requests.get(url, timeout=10).json()
        extract = r.get('extract', 'No info found.')[:800]
        page_url = r.get('content_urls', {}).get('desktop', {}).get('page', '')
        bot.reply_to(message, f"📚 *{r.get('title', topic)}*\n\n{extract}\n\n[Read more]({page_url})", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Could not fetch Wikipedia data.")

@bot.message_handler(commands=['crypto'])
def crypto_cmd(message):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,binancecoin,solana&vs_currencies=usd", timeout=10).json()
        result = f"""
💰 *CRYPTO PRICES (USD)*
━━━━━━━━━━━━━━━━━━
₿ Bitcoin: `${r.get('bitcoin',{}).get('usd','N/A'):,}`
⟠ Ethereum: `${r.get('ethereum',{}).get('usd','N/A'):,}`
🐕 Dogecoin: `${r.get('dogecoin',{}).get('usd','N/A')}`
🟡 BNB: `${r.get('binancecoin',{}).get('usd','N/A'):,}`
◎ Solana: `${r.get('solana',{}).get('usd','N/A'):,}`
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
        bot.reply_to(message, result, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Could not fetch crypto prices.")

@bot.message_handler(commands=['ping'])
def ping_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/ping <host>`\nExample: `/ping google.com`", parse_mode="Markdown")
        return
    host = args[1].strip()
    start = time.time()
    try:
        r = requests.get(f"http://{host}", timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)
        bot.reply_to(message, f"📡 *Ping Result*\n🎯 Host: `{host}`\n⏱️ Response: `{elapsed}ms`\n✅ Status: `{r.status_code}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, f"📡 *Ping Result*\n🎯 Host: `{host}`\n❌ Host unreachable or timeout!", parse_mode="Markdown")

@bot.message_handler(commands=['weather'])
def weather_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/weather <city>`\nExample: `/weather London`", parse_mode="Markdown")
        return
    city = args[1].strip()
    try:
        r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10).json()
        current = r['current_condition'][0]
        temp_c = current['temp_C']
        temp_f = current['temp_F']
        feels = current['FeelsLikeC']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        result = f"""
🌤️ *WEATHER: {city.upper()}*
━━━━━━━━━━━━━━━━━━
🌡️ *Temp:* `{temp_c}°C / {temp_f}°F`
🤔 *Feels Like:* `{feels}°C`
☁️ *Condition:* {desc}
💧 *Humidity:* `{humidity}%`
💨 *Wind:* `{wind} km/h`
━━━━━━━━━━━━━━━━━━
🔰 {hacker_text('voidxdownloder')}
"""
        bot.reply_to(message, result, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ City not found or weather service unavailable.")

@bot.message_handler(commands=['short'])
def short_url(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/short <url>`", parse_mode="Markdown")
        return
    url = args[1].strip()
    try:
        r = requests.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=10)
        short = r.text
        bot.reply_to(message, f"🔗 *URL Shortener*\n\n📎 Original: `{url[:50]}...`\n✅ Short: {short}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Could not shorten URL.")

@bot.message_handler(commands=['qr'])
def qr_cmd(message):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/qr <text or url>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={requests.utils.quote(text)}"
    bot.send_photo(message.chat.id, qr_url, caption=f"📱 *QR Code for:*\n`{text}`", parse_mode="Markdown")

# ══════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════

admin_data = {"owner_id": None, "banned_users": [], "user_count": 0, "users": []}

def send_admin_panel(chat_id, user_id):
    if admin_data["owner_id"] and user_id != admin_data["owner_id"]:
        bot.send_message(chat_id, "⛔ *Access Denied!* Admin panel is for owner only.", parse_mode="Markdown")
        return
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban"),
        InlineKeyboardButton("✅ Unban User", callback_data="admin_unban"),
        InlineKeyboardButton("🔄 Restart Bot", callback_data="admin_restart"),
        InlineKeyboardButton("💀 Hacker Mode", callback_data="admin_hacker"),
    )
    bot.send_message(chat_id, f"""
👑 *ADMIN PANEL*
━━━━━━━━━━━━━━━━━━
🔰 *Bot:* {hacker_text('voidxdownloder')}
👤 *Owner:* {hacker_text(OWNER)}
👥 *Users:* {admin_data['user_count']}
🚫 *Banned:* {len(admin_data['banned_users'])}
━━━━━━━━━━━━━━━━━━
""", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['setowner'])
def set_owner(message):
    if admin_data["owner_id"] is None:
        admin_data["owner_id"] = message.from_user.id
        bot.reply_to(message, f"✅ *You are now the owner!*\n👑 Owner ID: `{message.from_user.id}`", parse_mode="Markdown")
    elif message.from_user.id == admin_data["owner_id"]:
        bot.reply_to(message, "👑 You are already the owner!")
    else:
        bot.reply_to(message, "⛔ Owner already set!")

@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only command!")
        return
    result = f"""
📊 *BOT STATISTICS*
━━━━━━━━━━━━━━━━━━
🤖 *Bot:* {hacker_text('voidxdownloder')}
👥 *Total Users:* {admin_data['user_count']}
🚫 *Banned Users:* {len(admin_data['banned_users'])}
👑 *Owner:* {hacker_text(OWNER)}
━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, result, parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only command!")
        return
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/broadcast <message>`", parse_mode="Markdown")
        return
    text = args[1].strip()
    sent = 0
    for uid in admin_data["users"]:
        try:
            bot.send_message(uid, f"📢 *BROADCAST FROM OWNER:*\n\n{text}\n\n— {hacker_text(OWNER)}", parse_mode="Markdown")
            sent += 1
        except:
            pass
    bot.reply_to(message, f"✅ Broadcast sent to {sent} users!")

@bot.message_handler(commands=['ban'])
def ban_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only command!")
        return
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/ban <user_id>`", parse_mode="Markdown")
        return
    try:
        uid = int(args[1].strip())
        if uid not in admin_data["banned_users"]:
            admin_data["banned_users"].append(uid)
            bot.reply_to(message, f"🚫 User `{uid}` has been banned!", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"User `{uid}` is already banned!", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid user ID!")

@bot.message_handler(commands=['unban'])
def unban_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only command!")
        return
    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "Usage: `/unban <user_id>`", parse_mode="Markdown")
        return
    try:
        uid = int(args[1].strip())
        if uid in admin_data["banned_users"]:
            admin_data["banned_users"].remove(uid)
            bot.reply_to(message, f"✅ User `{uid}` has been unbanned!", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"User `{uid}` is not banned!", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid user ID!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callback(call):
    action = call.data.replace("admin_", "")
    if action == "stats":
        bot.answer_callback_query(call.id)
        result = f"📊 Users: {admin_data['user_count']} | Banned: {len(admin_data['banned_users'])}"
        bot.send_message(call.message.chat.id, result)
    elif action == "broadcast":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Use: `/broadcast <message>`", parse_mode="Markdown")
    elif action == "ban":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Use: `/ban <user_id>`", parse_mode="Markdown")
    elif action == "unban":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Use: `/unban <user_id>`", parse_mode="Markdown")
    elif action == "restart":
        bot.answer_callback_query(call.id, "🔄 Restarting...")
        bot.send_message(call.message.chat.id, "🔄 Bot restarting...")
    elif action == "hacker":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"💀 *HACKER MODE ACTIVATED*\n\n{hacker_text('DARK HACKER ZONE')}", parse_mode="Markdown")

# Track all users
@bot.middleware_handler(update_types=['message'])
def track_users(bot_instance, message):
    if message.from_user:
        uid = message.from_user.id
        if uid not in admin_data["users"]:
            admin_data["users"].append(uid)
            admin_data["user_count"] += 1
        if uid in admin_data["banned_users"]:
            return

# Flask keep-alive for Render
app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>🤖 {BOT_NAME} is ONLINE!</h1><p>POWERED BY DARK HACKER ZONE</p>"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def run_bot():
    print(f"🤖 {BOT_NAME} started!")
    print(f"👑 Owner: {OWNER}")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    run_bot()
