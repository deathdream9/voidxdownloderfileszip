import os
import math
import re
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
import uuid as uuid_lib
from datetime import datetime, timezone, timedelta
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

BOT_START_TIME = time.time()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

OWNER = "DEATH DREAM"
BOT_NAME = "voidxdownloder"
CHANNEL_TG = "https://t.me/HACKERQUEEN9"
CHANNEL_TG_ID = "@HACKERQUEEN9"
CHANNEL_WA = "https://whatsapp.com/channel/0029Vb7MViI0VycACP8CUI32"

admin_data = {"owner_id": None, "banned_users": [], "user_count": 0, "users": []}

HACKER_FONT = {
    'A':'𝔸','B':'𝔹','C':'ℂ','D':'𝔻','E':'𝔼','F':'𝔽','G':'𝔾','H':'ℍ','I':'𝕀','J':'𝕁',
    'K':'𝕂','L':'𝕃','M':'𝕄','N':'ℕ','O':'𝕆','P':'ℙ','Q':'ℚ','R':'ℝ','S':'𝕊','T':'𝕋',
    'U':'𝕌','V':'𝕍','W':'𝕎','X':'𝕏','Y':'𝕐','Z':'ℤ',
    'a':'𝕒','b':'𝕓','c':'𝕔','d':'𝕕','e':'𝕖','f':'𝕗','g':'𝕘','h':'𝕙','i':'𝕚','j':'𝕛',
    'k':'𝕜','l':'𝕝','m':'𝕞','n':'𝕟','o':'𝕠','p':'𝕡','q':'𝕢','r':'𝕣','s':'𝕤','t':'𝕥',
    'u':'𝕦','v':'𝕧','w':'𝕨','x':'𝕩','y':'𝕪','z':'𝕫'
}

def hk(text):
    return ''.join(HACKER_FONT.get(c, c) for c in text)

def check_member(user_id):
    try:
        s = bot.get_chat_member(CHANNEL_TG_ID, user_id)
        return s.status in ['member', 'administrator', 'creator']
    except:
        return False

def join_markup():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("📢  Join Telegram Channel", url=CHANNEL_TG))
    m.add(InlineKeyboardButton("💬  Join WhatsApp Channel", url=CHANNEL_WA))
    m.add(InlineKeyboardButton("✅  Done — Verify Me", callback_data="check_join"))
    return m

# ─────────────────────────────────────────────────────────
#  MAIN MENU  (professional card style)
# ─────────────────────────────────────────────────────────
def main_menu_markup():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("▬▬▬  📥 VIDEO DOWNLOADER  ▬▬▬", callback_data="noop"))
    m.add(
        InlineKeyboardButton("🎵 TikTok",       callback_data="menu_tiktok"),
        InlineKeyboardButton("📺 YouTube",      callback_data="menu_youtube"),
    )
    m.add(
        InlineKeyboardButton("📸 Instagram",    callback_data="menu_instagram"),
        InlineKeyboardButton("👤 Facebook",     callback_data="menu_facebook"),
    )
    m.add(
        InlineKeyboardButton("🐦 Twitter/X",    callback_data="menu_twitter"),
        InlineKeyboardButton("🎬 Pinterest",    callback_data="menu_pinterest"),
    )
    m.add(InlineKeyboardButton("▬▬▬  🔧 TOOLS HUB  ▬▬▬", callback_data="noop"))
    m.add(
        InlineKeyboardButton("💀 Hacker Tools",   callback_data="menu_hacker"),
        InlineKeyboardButton("🛠️ Utility Tools",  callback_data="menu_tools"),
    )
    m.add(
        InlineKeyboardButton("🌐 Network Tools",  callback_data="menu_network"),
        InlineKeyboardButton("🔐 Crypto Tools",   callback_data="menu_crypto"),
    )
    m.add(
        InlineKeyboardButton("🔑 Cipher Tools",   callback_data="menu_cipher"),
        InlineKeyboardButton("🧠 Pro Tools",      callback_data="menu_pro"),
    )
    m.add(InlineKeyboardButton("▬▬▬  ⚙️ SYSTEM  ▬▬▬", callback_data="noop"))
    m.add(
        InlineKeyboardButton("ℹ️ Help & Commands", callback_data="menu_help"),
        InlineKeyboardButton("👑 Admin Panel",    callback_data="menu_admin"),
    )
    m.add(
        InlineKeyboardButton("📊 Bot Stats",      callback_data="menu_botstats"),
        InlineKeyboardButton("📢 Our Channel",    url=CHANNEL_TG),
    )
    return m

# ─────────────────────────────────────────────────────────
#  WELCOME  &  /start
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid in admin_data["banned_users"]:
        bot.send_message(message.chat.id, "🚫 You have been banned from using this bot.")
        return
    if not check_member(uid):
        bot.send_message(
            message.chat.id,
            "╔══════════════════════════╗\n"
            "║   ⛔  ACCESS RESTRICTED  ║\n"
            "╚══════════════════════════╝\n\n"
            f"*{hk('voidxdownloder')}* requires you to join\n"
            "our official channels first.\n\n"
            "📢 Join both channels below, then press ✅",
            parse_mode="Markdown",
            reply_markup=join_markup()
        )
        return
    send_welcome(message.chat.id, message.from_user.first_name)

def send_welcome(chat_id, name):
    caption = (
        f"👋 *Welcome, {name}!*\n\n"
        "```\n"
        "╔══════════════════════════════╗\n"
        "║  💀  VOID X DOWNLOADER  💀   ║\n"
        "║  ⚡ DARK HACKER ZONE v3.0 ⚡ ║\n"
        f"║  👑 Owner: DEATH DREAM      ║\n"
        "╚══════════════════════════════╝\n"
        "```\n"
        "📥 *Video Downloader* — TikTok·YT·IG·FB·Twitter\n"
        "💀 *Hacker Tools* — IP·Hash·FakeID·Cipher\n"
        "🛠️ *Utility Tools* — 25+ working tools\n"
        "🌐 *Network Tools* — Ping·DNS·Port info\n"
        "🔐 *Crypto Tools* — Live prices & converter\n"
        "🔑 *Cipher Tools* — ROT13·Caesar·XOR·Vigenere\n"
        "🧠 *Pro Tools* — Strength·Validator·Analyzer\n\n"
        "🔻 *Select a section from the menu below* 🔻"
    )
    banner_path = "assets/banner.png"
    try:
        with open(banner_path, 'rb') as img:
            bot.send_photo(
                chat_id, img,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=main_menu_markup()
            )
    except Exception:
        bot.send_message(chat_id, caption, parse_mode="Markdown", reply_markup=main_menu_markup())

# ─────────────────────────────────────────────────────────
#  JOIN CHECK  CALLBACK
# ─────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def cb_check_join(call):
    if check_member(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified! Welcome aboard!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message.chat.id, call.from_user.first_name)
    else:
        bot.answer_callback_query(call.id, "❌ Not joined yet! Please join both channels.", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "noop")
def cb_noop(call):
    bot.answer_callback_query(call.id)

# ─────────────────────────────────────────────────────────
#  MENU  CALLBACKS
# ─────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data.startswith("menu_"))
def cb_menu(call):
    action = call.data[5:]
    bot.answer_callback_query(call.id)

    if action == "tiktok":
        show_downloader_menu(call.message.chat.id, "TikTok", "🎵", "tiktok")
    elif action == "youtube":
        show_downloader_menu(call.message.chat.id, "YouTube", "📺", "youtube")
    elif action == "instagram":
        show_downloader_menu(call.message.chat.id, "Instagram", "📸", "instagram")
    elif action == "facebook":
        show_downloader_menu(call.message.chat.id, "Facebook", "👤", "facebook")
    elif action == "twitter":
        show_downloader_menu(call.message.chat.id, "Twitter/X", "🐦", "twitter")
    elif action == "pinterest":
        show_downloader_menu(call.message.chat.id, "Pinterest", "🎬", "pinterest")
    elif action == "hacker":
        show_hacker_menu(call.message.chat.id)
    elif action == "tools":
        show_tools_menu(call.message.chat.id)
    elif action == "network":
        show_network_menu(call.message.chat.id)
    elif action == "crypto":
        show_crypto_menu(call.message.chat.id)
    elif action == "help":
        send_help(call.message.chat.id)
    elif action == "admin":
        send_admin_panel(call.message.chat.id, call.from_user.id)
    elif action == "cipher":
        show_cipher_menu(call.message.chat.id)
    elif action == "pro":
        show_pro_menu(call.message.chat.id)
    elif action == "botstats":
        send_bot_stats(call.message.chat.id)
    elif action == "back":
        send_welcome(call.message.chat.id, call.from_user.first_name)

def show_downloader_menu(chat_id, platform, emoji, key):
    m = InlineKeyboardMarkup(row_width=1)
    m.add(InlineKeyboardButton(f"{emoji}  Send me the {platform} link directly!", callback_data=f"dl_info_{key}"))
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        f"╔══════════════════════════╗\n"
        f"║  {emoji}  {platform} Downloader  ║\n"
        f"╚══════════════════════════╝\n\n"
        f"✅ *No watermark*\n"
        f"⚡ *High quality*\n"
        f"🚀 *Fast download*\n\n"
        f"📎 Just paste the *{platform} link* in chat\n"
        f"and I'll download it instantly!\n\n"
        f"Example:\n`https://www.{key}.com/...`",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("dl_info_"))
def cb_dl_info(call):
    key = call.data[8:]
    bot.answer_callback_query(call.id, f"Send me the {key} link in chat!")

