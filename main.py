from pathlib import Path
import re

src = Path('/mnt/data/main.py.file')
text = src.read_text(errors='ignore')

# Fix bot name typo
text = text.replace('voidxdownloder', 'voidxdownloader')

# Remove duplicate import time
text = text.replace('import time\nfrom datetime', 'from datetime', 1)

# Add advanced /wish command before Flask section if not already added
wish_code = r'''

# ─────────────────────────────────────────────────────────
#  ADVANCED WISH COMMAND
# ─────────────────────────────────────────────────────────
@bot.message_handler(commands=['wish'])
def wish_command(message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(
            message,
            "✨ *Advanced Wish Generator*\n\n"
            "Usage:\n`/wish Your Name`\n\n"
            "Example:\n`/wish Adeel`",
            parse_mode="Markdown"
        )
        return

    name = args[1]

    wishes = [
        f"🌟 *Special Wish For {name}* 🌟\n\nMay your life be filled with success, happiness, power and endless achievements. ⚡",
        f"💀 *Dark Hacker Blessing For {name}* 💀\n\nMay you conquer every challenge and rise stronger every day. 🔥",
        f"🚀 *Legendary Wish For {name}* 🚀\n\nMay fortune, respect and victory always stay with you.",
        f"✨ *Motivational Wish* ✨\n\n{name}, never stop believing in yourself. Great things are coming!"
    ]

    bot.send_message(
        message.chat.id,
        random.choice(wishes),
        parse_mode="Markdown"
    )

# ─────────────────────────────────────────────────────────
#  FULL HOROSCOPE SYSTEM
# ─────────────────────────────────────────────────────────
HOROSCOPE_DATA = {
    "Aries": "🔥 Today is perfect for bold moves and new beginnings.",
    "Taurus": "🌿 Stability and peace will guide your decisions today.",
    "Gemini": "💬 Communication brings unexpected opportunities.",
    "Cancer": "🌊 Trust your emotions but stay focused on goals.",
    "Leo": "🦁 Your confidence will attract success and attention.",
    "Virgo": "📚 Small details will help you win big today.",
    "Libra": "⚖️ Balance your work and personal life carefully.",
    "Scorpio": "🦂 Powerful energy surrounds your ambitions today.",
    "Sagittarius": "🏹 Adventure and learning bring positive vibes.",
    "Capricorn": "⛰️ Hard work will finally show results.",
    "Aquarius": "⚡ Creative ideas can change your future.",
    "Pisces": "🌌 Your intuition is stronger than ever today."
}

@bot.callback_query_handler(func=lambda c: c.data.startswith("horo_"))
def cb_horoscope(call):
    sign = call.data.split("_")[1]

    msg = (
        f"☀️ *{sign} Horoscope* ☀️\\n\\n"
        f"{HOROSCOPE_DATA.get(sign, 'Good luck is with you today!')}\\n\\n"
        f"💎 Lucky Number: `{random.randint(1,99)}`\\n"
        f"🎨 Lucky Color: `{random.choice(['Red','Blue','Black','Purple','Green','Silver'])}`\\n"
        f"🍀 Lucky Day: `{random.choice(['Monday','Tuesday','Wednesday','Thursday','Friday'])}`\\n\\n"
        f"⚡ Powered by VOID X DOWNLOADER"
    )

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

'''

# Insert before Flask app if not present
if 'ADVANCED WISH COMMAND' not in text:
    idx = text.find('app = Flask(__name__)')
    if idx != -1:
        text = text[:idx] + wish_code + '\n' + text[idx:]

# Fix duplicate polling issue
text = text.replace('''if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
  
bot.infinity_polling ()
''',
'''if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
''')

# Save updated file
out = Path('/mnt/data/voidxdownloader_fixed.py')
out.write_text(text)

print("Updated bot file created:", out)
print("Added:")
print("- /wish command")
print("- Advanced horoscope system")
print("- Polling fix")
print("- Bot name fix")
