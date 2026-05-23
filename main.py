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
    sign = ca