# ─────────────────────────────────────────────────────────
#  HACKER TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_hacker_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🌐  IP Tracker",      callback_data="hk_ip"),
        InlineKeyboardButton("🔐  Hash Generator",  callback_data="hk_hash"),
    )
    m.add(
        InlineKeyboardButton("🔑  Base64 Encode",   callback_data="hk_enc"),
        InlineKeyboardButton("🔓  Base64 Decode",   callback_data="hk_dec"),
    )
    m.add(
        InlineKeyboardButton("🛡️  PassGen",         callback_data="hk_pass"),
        InlineKeyboardButton("🕵️  Username Hunt",   callback_data="hk_user"),
    )
    m.add(
        InlineKeyboardButton("💀  Fake Identity",   callback_data="hk_fakeid"),
        InlineKeyboardButton("⚡  Phish Guide",     callback_data="hk_phish"),
    )
    m.add(
        InlineKeyboardButton("🪪  WhoAmI",          callback_data="hk_whoami"),
        InlineKeyboardButton("📡  Port Info",       callback_data="hk_port"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║  💀  HACKER TOOLS PANEL  ║\n"
        "║  DARK HACKER ZONE v2.0   ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "⚠️ *For educational purposes only*\n\n"
        "Select a tool to begin:",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("hk_"))
def cb_hacker(call):
    bot.answer_callback_query(call.id)
    a = call.data[3:]
    cid = call.message.chat.id
    uid = call.from_user.id
    if a == "ip":
        bot.send_message(cid, "🌐 *IP Tracker*\n\nUsage: `/ip <ip_address>`\nExample: `/ip 8.8.8.8`\n\nAlso works for domain names!", parse_mode="Markdown")
    elif a == "hash":
        bot.send_message(cid, "🔐 *Hash Generator*\n\nUsage: `/hash <text>`\nGenerates: MD5, SHA1, SHA256, SHA512", parse_mode="Markdown")
    elif a == "enc":
        bot.send_message(cid, "🔑 *Base64 Encode*\n\nUsage: `/encode <text>`", parse_mode="Markdown")
    elif a == "dec":
        bot.send_message(cid, "🔓 *Base64 Decode*\n\nUsage: `/decode <base64_text>`", parse_mode="Markdown")
    elif a == "pass":
        bot.send_message(cid, "🛡️ *Password Generator*\n\nUsage: `/passgen <length>`\nExample: `/passgen 20`\nMax length: 64", parse_mode="Markdown")
    elif a == "user":
        bot.send_message(cid, "🕵️ *Username Hunt*\n\nUsage: `/username <name>`\nChecks 10+ platforms!", parse_mode="Markdown")
    elif a == "fakeid":
        generate_fake_id(cid)
    elif a == "phish":
        send_phish_info(cid)
    elif a == "whoami":
        whoami_action(cid, call.from_user)
    elif a == "port":
        bot.send_message(cid, "📡 *Port Scanner Info*\n\nUsage: `/portscan <host>`\nExample: `/portscan google.com`", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  CIPHER TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_cipher_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🔁  ROT13",         callback_data="ci_rot13"),
        InlineKeyboardButton("🏛️  Caesar",         callback_data="ci_caesar"),
    )
    m.add(
        InlineKeyboardButton("⚡  XOR Cipher",    callback_data="ci_xor"),
        InlineKeyboardButton("🌿  Vigenere",       callback_data="ci_vigenere"),
    )
    m.add(
        InlineKeyboardButton("🔤  Atbash",         callback_data="ci_atbash"),
        InlineKeyboardButton("💠  Base32",         callback_data="ci_base32"),
    )
    m.add(
        InlineKeyboardButton("🔢  Hex Encode",     callback_data="ci_hexenc"),
        InlineKeyboardButton("📦  URL Encode",     callback_data="ci_urlenc"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║  🔑  CIPHER TOOLS v2.0  ║\n"
        "║  DARK HACKER ZONE        ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "🔐 *Encrypt & Decode anything!*\n\n"
        "▸ ROT13 · Caesar · XOR\n"
        "▸ Vigenere · Atbash · Base32\n"
        "▸ Hex & URL encoding\n\n"
        "Or use commands directly:\n"
        "`/rot13` `/caesar` `/atbash` `/vigenere`",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("ci_"))
def cb_cipher(call):
    bot.answer_callback_query(call.id)
    a = call.data[3:]
    cid = call.message.chat.id
    if a == "rot13":
        bot.send_message(cid, "🔁 *ROT13 Cipher*\n\nUsage: `/rot13 <text>`\nExample: `/rot13 hello world`\n\n_ROT13 shifts each letter by 13 positions._", parse_mode="Markdown")
    elif a == "caesar":
        bot.send_message(cid, "🏛️ *Caesar Cipher*\n\nUsage: `/caesar <shift> <text>`\nExample: `/caesar 3 hello`\n\n_Shifts each letter by the given number._", parse_mode="Markdown")
    elif a == "xor":
        bot.send_message(cid, "⚡ *XOR Cipher*\n\nUsage: `/xor <key> <text>`\nExample: `/xor 42 hello`\n\n_XOR each character with a numeric key._", parse_mode="Markdown")
    elif a == "vigenere":
        bot.send_message(cid, "🌿 *Vigenere Cipher*\n\nUsage: `/vigenere <key> <text>`\nExample: `/vigenere secret hello`\n\n_Polyalphabetic substitution cipher._", parse_mode="Markdown")
    elif a == "atbash":
        bot.send_message(cid, "🔤 *Atbash Cipher*\n\nUsage: `/atbash <text>`\nExample: `/atbash hello`\n\n_Reverses the alphabet (A↔Z, B↔Y...)_", parse_mode="Markdown")
    elif a == "base32":
        bot.send_message(cid, "💠 *Base32 Encode*\n\nUsage: `/base32 <text>`\nExample: `/base32 hello world`", parse_mode="Markdown")
    elif a == "hexenc":
        bot.send_message(cid, "🔢 *Hex Encode*\n\nUsage: `/hex <text>`\nExample: `/hex hello`", parse_mode="Markdown")
    elif a == "urlenc":
        bot.send_message(cid, "📦 *URL Encode*\n\nUsage: `/urlencode <text>`\nExample: `/urlencode hello world&more`", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  PRO TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_pro_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("💪  Pass Strength",   callback_data="pr_strength"),
        InlineKeyboardButton("📧  Email Validator",  callback_data="pr_email"),
    )
    m.add(
        InlineKeyboardButton("📝  Text Analyzer",   callback_data="pr_textana"),
        InlineKeyboardButton("🔢  Prime Check",     callback_data="pr_prime"),
    )
    m.add(
        InlineKeyboardButton("🧮  Factorial",       callback_data="pr_factorial"),
        InlineKeyboardButton("🎲  Random Number",   callback_data="pr_randnum"),
    )
    m.add(
        InlineKeyboardButton("🌍  Country Info",    callback_data="pr_country"),
        InlineKeyboardButton("☀️  Horoscope",       callback_data="pr_horo"),
    )
    m.add(
        InlineKeyboardButton("⏱️  Bot Uptime",      callback_data="pr_uptime"),
        InlineKeyboardButton("🖥️  System Info",     callback_data="pr_sysinfo"),
    )
    m.add(
        InlineKeyboardButton("🔗  Link Checker",    callback_data="pr_linkcheck"),
        InlineKeyboardButton("📊  Text Stats",      callback_data="pr_textstats"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║  🧠  PRO TOOLS PANEL     ║\n"
        "║  Advanced Features v3.0  ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "⚡ *Professional grade tools:*\n\n"
        "▸ Password strength analyzer\n"
        "▸ Email & URL validator\n"
        "▸ Text statistics & analysis\n"
        "▸ Math tools (prime, factorial)\n"
        "▸ Country info, Horoscope\n"
        "▸ System & uptime info",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("pr_"))
def cb_pro(call):
    bot.answer_callback_query(call.id)
    a = call.data[3:]
    cid = call.message.chat.id
    if a == "strength":
        bot.send_message(cid, "💪 *Password Strength Checker*\n\nUsage: `/strength <password>`\nExample: `/strength MyP@ss123!`", parse_mode="Markdown")
    elif a == "email":
        bot.send_message(cid, "📧 *Email Validator*\n\nUsage: `/email <email>`\nExample: `/email test@gmail.com`", parse_mode="Markdown")
    elif a == "textana":
        bot.send_message(cid, "📝 *Text Analyzer*\n\nUsage: `/analyze <text>`\nShows: words, chars, sentences, reading time!", parse_mode="Markdown")
    elif a == "prime":
        bot.send_message(cid, "🔢 *Prime Number Checker*\n\nUsage: `/prime <number>`\nExample: `/prime 97`", parse_mode="Markdown")
    elif a == "factorial":
        bot.send_message(cid, "🧮 *Factorial Calculator*\n\nUsage: `/factorial <number>`\nExample: `/factorial 10`", parse_mode="Markdown")
    elif a == "randnum":
        rn = random.randint(1, 1000000)
        bot.send_message(cid, f"🎲 *Random Number (1–1,000,000):*\n\n`{rn:,}`", parse_mode="Markdown")
    elif a == "country":
        bot.send_message(cid, "🌍 *Country Info*\n\nUsage: `/country <name>`\nExample: `/country Pakistan`", parse_mode="Markdown")
    elif a == "horo":
        show_horoscope_menu(cid)
    elif a == "uptime":
        send_uptime(cid)
    elif a == "sysinfo":
        send_sysinfo(cid)
    elif a == "linkcheck":
        bot.send_message(cid, "🔗 *Link Checker*\n\nUsage: `/check <url>`\nExample: `/check https://google.com`\n\nChecks if URL is alive & safe!", parse_mode="Markdown")
    elif a == "textstats":
        bot.send_message(cid, "📊 *Text Stats*\n\nUsage: `/analyze <text>`\nExample: `/analyze Hello world this is a test`", parse_mode="Markdown")

def show_horoscope_menu(chat_id):
    signs = ["♈ Aries","♉ Taurus","♊ Gemini","♋ Cancer","♌ Leo","♍ Virgo",
             "♎ Libra","♏ Scorpio","♐ Sagittarius","♑ Capricorn","♒ Aquarius","♓ Pisces"]
    m = InlineKeyboardMarkup(row_width=3)
    for s in signs:
        m.add(InlineKeyboardButton(s, callback_data=f"horo_{s.split()[1]}"))
    m.add(InlineKeyboardButton("🏠  Back", callback_data="menu_back"))
    bot.send_message(chat_id, "☀️ *Choose your zodiac sign:*", parse_mode="Markdown", reply_markup=m)

@bot.callback_query_handler(func=lambda c: c.data.startswith("horo_"))
def cb_horoscope(call):
    sign = call.data[5:]
    bot.answer_callback_query(call.id)
    fortunes = [
        "🌟 Great energy surrounds you today. Take bold action!",
        "🔮 A mysterious opportunity will present itself soon.",
        "⚡ Your hacker instincts are sharp — trust them.",
        "💀 The digital world bows to your skills today.",
        "🌙 Patience is your superpower. The code will compile.",
        "🎯 Focus on one goal and you'll achieve the impossible.",
        "🛡️ Your defenses are strong. Nothing can breach you.",
        "💡 A brilliant idea will strike you like a zero-day exploit.",
        "🚀 Level up today — new skills await you.",
        "🌐 The network is in your favor. Connect and conquer.",
    ]
    moods = ["Focused 🎯", "Energized ⚡", "Mysterious 🔮", "Powerful 💀", "Creative 💡"]
    lucky = [f"0x{random.randint(0,255):02X}", str(random.randint(1,99)), random.choice(["7","13","42","1337","404"])]
    msg = (
        f"☀️ *{sign} Horoscope*\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🔮 *Today's Message:*\n_{random.choice(fortunes)}_\n\n"
        f"😊 *Mood:* {random.choice(moods)}\n"
        f"🍀 *Lucky Number:* `{random.choice(lucky)}`\n"
        f"🎨 *Lucky Color:* `#{random.randint(0,0xFFFFFF):06X}`\n"
        f"⚡ *Power Level:* `{'█' * random.randint(5,10)}` {random.randint(70,100)}%\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔰 {hk('voidxdownloder')}"
    )
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

def send_uptime(chat_id):
    elapsed = int(time.time() - BOT_START_TIME)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  ⏱️  BOT UPTIME STATUS   ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🤖 Bot: *{hk('voidxdownloder')}*\n"
        f"⏱️ Uptime: `{h}h {m}m {s}s`\n"
        f"🟢 Status: `Online & Running`\n"
        f"👥 Total Users: `{admin_data['user_count']}`\n"
        f"🚫 Banned Users: `{len(admin_data['banned_users'])}`\n"
        f"🕐 Started: `{datetime.utcfromtimestamp(BOT_START_TIME).strftime('%Y-%m-%d %H:%M UTC')}`"
    )
    bot.send_message(chat_id, msg, parse_mode="Markdown")

def send_sysinfo(chat_id):
    try:
        import platform
        msg = (
            "```\n╔══════════════════════════╗\n"
            "║  🖥️  SYSTEM INFORMATION  ║\n"
            "╚══════════════════════════╝\n```\n"
            f"🖥️ OS: `{platform.system()} {platform.release()}`\n"
            f"🐍 Python: `{platform.python_version()}`\n"
            f"💻 Machine: `{platform.machine()}`\n"
            f"🌐 Node: `{platform.node()[:20]}`\n"
            f"⚙️ Processor: `{platform.processor()[:30] or 'Unknown'}`\n"
            f"🕐 UTC Time: `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: `{e}`", parse_mode="Markdown")

def send_bot_stats(chat_id):
    elapsed = int(time.time() - BOT_START_TIME)
    h, rem = divmod(elapsed, 3600)
    m_t, s = divmod(rem, 60)
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  📊  BOT STATISTICS      ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🤖 *{hk('voidxdownloder')}*\n"
        f"👑 Owner: *{hk(OWNER)}*\n\n"
        f"👥 Total Users: `{admin_data['user_count']}`\n"
        f"🚫 Banned: `{len(admin_data['banned_users'])}`\n"
        f"⏱️ Uptime: `{h}h {m_t}m {s}s`\n"
        f"🟢 Status: `Online`\n"
        f"⚡ Version: `v3.0 DARK HACKER`\n"
        f"📡 Tools: `25+`\n"
        f"📥 Platforms: `6`\n\n"
        f"📢 Channel: @HACKERQUEEN9\n"
        f"⚡ POWERED BY DARK HACKER ZONE"
    )
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=m)

# ─────────────────────────────────────────────────────────
#  UTILITY TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_tools_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🎲  Dice Roll",    callback_data="ut_dice"),
        InlineKeyboardButton("🪙  Coin Flip",    callback_data="ut_coin"),
    )
    m.add(
        InlineKeyboardButton("😂  Hacker Joke",  callback_data="ut_joke"),
        InlineKeyboardButton("💬  Hacker Quote", callback_data="ut_quote"),
    )
    m.add(
        InlineKeyboardButton("🌈  Random Color", callback_data="ut_color"),
        InlineKeyboardButton("💡  Tech Fact",    callback_data="ut_fact"),
    )
    m.add(
        InlineKeyboardButton("🆔  UUID Gen",     callback_data="ut_uuid"),
        InlineKeyboardButton("⏰  World Time",   callback_data="ut_time"),
    )
    m.add(
        InlineKeyboardButton("📱  QR Code",      callback_data="ut_qr"),
        InlineKeyboardButton("🔗  URL Short",    callback_data="ut_short"),
    )
    m.add(
        InlineKeyboardButton("🔢  Binary",       callback_data="ut_binary"),
        InlineKeyboardButton("🔠  Morse Code",   callback_data="ut_morse"),
    )
    m.add(
        InlineKeyboardButton("🔤  Hex Convert",  callback_data="ut_hex"),
        InlineKeyboardButton("🔄  Reverse Text", callback_data="ut_reverse"),
    )
    m.add(
        InlineKeyboardButton("🧮  Calculator",   callback_data="ut_calc"),
        InlineKeyboardButton("📚  Wikipedia",    callback_data="ut_wiki"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║   🛠️  UTILITY TOOLS KIT  ║\n"
        "║  20+ Working Tools Here  ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "Select any tool below:",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("ut_"))
def cb_utility(call):
    bot.answer_callback_query(call.id)
    a = call.data[3:]
    cid = call.message.chat.id
    if a == "dice":
        r = random.randint(1, 6)
        faces = ["", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
        bot.send_message(cid, f"🎲 *Dice Rolled!*\n\nResult: {faces[r]} (`{r}`)", parse_mode="Markdown")
    elif a == "coin":
        r = random.choice(["🪙 Heads", "🔄 Tails"])
        bot.send_message(cid, f"🪙 *Coin Flipped!*\n\nResult: *{r}*", parse_mode="Markdown")
    elif a == "joke":
        send_joke(cid)
    elif a == "quote":
        send_quote(cid)
    elif a == "color":
        send_color(cid)
    elif a == "fact":
        send_fact(cid)
    elif a == "uuid":
        uid = str(uuid_lib.uuid4())
        bot.send_message(cid, f"🆔 *Random UUID Generated:*\n\n`{uid}`\n\n_Click to copy!_", parse_mode="Markdown")
    elif a == "time":
        send_time(cid)
    elif a == "qr":
        bot.send_message(cid, "📱 *QR Code Generator*\n\nUsage: `/qr <text or url>`\nExample: `/qr https://t.me/HACKERQUEEN9`", parse_mode="Markdown")
    elif a == "short":
        bot.send_message(cid, "🔗 *URL Shortener*\n\nUsage: `/short <url>`\nExample: `/short https://example.com`", parse_mode="Markdown")
    elif a == "binary":
        bot.send_message(cid, "🔢 *Text → Binary*\n\nUsage: `/binary <text>`\nExample: `/binary hello`", parse_mode="Markdown")
    elif a == "morse":
        bot.send_message(cid, "🔠 *Text → Morse Code*\n\nUsage: `/morse <text>`\nExample: `/morse SOS`", parse_mode="Markdown")
    elif a == "hex":
        bot.send_message(cid, "🔤 *Text → Hex*\n\nUsage: `/hex <text>`\nExample: `/hex hello`", parse_mode="Markdown")
    elif a == "reverse":
        bot.send_message(cid, "🔄 *Reverse Text*\n\nUsage: `/reverse <text>`\nExample: `/reverse hello world`", parse_mode="Markdown")
    elif a == "calc":
        bot.send_message(cid, "🧮 *Calculator*\n\nUsage: `/calc <expression>`\nExample: `/calc 25*4+10/2`", parse_mode="Markdown")
    elif a == "wiki":
        bot.send_message(cid, "📚 *Wikipedia Search*\n\nUsage: `/wiki <topic>`\nExample: `/wiki Python programming`", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  NETWORK TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_network_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📡  Ping Host",    callback_data="nt_ping"),
        InlineKeyboardButton("🌐  IP Lookup",    callback_data="nt_ip"),
    )
    m.add(
        InlineKeyboardButton("🔍  DNS Lookup",   callback_data="nt_dns"),
        InlineKeyboardButton("📊  Port Info",    callback_data="nt_port"),
    )
    m.add(
        InlineKeyboardButton("🕵️  My IP",        callback_data="nt_myip"),
        InlineKeyboardButton("🌍  GeoIP Map",    callback_data="nt_geo"),
    )
    m.add(
        InlineKeyboardButton("⚡  Speed Test",   callback_data="nt_speed"),
        InlineKeyboardButton("🛡️  VPN Check",    callback_data="nt_vpn"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║  🌐  NETWORK TOOLS PANEL ║\n"
        "║  Professional Suite v2.0 ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "🔧 All network utilities in one place:\n\n"
        "Use commands: `/ping` `/ip` `/dns` `/portscan`",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("nt_"))
def cb_network(call):
    bot.answer_callback_query(call.id)
    a = call.data[3:]
    cid = call.message.chat.id
    if a == "ping":
        bot.send_message(cid, "📡 *Ping Tool*\n\nUsage: `/ping <host>`\nExample: `/ping google.com`", parse_mode="Markdown")
    elif a == "ip":
        bot.send_message(cid, "🌐 *IP Tracker*\n\nUsage: `/ip <ip or domain>`\nExample: `/ip 8.8.8.8`", parse_mode="Markdown")
    elif a == "dns":
        bot.send_message(cid, "🔍 *DNS Lookup*\n\nUsage: `/dns <domain>`\nExample: `/dns google.com`", parse_mode="Markdown")
    elif a == "port":
        bot.send_message(cid, "📊 *Port Info*\n\nUsage: `/portscan <host>`\nExample: `/portscan google.com`", parse_mode="Markdown")
    elif a == "myip":
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=8).json()
            bot.send_message(cid, f"🕵️ *Bot Server IP:*\n`{r.get('ip','N/A')}`", parse_mode="Markdown")
        except:
            bot.send_message(cid, "❌ Could not fetch IP.")
    elif a == "geo":
        bot.send_message(cid, "🌍 *GeoIP Map*\n\nUsage: `/ip <ip>`\nShows location on map link.", parse_mode="Markdown")
    elif a == "speed":
        bot.send_message(cid, "⚡ *Server Response Test*\n\nUsage: `/ping <host>`\nMeasures response time in ms.", parse_mode="Markdown")
    elif a == "vpn":
        bot.send_message(cid, "🛡️ *VPN/Proxy Checker*\n\nUsage: `/ip <ip>`\nShows ISP and proxy info.", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  CRYPTO TOOLS  MENU
# ─────────────────────────────────────────────────────────
def show_crypto_menu(chat_id):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("₿  Bitcoin",      callback_data="cr_btc"),
        InlineKeyboardButton("⟠  Ethereum",     callback_data="cr_eth"),
    )
    m.add(
        InlineKeyboardButton("🐕  Dogecoin",    callback_data="cr_doge"),
        InlineKeyboardButton("◎  Solana",       callback_data="cr_sol"),
    )
    m.add(
        InlineKeyboardButton("📊  All Prices",  callback_data="cr_all"),
        InlineKeyboardButton("🔄  Converter",   callback_data="cr_conv"),
    )
    m.add(
        InlineKeyboardButton("📈  Market Cap",  callback_data="cr_cap"),
        InlineKeyboardButton("🌡️  Fear Index",  callback_data="cr_fear"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n"
        "╔══════════════════════════╗\n"
        "║  🔐  CRYPTO TOOLS PANEL  ║\n"
        "║  Live Prices & Analytics ║\n"
        "╚══════════════════════════╝\n"
        "```\n"
        "💰 Real-time crypto data!\n\nUse: `/crypto` for all prices",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("cr_"))
def cb_crypto(call):
    bot.answer_callback_query(call.id, "⏳ Fetching live data...")
    a = call.data[3:]
    cid = call.message.chat.id
    coin_map = {"btc": "bitcoin", "eth": "ethereum", "doge": "dogecoin", "sol": "solana"}
    if a in coin_map:
        fetch_single_crypto(cid, coin_map[a])
    elif a == "all":
        fetch_all_crypto(cid)
    elif a == "cap":
        fetch_market_cap(cid)
    elif a == "fear":
        fetch_fear_index(cid)
    elif a == "conv":
        bot.send_message(cid, "🔄 *Crypto Converter*\n\nUsage: `/convert <amount> <from> <to>`\nExample: `/convert 1 btc usd`", parse_mode="Markdown")

def fetch_single_crypto(chat_id, coin):
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd,eur,gbp&include_24hr_change=true&include_market_cap=true",
            timeout=10
        ).json()
        d = r.get(coin, {})
        change = d.get('usd_24h_change', 0)
        trend = "📈" if change > 0 else "📉"
        names = {"bitcoin": "₿ Bitcoin", "ethereum": "⟠ Ethereum", "dogecoin": "🐕 Dogecoin", "solana": "◎ Solana"}
        msg = (
            f"```\n"
            f"╔════════════════════════╗\n"
            f"║  {names.get(coin, coin):^22}  ║\n"
            f"╚════════════════════════╝\n"
            f"```\n"
            f"💵 USD:  `${d.get('usd',0):,.4f}`\n"
            f"💶 EUR:  `€{d.get('eur',0):,.4f}`\n"
            f"💷 GBP:  `£{d.get('gbp',0):,.4f}`\n"
            f"{trend} 24h Change: `{change:.2f}%`\n"
            f"📊 Market Cap: `${d.get('usd_market_cap',0):,.0f}`"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "❌ Could not fetch crypto data. Try again.")

def fetch_all_crypto(chat_id):
    try:
        ids = "bitcoin,ethereum,dogecoin,binancecoin,solana,ripple,cardano,polkadot"
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true",
            timeout=10
        ).json()
        lines = [
            "```\n╔══════════════════════════╗",
            "║   💰  LIVE CRYPTO PRICES  ║",
            "╚══════════════════════════╝\n```",
        ]
        symbols = [
            ("bitcoin","₿ BTC"), ("ethereum","⟠ ETH"), ("binancecoin","🟡 BNB"),
            ("solana","◎ SOL"), ("ripple","💧 XRP"), ("cardano","🔵 ADA"),
            ("polkadot","⚫ DOT"), ("dogecoin","🐕 DOGE"),
        ]
        for cid_key, sym in symbols:
            d = r.get(cid_key, {})
            p = d.get('usd', 0)
            ch = d.get('usd_24h_change', 0)
            arrow = "▲" if ch > 0 else "▼"
            lines.append(f"{sym}: `${p:,.4f}` {arrow}`{ch:.1f}%`")
        lines.append(f"\n🕐 Updated: `{datetime.utcnow().strftime('%H:%M UTC')}`")
        bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "❌ Could not fetch crypto data.")

def fetch_market_cap(chat_id):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=10).json()
        d = r.get("data", {})
        total = d.get("total_market_cap", {}).get("usd", 0)
        vol = d.get("total_volume", {}).get("usd", 0)
        btc_dom = d.get("market_cap_percentage", {}).get("btc", 0)
        msg = (
            "```\n╔══════════════════════════╗\n"
            "║  📈  CRYPTO MARKET CAP   ║\n"
            "╚══════════════════════════╝\n```\n"
            f"💰 Total Market Cap: `${total:,.0f}`\n"
            f"📊 24h Volume: `${vol:,.0f}`\n"
            f"₿ BTC Dominance: `{btc_dom:.1f}%`"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "❌ Could not fetch market data.")

def fetch_fear_index(chat_id):
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10).json()
        d = r.get("data", [{}])[0]
        val = d.get("value", "N/A")
        label = d.get("value_classification", "N/A")
        emoji_map = {"Extreme Fear":"😱","Fear":"😨","Neutral":"😐","Greed":"😄","Extreme Greed":"🤑"}
        e = emoji_map.get(label, "📊")
        msg = (
            "```\n╔══════════════════════════╗\n"
            "║  🌡️  FEAR & GREED INDEX  ║\n"
            "╚══════════════════════════╝\n```\n"
            f"{e} *{label}*\n\n"
            f"Index Value: `{val}/100`\n\n"
            f"_0 = Extreme Fear | 100 = Extreme Greed_"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "❌ Could not fetch fear index.")

# ─────────────────────────────────────────────────────────
#  BACK TO MAIN (from sub-menus)
# ─────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data == "menu_back")
def cb_back(call):
    bot.answer_callback_query(call.id)
    send_welcome(call.message.chat.id, call.from_user.first_name)

# ─────────────────────────────────────────────────────────
#  VIDEO  DOWNLOADERS
# ─────────────────────────────────────────────────────────
def download_video(url, chat_id, platform):
    msg = bot.send_message(
        chat_id,
        f"```\n⏳ Downloading from {platform}...\n"
        f"Please wait — this may take a moment.\n```",
        parse_mode="Markdown"
    )
    try:
        ydl_opts = {
            'format': 'best[ext=mp4][filesize<50M]/best[filesize<50M]/best',
            'outtmpl': '/tmp/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            title = info.get('title', 'Video')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')

        bot.edit_message_text("✅ Download complete! Uploading now...", chat_id, msg.message_id)

        caption = (
            f"🎬 *{title[:80]}*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📺 Platform: *{platform}*\n"
            f"👤 By: {uploader}\n"
            f"⏱️ Duration: {duration}s\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📥 {hk('voidxdownloder')}\n"
            f"👑 Owner: {hk(OWNER)}\n"
            f"📢 {CHANNEL_TG}"
        )
        with open(file_path, 'rb') as video:
            bot.send_video(chat_id, video, caption=caption, parse_mode="Markdown", supports_streaming=True)
        os.remove(file_path)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        err = str(e)[:200]
        bot.edit_message_text(
            f"❌ *Download Failed*\n\n`{err}`\n\n"
            "_Make sure the link is valid and publicly accessible._",
            chat_id, msg.message_id, parse_mode="Markdown"
        )

@bot.message_handler(commands=['tiktok'])
def tiktok_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "🎵 Send: `/tiktok <link>`", parse_mode="Markdown"); return
    threading.Thread(target=download_video, args=(parts[1].strip(), message.chat.id, "TikTok")).start()

@bot.message_handler(commands=['youtube'])
def youtube_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "📺 Send: `/youtube <link>`", parse_mode="Markdown"); return
    threading.Thread(target=download_video, args=(parts[1].strip(), message.chat.id, "YouTube")).start()

@bot.message_handler(commands=['instagram'])
def instagram_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "📸 Send: `/instagram <link>`", parse_mode="Markdown"); return
    threading.Thread(target=download_video, args=(parts[1].strip(), message.chat.id, "Instagram")).start()

@bot.message_handler(commands=['facebook'])
def facebook_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "👤 Send: `/facebook <link>`", parse_mode="Markdown"); return
    threading.Thread(target=download_video, args=(parts[1].strip(), message.chat.id, "Facebook")).start()

@bot.message_handler(commands=['twitter'])
def twitter_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "🐦 Send: `/twitter <link>`", parse_mode="Markdown"); return
    threading.Thread(target=download_video, args=(parts[1].strip(), message.chat.id, "Twitter/X")).start()

@bot.message_handler(func=lambda m: m.text and any(x in m.text for x in [
    'tiktok.com','youtu','instagram.com','facebook.com','fb.watch','twitter.com','x.com','t.co','pin.it','pinterest.com'
]))
def auto_download(message):
    if message.from_user.id in admin_data["banned_users"]: return
    if not check_member(message.from_user.id):
        bot.reply_to(message, "⛔ Join our channel first!", reply_markup=join_markup()); return
    url = message.text.strip()
    platform = "Video"
    if 'tiktok' in url: platform = "TikTok"
    elif 'youtu' in url: platform = "YouTube"
    elif 'instagram' in url: platform = "Instagram"
    elif 'facebook' in url or 'fb.watch' in url: platform = "Facebook"
    elif 'twitter' in url or 'x.com' in url or 't.co' in url: platform = "Twitter/X"
    elif 'pinterest' in url or 'pin.it' in url: platform = "Pinterest"
    threading.Thread(target=download_video, args=(url, message.chat.id, platform)).start()

# ─────────────────────────────────────────────────────────
#  HACKER  TOOL  COMMANDS
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['ip'])
def ip_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/ip <ip or domain>`", parse_mode="Markdown"); return
    target = parts[1].strip()
    try:
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=10).json()
        if r['status'] == 'success':
            lat, lon = r.get('lat',''), r.get('lon','')
            map_link = f"https://www.google.com/maps?q={lat},{lon}"
            msg = (
                "```\n╔══════════════════════════╗\n"
                "║  🌐  IP TRACKER RESULT   ║\n"
                "╚══════════════════════════╝\n```\n"
                f"🎯 IP: `{r.get('query','N/A')}`\n"
                f"🌍 Country: `{r.get('country','N/A')}` {r.get('countryCode','')}\n"
                f"🏙️ City: `{r.get('city','N/A')}`\n"
                f"📍 Region: `{r.get('regionName','N/A')}`\n"
                f"📮 ZIP: `{r.get('zip','N/A')}`\n"
                f"📡 ISP: `{r.get('isp','N/A')}`\n"
                f"🏢 Org: `{r.get('org','N/A')}`\n"
                f"🗺️ Lat/Lon: `{lat}, {lon}`\n"
                f"⏰ Timezone: `{r.get('timezone','N/A')}`\n"
                f"🗾 [View on Map]({map_link})"
            )
            bot.reply_to(message, msg, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Invalid IP or private address.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: `{e}`", parse_mode="Markdown")

@bot.message_handler(commands=['dns'])
def dns_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/dns <domain>`", parse_mode="Markdown"); return
    domain = parts[1].strip()
    try:
        r = requests.get(f"https://dns.google/resolve?name={domain}&type=A", timeout=10).json()
        answers = r.get('Answer', [])
        if answers:
            ips = "\n".join(f"▸ `{a.get('data','')}`" for a in answers[:5])
            bot.reply_to(message, f"🔍 *DNS Lookup: `{domain}`*\n\n{ips}", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ No DNS records found for `{domain}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ DNS lookup failed.")

@bot.message_handler(commands=['whoami'])
def whoami_cmd(message):
    whoami_action(message.chat.id, message.from_user)

def whoami_action(chat_id, user):
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  🕵️  YOUR INFO LOOKUP    ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🆔 User ID: `{user.id}`\n"
        f"👤 Name: `{user.first_name} {user.last_name or ''}`\n"
        f"📛 Username: `@{user.username or 'None'}`\n"
        f"🌐 Language: `{user.language_code or 'Unknown'}`\n"
        f"🤖 Is Bot: `{user.is_bot}`"
    )
    bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['hash'])
def hash_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/hash <text>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  🔐  HASH GENERATOR      ║\n"
        "╚══════════════════════════╝\n```\n"
        f"📝 Input: `{text}`\n\n"
        f"🔑 MD5:\n`{hashlib.md5(text.encode()).hexdigest()}`\n\n"
        f"🔒 SHA1:\n`{hashlib.sha1(text.encode()).hexdigest()}`\n\n"
        f"🛡️ SHA256:\n`{hashlib.sha256(text.encode()).hexdigest()}`\n\n"
        f"💀 SHA512:\n`{hashlib.sha512(text.encode()).hexdigest()[:64]}...`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(commands=['encode'])
def encode_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/encode <text>`", parse_mode="Markdown"); return
    bot.reply_to(message, f"🔑 *Base64 Encoded:*\n\n`{base64.b64encode(parts[1].strip().encode()).decode()}`", parse_mode="Markdown")

@bot.message_handler(commands=['decode'])
def decode_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/decode <base64>`", parse_mode="Markdown"); return
    try:
        bot.reply_to(message, f"🔓 *Base64 Decoded:*\n\n`{base64.b64decode(parts[1].strip()).decode()}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid Base64 string!")

@bot.message_handler(commands=['passgen'])
def passgen_cmd(message):
    parts = message.text.split(' ', 1)
    length = 16
    if len(parts) > 1:
        try: length = min(64, max(4, int(parts[1].strip())))
        except: pass
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    pwd = ''.join(random.choice(chars) for _ in range(length))
    strength = "🟢 Strong" if length >= 12 else "🟡 Medium" if length >= 8 else "🔴 Weak"
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  🛡️  PASSWORD GENERATOR  ║\n"
        "╚══════════════════════════╝\n```\n"
        f"📏 Length: `{length}`\n"
        f"💪 Strength: {strength}\n\n"
        f"🔑 Password:\n`{pwd}`\n\n"
        "_Tap to copy!_"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(commands=['username'])
def username_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/username <name>`", parse_mode="Markdown"); return
    name = parts[1].strip()
    platforms = {
        "GitHub": f"https://github.com/{name}",
        "Twitter/X": f"https://twitter.com/{name}",
        "Instagram": f"https://instagram.com/{name}",
        "TikTok": f"https://tiktok.com/@{name}",
        "Reddit": f"https://reddit.com/u/{name}",
        "YouTube": f"https://youtube.com/@{name}",
        "Telegram": f"https://t.me/{name}",
        "Pinterest": f"https://pinterest.com/{name}",
        "LinkedIn": f"https://linkedin.com/in/{name}",
        "Snapchat": f"https://snapchat.com/add/{name}",
    }
    lines = [
        "```\n╔══════════════════════════╗\n"
        "║  🕵️  USERNAME HUNTER     ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🔎 Searching: `{name}`\n\n"
    ]
    for p, url in platforms.items():
        lines.append(f"▸ [{p}]({url})")
    lines.append(f"\n_Click to check availability!_")
    bot.reply_to(message, "\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['fakeid'])
def fakeid_cmd(message):
    generate_fake_id(message.chat.id)

def generate_fake_id(chat_id):
    fn = random.choice(["Alex","Jordan","Morgan","Taylor","Casey","Riley","Dakota","Skyler","Avery","Quinn","Blake","Drew"])
    ln = random.choice(["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Moore","Anderson"])
    city = random.choice(["New York","London","Tokyo","Berlin","Paris","Sydney","Toronto","Dubai","Singapore","Mumbai","Seoul"])
    email = f"{fn.lower()}.{ln.lower()}{random.randint(10,999)}@{random.choice(['gmail.com','yahoo.com','proton.me','outlook.com'])}"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    dob = f"{random.randint(1970,2004)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  💀  FAKE IDENTITY GEN   ║\n"
        "╚══════════════════════════╝\n```\n"
        f"👤 Name: `{fn} {ln}`\n"
        f"🎂 DOB: `{dob}`\n"
        f"🏙️ City: `{city}`\n"
        f"📧 Email: `{email}`\n"
        f"📱 Phone: `{phone}`\n"
        f"🔑 Password: `{fn.lower()}@{random.randint(1000,9999)}!`\n\n"
        "⚠️ _Educational purposes only!_"
    )
    bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(commands=['portscan'])
def portscan_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/portscan <host>`", parse_mode="Markdown"); return
    host = parts[1].strip()
    ports = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
             143:"IMAP",443:"HTTPS",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",
             6379:"Redis",8080:"HTTP-Alt",8443:"HTTPS-Alt",27017:"MongoDB"}
    lines = [
        "```\n╔══════════════════════════╗\n"
        "║  📡  PORT INFO PANEL     ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🎯 Target: `{host}`\n\n"
    ]
    for port, svc in ports.items():
        lines.append(f"▸ `{port:5d}` → {svc}")
    lines.append("\n⚠️ _Unauthorized scanning is illegal!_")
    bot.reply_to(message, "\n".join(lines), parse_mode="Markdown")

@bot.message_handler(commands=['phish'])
def phish_cmd(message):
    send_phish_info(message.chat.id)

def send_phish_info(chat_id):
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║  ⚡  PHISHING AWARENESS   ║\n"
        "╚══════════════════════════╝\n```\n"
        "🎣 *What is Phishing?*\n"
        "Attackers trick you into revealing passwords/data.\n\n"
        "🔴 *Red Flags:*\n"
        "▸ Urgent: 'Your account will be deleted!'\n"
        "▸ Suspicious URLs (check carefully!)\n"
        "▸ Password requests via email/SMS\n"
        "▸ Too-good-to-be-true offers\n"
        "▸ Fake login pages\n\n"
        "🛡️ *Stay Safe:*\n"
        "▸ Always verify URLs before clicking\n"
        "▸ Enable 2FA on all accounts\n"
        "▸ Never share passwords\n"
        "▸ Use a password manager\n"
        "▸ Keep all software updated\n\n"
        "⚠️ _Educational purposes only!_"
    )
    bot.send_message(chat_id, msg, parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  UTILITY  COMMANDS
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['joke'])
def joke_cmd(message): send_joke(message.chat.id)

def send_joke(chat_id):
    jokes = [
        "Why do hackers prefer dark mode? Because light attracts bugs! 🐛",
        "A SQL query walks into a bar and asks two tables: 'Can I join you?' 😄",
        "How many programmers does it take to change a light bulb? None — that's a hardware problem! 💡",
        "There are 10 types of people: those who understand binary and those who don't. 0️⃣1️⃣",
        "Why did the hacker break up with the internet? Too many phishing attempts! 🎣",
        "Why was the JavaScript developer sad? He didn't know how to 'null' his feelings! 😢",
        "A Wi-Fi router walks into a bar. The bartender says, 'We don't serve your type.' 📡",
        "Why do programmers prefer iOS? Because they hate Windows! 🖥️",
    ]
    bot.send_message(chat_id, f"😂 *Hacker Joke:*\n\n_{random.choice(jokes)}_", parse_mode="Markdown")

@bot.message_handler(commands=['quote'])
def quote_cmd(message): send_quote(message.chat.id)

def send_quote(chat_id):
    quotes = [
        "\"The quieter you become, the more you are able to hear.\" — Kali Linux",
        "\"Hacking is not a crime, it's an art.\" — Anonymous",
        "\"The only secure computer is one that's unplugged.\" — Unknown",
        "\"Knowledge is power. Guard it well.\" — Unknown",
        "\"Privacy is not for the timid.\" — Anonymous",
        "\"In a world of zeros and ones, be the exception.\" — Unknown",
        "\"The best defense is a good offense.\" — Sun Tzu",
        "\"Security is not a product, but a process.\" — Bruce Schneier",
    ]
    bot.send_message(chat_id, f"💬 *Hacker Quote:*\n\n_{random.choice(quotes)}_", parse_mode="Markdown")

@bot.message_handler(commands=['coin'])
def coin_cmd(message):
    r = random.choice(["🪙 Heads", "🔄 Tails"])
    bot.reply_to(message, f"🪙 *Coin Flip Result:*\n\n*{r}*", parse_mode="Markdown")

@bot.message_handler(commands=['dice'])
def dice_cmd(message):
    r = random.randint(1, 6)
    faces = ["","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
    bot.reply_to(message, f"🎲 *Dice Roll:* {faces[r]} = `{r}`", parse_mode="Markdown")

@bot.message_handler(commands=['uuid'])
def uuid_cmd(message):
    bot.reply_to(message, f"🆔 *UUID:*\n`{uuid_lib.uuid4()}`", parse_mode="Markdown")

@bot.message_handler(commands=['calc'])
def calc_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/calc 2+2*10`", parse_mode="Markdown"); return
    expr = parts[1].strip()
    try:
        if not all(c in '0123456789+-*/.() ' for c in expr): raise ValueError
        result = eval(expr)
        bot.reply_to(message, f"🧮 `{expr}` = `{result}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Invalid expression!")

@bot.message_handler(commands=['time'])
def time_cmd(message): send_time(message.chat.id)

def send_time(chat_id):
    zones = {"🇺🇸 New York":-5,"🇬🇧 London":0,"🇩🇪 Berlin":1,"🇦🇪 Dubai":4,
             "🇮🇳 India":5.5,"🇵🇰 Pakistan":5,"🇨🇳 China":8,"🇯🇵 Tokyo":9,"🇦🇺 Sydney":10}
    now = datetime.now(timezone.utc)
    lines = ["```\n╔══════════════════════════╗\n║   ⏰  WORLD TIME ZONES   ║\n╚══════════════════════════╝\n```\n"]
    for zone, offset in zones.items():
        tz = timezone(timedelta(hours=offset))
        t = now.astimezone(tz).strftime('%H:%M:%S')
        lines.append(f"{zone}: `{t}`")
    bot.send_message(chat_id, "\n".join(lines), parse_mode="Markdown")

@bot.message_handler(commands=['color'])
def color_cmd(message): send_color(message.chat.id)

def send_color(chat_id):
    r, g, b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
    hex_c = f"#{r:02X}{g:02X}{b:02X}"
    bot.send_message(chat_id, f"🌈 *Random Color*\n\n🎨 HEX: `{hex_c}`\n🔴 R:`{r}` 🟢 G:`{g}` 🔵 B:`{b}`", parse_mode="Markdown")

@bot.message_handler(commands=['fact'])
def fact_cmd(message): send_fact(message.chat.id)

def send_fact(chat_id):
    facts = [
        "The first computer virus was created in 1983 by Fred Cohen! 🦠",
        "Google processes over 8.5 billion searches per day! 🔍",
        "The first email was sent in 1971 by Ray Tomlinson to himself! 📧",
        "Python was named after Monty Python, not the snake! 🐍",
        "The first computer bug was an actual moth found in 1947! 🦗",
        "Linux powers 96.3% of the world's top 1 million servers! 🐧",
        "About 90% of world currency exists only on computers! 💰",
        "The average person has 100 passwords to remember! 🔑",
        "There are over 4.5 billion internet users worldwide! 🌐",
        "Bitcoin was created by the anonymous person 'Satoshi Nakamoto' in 2008! ₿",
    ]
    bot.send_message(chat_id, f"💡 *Tech Fact:*\n\n_{random.choice(facts)}_", parse_mode="Markdown")

@bot.message_handler(commands=['ascii'])
def ascii_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/ascii <text>`", parse_mode="Markdown"); return
    bot.reply_to(message, f"🔤 *Hacker Font:*\n`{hk(parts[1].strip()[:20])}`", parse_mode="Markdown")

@bot.message_handler(commands=['morse'])
def morse_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/morse <text>`", parse_mode="Markdown"); return
    mc = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
          'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
          'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---',
          '3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'}
    result = ' '.join(mc.get(c.upper(),'?') for c in parts[1].strip() if c != ' ')
    bot.reply_to(message, f"📡 *Morse Code:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['binary'])
def binary_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/binary <text>`", parse_mode="Markdown"); return
    result = ' '.join(format(ord(c), '08b') for c in parts[1].strip()[:20])
    bot.reply_to(message, f"💻 *Binary:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['hex'])
def hex_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/hex <text>`", parse_mode="Markdown"); return
    result = ' '.join(format(ord(c), '02X') for c in parts[1].strip()[:30])
    bot.reply_to(message, f"🔢 *Hex:*\n`{result}`", parse_mode="Markdown")

@bot.message_handler(commands=['reverse'])
def reverse_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/reverse <text>`", parse_mode="Markdown"); return
    bot.reply_to(message, f"🔄 *Reversed:*\n`{parts[1].strip()[::-1]}`", parse_mode="Markdown")

@bot.message_handler(commands=['wiki'])
def wiki_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/wiki <topic>`", parse_mode="Markdown"); return
    topic = parts[1].strip().replace(' ', '_')
    try:
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}", timeout=10).json()
        extract = r.get('extract','Not found.')[:600]
        page_url = r.get('content_urls',{}).get('desktop',{}).get('page','')
        bot.reply_to(message, f"📚 *{r.get('title',topic)}*\n\n{extract}\n\n[Read more »]({page_url})", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Wikipedia fetch failed.")

@bot.message_handler(commands=['crypto'])
def crypto_cmd(message):
    fetch_all_crypto(message.chat.id)

@bot.message_handler(commands=['convert'])
def convert_cmd(message):
    parts = message.text.split(' ')
    if len(parts) < 4:
        bot.reply_to(message, "Usage: `/convert <amount> <from> <to>`\nExample: `/convert 1 btc usd`", parse_mode="Markdown"); return
    try:
        amount = float(parts[1])
        from_c = parts[2].lower()
        to_c = parts[3].lower()
        coin_ids = {"btc":"bitcoin","eth":"ethereum","doge":"dogecoin","sol":"solana","bnb":"binancecoin"}
        coin = coin_ids.get(from_c, from_c)
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={to_c}", timeout=10).json()
        price = r.get(coin,{}).get(to_c)
        if price:
            total = amount * price
            bot.reply_to(message, f"🔄 *Crypto Converter*\n\n`{amount} {from_c.upper()}` = `{total:,.4f} {to_c.upper()}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Invalid currency pair.")
    except:
        bot.reply_to(message, "❌ Conversion failed.")

@bot.message_handler(commands=['ping'])
def ping_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/ping <host>`", parse_mode="Markdown"); return
    host = parts[1].strip()
    start = time.time()
    try:
        r = requests.get(f"http://{host}", timeout=7)
        elapsed = round((time.time() - start) * 1000, 2)
        bot.reply_to(message, f"📡 *Ping: `{host}`*\n⏱️ Response: `{elapsed}ms`\n✅ Status: `{r.status_code}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, f"📡 *Ping: `{host}`*\n❌ Unreachable / Timeout", parse_mode="Markdown")

@bot.message_handler(commands=['weather'])
def weather_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/weather <city>`", parse_mode="Markdown"); return
    city = parts[1].strip()
    try:
        r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10).json()
        c = r['current_condition'][0]
        msg = (
            "```\n╔══════════════════════════╗\n"
            f"║  🌤️  WEATHER: {city[:12]:^12}  ║\n"
            "╚══════════════════════════╝\n```\n"
            f"🌡️ Temp: `{c['temp_C']}°C / {c['temp_F']}°F`\n"
            f"🤔 Feels Like: `{c['FeelsLikeC']}°C`\n"
            f"☁️ Condition: `{c['weatherDesc'][0]['value']}`\n"
            f"💧 Humidity: `{c['humidity']}%`\n"
            f"💨 Wind: `{c['windspeedKmph']} km/h`\n"
            f"👁️ Visibility: `{c['visibility']} km`"
        )
        bot.reply_to(message, msg, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ City not found or service unavailable.")

@bot.message_handler(commands=['short'])
def short_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/short <url>`", parse_mode="Markdown"); return
    try:
        r = requests.get(f"https://tinyurl.com/api-create.php?url={parts[1].strip()}", timeout=10)
        bot.reply_to(message, f"🔗 *Shortened URL:*\n\n{r.text}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Could not shorten URL.")

@bot.message_handler(commands=['qr'])
def qr_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/qr <text or url>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={requests.utils.quote(text)}"
    bot.send_photo(message.chat.id, qr_url, caption=f"📱 *QR Code*\n\n`{text[:100]}`", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  CIPHER  COMMANDS
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['rot13'])
def rot13_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/rot13 <text>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    result = ''.join(
        chr((ord(c) - 65 + 13) % 26 + 65) if c.isupper()
        else chr((ord(c) - 97 + 13) % 26 + 97) if c.islower()
        else c for c in text
    )
    bot.reply_to(message,
        f"🔁 *ROT13 Result*\n\n"
        f"📝 Input: `{text}`\n"
        f"🔐 Output: `{result}`\n\n"
        f"_Apply again to decode!_",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['caesar'])
def caesar_cmd(message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Usage: `/caesar <shift> <text>`\nExample: `/caesar 3 hello`", parse_mode="Markdown"); return
    try:
        shift = int(parts[1]) % 26
        text = parts[2]
        result = ''.join(
            chr((ord(c) - 65 + shift) % 26 + 65) if c.isupper()
            else chr((ord(c) - 97 + shift) % 26 + 97) if c.islower()
            else c for c in text
        )
        bot.reply_to(message,
            f"🏛️ *Caesar Cipher*\n\n"
            f"📝 Input: `{text}`\n"
            f"🔢 Shift: `{shift}`\n"
            f"🔐 Encoded: `{result}`\n\n"
            f"_Use shift {26-shift} to decode!_",
            parse_mode="Markdown"
        )
    except:
        bot.reply_to(message, "❌ Invalid shift value. Use a number.")

@bot.message_handler(commands=['atbash'])
def atbash_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/atbash <text>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    result = ''.join(
        chr(90 - (ord(c) - 65)) if c.isupper()
        else chr(122 - (ord(c) - 97)) if c.islower()
        else c for c in text
    )
    bot.reply_to(message,
        f"🔤 *Atbash Cipher*\n\n"
        f"📝 Input: `{text}`\n"
        f"🔐 Output: `{result}`\n\n"
        f"_A↔Z, B↔Y, C↔X... Symmetric!_",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['vigenere'])
def vigenere_cmd(message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Usage: `/vigenere <key> <text>`\nExample: `/vigenere secret hello`", parse_mode="Markdown"); return
    key = parts[1].lower()
    text = parts[2]
    result = []
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - 97
            base = 65 if c.isupper() else 97
            result.append(chr((ord(c) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(c)
    bot.reply_to(message,
        f"🌿 *Vigenere Cipher*\n\n"
        f"🔑 Key: `{key}`\n"
        f"📝 Input: `{text}`\n"
        f"🔐 Encoded: `{''.join(result)}`",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['xor'])
def xor_cmd(message):
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Usage: `/xor <key_number> <text>`\nExample: `/xor 42 hello`", parse_mode="Markdown"); return
    try:
        key = int(parts[1]) % 256
        text = parts[2]
        result = ''.join(chr(ord(c) ^ key) for c in text)
        hex_out = ' '.join(f'{ord(c):02X}' for c in result)
        bot.reply_to(message,
            f"⚡ *XOR Cipher*\n\n"
            f"🔑 Key: `{key}` (0x{key:02X})\n"
            f"📝 Input: `{text}`\n"
            f"🔐 Hex Output: `{hex_out[:200]}`\n\n"
            f"_Apply same key to decode!_",
            parse_mode="Markdown"
        )
    except:
        bot.reply_to(message, "❌ Key must be a number (0-255).")

@bot.message_handler(commands=['base32'])
def base32_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/base32 <text>`", parse_mode="Markdown"); return
    import base64 as b64
    encoded = b64.b32encode(parts[1].strip().encode()).decode()
    bot.reply_to(message, f"💠 *Base32 Encoded:*\n\n`{encoded}`", parse_mode="Markdown")

@bot.message_handler(commands=['urlencode'])
def urlencode_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/urlencode <text>`", parse_mode="Markdown"); return
    from urllib.parse import quote
    encoded = quote(parts[1].strip())
    bot.reply_to(message, f"📦 *URL Encoded:*\n\n`{encoded}`", parse_mode="Markdown")

# ─────────────────────────────────────────────────────────
#  PRO TOOL  COMMANDS
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['strength'])
def strength_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/strength <password>`", parse_mode="Markdown"); return
    pwd = parts[1].strip()
    score = 0
    feedback = []
    if len(pwd) >= 8: score += 1
    else: feedback.append("▸ Use at least 8 characters")
    if len(pwd) >= 12: score += 1
    if any(c.isupper() for c in pwd): score += 1
    else: feedback.append("▸ Add uppercase letters (A-Z)")
    if any(c.islower() for c in pwd): score += 1
    else: feedback.append("▸ Add lowercase letters (a-z)")
    if any(c.isdigit() for c in pwd): score += 1
    else: feedback.append("▸ Add numbers (0-9)")
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd): score += 1
    else: feedback.append("▸ Add special characters (!@#$...)")
    if len(set(pwd)) > len(pwd) * 0.6: score += 1
    bars = "█" * score + "░" * (7 - score)
    levels = {0:"💀 Very Weak",1:"🔴 Weak",2:"🔴 Weak",3:"🟠 Fair",4:"🟡 Moderate",5:"🟢 Strong",6:"🟢 Strong",7:"💎 Excellent"}
    level = levels.get(score, "Unknown")
    tips = "\n".join(feedback) if feedback else "✅ Great password!"
    bot.reply_to(message,
        f"💪 *Password Strength Analyzer*\n\n"
        f"🔑 Password: `{'*' * len(pwd)}`\n"
        f"📏 Length: `{len(pwd)}`\n\n"
        f"📊 Strength: `[{bars}]` {score}/7\n"
        f"🏷️ Rating: *{level}*\n\n"
        f"💡 *Suggestions:*\n{tips}",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['email'])
def email_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/email <email_address>`", parse_mode="Markdown"); return
    email_addr = parts[1].strip()
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    valid = bool(re.match(pattern, email_addr))
    if valid:
        local, domain = email_addr.split('@', 1)
        providers = {"gmail.com":"🔵 Google","yahoo.com":"🟣 Yahoo","hotmail.com":"🔷 Microsoft",
                     "outlook.com":"🔷 Microsoft","proton.me":"🟢 ProtonMail","icloud.com":"⚪ Apple"}
        provider = providers.get(domain.lower(), f"🌐 {domain}")
        msg = (
            f"📧 *Email Validator*\n\n"
            f"✅ *Valid Email!*\n\n"
            f"📨 Address: `{email_addr}`\n"
            f"👤 Local: `{local}`\n"
            f"🌐 Domain: `{domain}`\n"
            f"📡 Provider: {provider}"
        )
    else:
        msg = f"📧 *Email Validator*\n\n❌ *Invalid Email!*\n\n`{email_addr}`\n\n_Check format: user@domain.com_"
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(commands=['analyze'])
def analyze_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/analyze <text>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(' ', ''))
    sentences = len([s for s in re.split(r'[.!?]+', text) if s.strip()])
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    reading_time = max(1, round(words / 200))
    unique_words = len(set(w.lower().strip('.,!?') for w in text.split()))
    bot.reply_to(message,
        f"📝 *Text Analyzer Results*\n\n"
        f"📊 *Statistics:*\n"
        f"▸ Words: `{words}`\n"
        f"▸ Characters: `{chars}`\n"
        f"▸ Chars (no spaces): `{chars_no_space}`\n"
        f"▸ Sentences: `{sentences}`\n"
        f"▸ Paragraphs: `{paragraphs}`\n"
        f"▸ Unique Words: `{unique_words}`\n\n"
        f"⏱️ *Reading Time:* `~{reading_time} min`\n"
        f"📖 *Avg Word Length:* `{chars_no_space//max(words,1)} chars`",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['prime'])
def prime_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/prime <number>`\nExample: `/prime 97`", parse_mode="Markdown"); return
    try:
        n = int(parts[1].strip())
        if n < 2:
            is_prime = False
        elif n == 2:
            is_prime = True
        elif n % 2 == 0:
            is_prime = False
        else:
            is_prime = all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))
        result = "✅ *PRIME NUMBER!*" if is_prime else "❌ *NOT a prime number*"
        factors = []
        if not is_prime and n > 1:
            temp = n
            d = 2
            while d * d <= temp:
                while temp % d == 0:
                    factors.append(d)
                    temp //= d
                d += 1
            if temp > 1: factors.append(temp)
        factor_str = f"\n🔢 Factors: `{' × '.join(map(str, factors))}`" if factors else ""
        bot.reply_to(message,
            f"🔢 *Prime Number Checker*\n\n"
            f"Number: `{n:,}`\n"
            f"{result}{factor_str}",
            parse_mode="Markdown"
        )
    except:
        bot.reply_to(message, "❌ Please provide a valid integer.")

@bot.message_handler(commands=['factorial'])
def factorial_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/factorial <number>`\nExample: `/factorial 10`", parse_mode="Markdown"); return
    try:
        n = int(parts[1].strip())
        if n < 0:
            bot.reply_to(message, "❌ Factorial undefined for negative numbers!"); return
        if n > 50:
            bot.reply_to(message, "❌ Too large! Max 50."); return
        result = math.factorial(n)
        bot.reply_to(message,
            f"🧮 *Factorial Calculator*\n\n"
            f"`{n}!` = `{result:,}`\n\n"
            f"📏 Digits: `{len(str(result))}`",
            parse_mode="Markdown"
        )
    except:
        bot.reply_to(message, "❌ Invalid number.")

@bot.message_handler(commands=['country'])
def country_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/country <name>`\nExample: `/country Pakistan`", parse_mode="Markdown"); return
    country = parts[1].strip()
    try:
        r = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10).json()
        if isinstance(r, list) and len(r) > 0:
            d = r[0]
            name = d.get('name', {}).get('common', country)
            capital = d.get('capital', ['N/A'])[0] if d.get('capital') else 'N/A'
            region = d.get('region', 'N/A')
            subregion = d.get('subregion', 'N/A')
            population = d.get('population', 0)
            area = d.get('area', 0)
            currencies = ', '.join([v.get('name','') for v in d.get('currencies',{}).values()])
            languages = ', '.join(d.get('languages',{}).values())
            flag = d.get('flag', '')
            bot.reply_to(message,
                f"🌍 *Country Info: {name}* {flag}\n\n"
                f"🏛️ Capital: `{capital}`\n"
                f"🌐 Region: `{region}` › `{subregion}`\n"
                f"👥 Population: `{population:,}`\n"
                f"📐 Area: `{area:,} km²`\n"
                f"💰 Currency: `{currencies}`\n"
                f"🗣️ Languages: `{languages}`",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(message, "❌ Country not found.")
    except:
        bot.reply_to(message, "❌ Could not fetch country data.")

@bot.message_handler(commands=['check'])
def check_url_cmd(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/check <url>`\nExample: `/check https://google.com`", parse_mode="Markdown"); return
    url = parts[1].strip()
    if not url.startswith('http'):
        url = 'https://' + url
    start = time.time()
    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        elapsed = round((time.time() - start) * 1000, 2)
        status = r.status_code
        status_emoji = "✅" if status < 300 else "⚠️" if status < 400 else "❌"
        final_url = r.url
        content_type = r.headers.get('Content-Type', 'Unknown')[:40]
        server = r.headers.get('Server', 'Unknown')[:30]
        bot.reply_to(message,
            f"🔗 *Link Checker*\n\n"
            f"🌐 URL: `{url[:60]}`\n"
            f"{status_emoji} Status: `{status}`\n"
            f"⏱️ Response: `{elapsed}ms`\n"
            f"📡 Server: `{server}`\n"
            f"📄 Content: `{content_type}`\n"
            f"🔀 Final URL: `{final_url[:60]}`",
            parse_mode="Markdown"
        )
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, f"🔗 *Link Checker*\n\n❌ *DEAD LINK!*\n\n`{url}`\n\nHost unreachable.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: `{str(e)[:100]}`", parse_mode="Markdown")

@bot.message_handler(commands=['uptime'])
def uptime_cmd(message):
    send_uptime(message.chat.id)

@bot.message_handler(commands=['sysinfo'])
def sysinfo_cmd(message):
    send_sysinfo(message.chat.id)

@bot.message_handler(commands=['botstats'])
def botstats_cmd(message):
    send_bot_stats(message.chat.id)

# ─────────────────────────────────────────────────────────
#  ADMIN  PANEL
# ─────────────────────────────────────────────────────────
def send_admin_panel(chat_id, user_id):
    if admin_data["owner_id"] and user_id != admin_data["owner_id"]:
        bot.send_message(chat_id, "⛔ *Admin Panel — Restricted*\n\nOnly the bot owner can access this.", parse_mode="Markdown"); return
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📊  Statistics",   callback_data="adm_stats"),
        InlineKeyboardButton("📢  Broadcast",    callback_data="adm_broadcast"),
    )
    m.add(
        InlineKeyboardButton("🚫  Ban User",     callback_data="adm_ban"),
        InlineKeyboardButton("✅  Unban User",   callback_data="adm_unban"),
    )
    m.add(
        InlineKeyboardButton("👥  User List",    callback_data="adm_users"),
        InlineKeyboardButton("💀  Hacker Mode",  callback_data="adm_hacker"),
    )
    m.add(InlineKeyboardButton("🏠  Back to Main Menu", callback_data="menu_back"))
    bot.send_message(
        chat_id,
        "```\n╔══════════════════════════╗\n"
        "║  👑  ADMIN CONTROL PANEL ║\n"
        "║  DARK HACKER ZONE v2.0   ║\n"
        "╚══════════════════════════╝\n```\n"
        f"🤖 Bot: *{hk('voidxdownloder')}*\n"
        f"👑 Owner: *{hk(OWNER)}*\n"
        f"👥 Total Users: `{admin_data['user_count']}`\n"
        f"🚫 Banned: `{len(admin_data['banned_users'])}`\n"
        f"📊 Status: 🟢 Online",
        parse_mode="Markdown",
        reply_markup=m
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("adm_"))
def cb_admin(call):
    if admin_data["owner_id"] and call.from_user.id != admin_data["owner_id"]:
        bot.answer_callback_query(call.id, "⛔ Owner only!", show_alert=True); return
    bot.answer_callback_query(call.id)
    a = call.data[4:]
    cid = call.message.chat.id
    if a == "stats":
        bot.send_message(cid,
            f"📊 *Bot Statistics*\n\n"
            f"👥 Total Users: `{admin_data['user_count']}`\n"
            f"🚫 Banned Users: `{len(admin_data['banned_users'])}`\n"
            f"🟢 Bot Status: Online",
            parse_mode="Markdown"
        )
    elif a == "broadcast":
        bot.send_message(cid, "📢 Usage: `/broadcast <message>`", parse_mode="Markdown")
    elif a == "ban":
        bot.send_message(cid, "🚫 Usage: `/ban <user_id>`", parse_mode="Markdown")
    elif a == "unban":
        bot.send_message(cid, "✅ Usage: `/unban <user_id>`", parse_mode="Markdown")
    elif a == "users":
        uid_list = ", ".join(str(u) for u in admin_data["users"][-10:])
        bot.send_message(cid, f"👥 *Last 10 Users:*\n`{uid_list or 'None'}`", parse_mode="Markdown")
    elif a == "hacker":
        bot.send_message(cid, f"```\n💀 DARK HACKER ZONE ACTIVATED\n{hk('POWERED BY DEATH DREAM')}\n```", parse_mode="Markdown")

@bot.message_handler(commands=['setowner'])
def setowner_cmd(message):
    if admin_data["owner_id"] is None:
        admin_data["owner_id"] = message.from_user.id
        bot.reply_to(message, f"✅ *You are now the Owner!*\n👑 ID: `{message.from_user.id}`", parse_mode="Markdown")
    elif message.from_user.id == admin_data["owner_id"]:
        bot.reply_to(message, "👑 You are already the owner!")
    else:
        bot.reply_to(message, "⛔ Owner already assigned!")

@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only!"); return
    bot.reply_to(message,
        f"📊 *Bot Stats*\n👥 Users: `{admin_data['user_count']}`\n"
        f"🚫 Banned: `{len(admin_data['banned_users'])}`",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['broadcast'])
def broadcast_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only!"); return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/broadcast <message>`", parse_mode="Markdown"); return
    text = parts[1].strip()
    sent = 0
    for uid in admin_data["users"]:
        try:
            bot.send_message(uid, f"📢 *BROADCAST*\n\n{text}\n\n— 👑 {hk(OWNER)}", parse_mode="Markdown")
            sent += 1
        except: pass
    bot.reply_to(message, f"✅ Sent to `{sent}` users!", parse_mode="Markdown")

@bot.message_handler(commands=['ban'])
def ban_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only!"); return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/ban <user_id>`", parse_mode="Markdown"); return
    try:
        uid = int(parts[1].strip())
        if uid not in admin_data["banned_users"]:
            admin_data["banned_users"].append(uid)
            bot.reply_to(message, f"🚫 User `{uid}` banned!", parse_mode="Markdown")
        else:
            bot.reply_to(message, "Already banned!")
    except:
        bot.reply_to(message, "❌ Invalid user ID!")

@bot.message_handler(commands=['unban'])
def unban_cmd(message):
    if admin_data["owner_id"] and message.from_user.id != admin_data["owner_id"]:
        bot.reply_to(message, "⛔ Admin only!"); return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Usage: `/unban <user_id>`", parse_mode="Markdown"); return
    try:
        uid = int(parts[1].strip())
        if uid in admin_data["banned_users"]:
            admin_data["banned_users"].remove(uid)
            bot.reply_to(message, f"✅ User `{uid}` unbanned!", parse_mode="Markdown")
        else:
            bot.reply_to(message, "User is not banned!")
    except:
        bot.reply_to(message, "❌ Invalid user ID!")

# ─────────────────────────────────────────────────────────
#  /help  COMMAND
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['help'])
def help_cmd(message): send_help(message.chat.id)

def send_help(chat_id):
    msg = (
        "```\n╔══════════════════════════╗\n"
        "║   📖  FULL COMMAND LIST  ║\n"
        "╚══════════════════════════╝\n```\n"
        "📥 *VIDEO DOWNLOADERS*\n"
        "`/tiktok` `/youtube` `/instagram`\n"
        "`/facebook` `/twitter`\n\n"
        "💀 *HACKER TOOLS*\n"
        "`/ip` `/whoami` `/hash` `/encode` `/decode`\n"
        "`/passgen` `/username` `/fakeid` `/portscan`\n"
        "`/phish` `/dns`\n\n"
        "🛠️ *UTILITY TOOLS*\n"
        "`/calc` `/weather` `/joke` `/quote` `/coin`\n"
        "`/dice` `/uuid` `/qr` `/short` `/ping`\n"
        "`/time` `/crypto` `/convert` `/wiki`\n"
        "`/color` `/fact` `/ascii` `/morse`\n"
        "`/binary` `/hex` `/reverse`\n\n"
        "👑 *ADMIN COMMANDS*\n"
        "`/setowner` `/broadcast` `/stats`\n"
        "`/ban` `/unban`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 Owner: {hk(OWNER)}\n"
        f"📢 Channel: @HACKERQUEEN9\n"
        f"💬 WhatsApp: [Join]({CHANNEL_WA})"
    )
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🏠  Main Menu", callback_data="menu_back"))
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=m, disable_web_page_preview=True)

# ─────────────────────────────────────────────────────────
#  MIDDLEWARE  — track users
# ─────────────────────────────────────────────────────────
@bot.middleware_handler(update_types=['message'])
def track_users(bot_instance, message):
    if message.from_user:
        uid = message.from_user.id
        if uid not in admin_data["users"]:
            admin_data["users"].append(uid)
            admin_data["user_count"] += 1
        if uid in admin_data["banned_users"]:
            return

# ─────────────────────────────────────────────────────────
#  FLASK  keep-alive  +  main
# ─────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <html><head><title>{BOT_NAME}</title></head>
    <body style='background:#0a0a0a;color:#00ff41;font-family:monospace;text-align:center;padding:50px'>
    <pre>
██╗   ██╗ ██████╗ ██╗██████╗ ██╗  ██╗
██║   ██║██╔═══██╗██║██╔══██╗╚██╗██╔╝
██║   ██║██║   ██║██║██║  ██║ ╚███╔╝
╚██╗ ██╔╝██║   ██║██║██║  ██║ ██╔██╗
 ╚████╔╝ ╚██████╔╝██║██████╔╝██╔╝ ██╗
  ╚═══╝   ╚═════╝ ╚═╝╚═════╝ ╚═╝  ╚═╝
    </pre>
    <h2 style='color:#00ff41'>🟢 BOT IS ONLINE</h2>
    <p>POWERED BY DARK HACKER ZONE</p>
    <p>OWNER: DEATH DREAM</p>
    </body></html>
    """

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
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
