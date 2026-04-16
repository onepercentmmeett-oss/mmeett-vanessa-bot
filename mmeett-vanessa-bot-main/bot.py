#!/usr/bin/env python3
"""
Vanessa - MMEETT FAQ Guide
Telegram Auto-Responder with Human Personality
Topic-aware: Welcomes in General Chat, Answers in FAQ
"""

import os
import re
import telebot
from telebot import types
import random

# Configuration from environment variables
TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID", "-1003884650831"))
GENERAL_CHAT_ID = int(os.environ.get("GENERAL_CHAT_ID", "5"))
FAQ_ID = int(os.environ.get("FAQ_ID", "9"))
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "ukkbasf")

# Links from environment
TUTORIAL_LINK = os.environ.get("TUTORIAL_LINK", "https://t.me/c/3884650831/41")
VAULT_LINK = os.environ.get("VAULT_LINK", "https://t.me/c/3884650831/7")
FAQ_LINK = os.environ.get("FAQ_LINK", "https://t.me/c/3884650831/9")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN not set!")
    print("Add it in Render Environment Variables as: BOT_TOKEN")
    exit(1)

# Initialize bot
bot = telebot.TeleBot(TOKEN)

print("🤖 Vanessa - MMEETT Guide started...")
print(f"📍 Monitoring group: {GROUP_ID}")
print(f"💬 General Chat Topic: {GENERAL_CHAT_ID}")
print(f"❓ FAQ Topic: {FAQ_ID}")
print(f"👤 Admin: @{ADMIN_USERNAME}")

# ============================================
# WELCOME MESSAGE (Human - No Bot Reveal)
# ============================================

def get_welcome_message(user_name):
    """Generate welcome message for new members"""
    return f"""
hey {user_name}, welcome to MMEETT X 1% Club! ⚡️

really glad to have u here!

so u don't feel lost, here's what each tab is for:

☕️ General Chat — hang out, introduce urself, connect with other members

📢 Announcement — company updates, zoom call links, official news

📂 The Vault — company PPT slides + professional resources (multiple languages)

🛠 Learn & Master MMEETT — step-by-step tutorials (videos + guides)

❓ Frequently Asked Questions — got a question? ask here! i'll answer ASAP

💡 first steps if u're new:
1. check the Tutorial tab for a video on how to purchase ur MMEETT package
2. have questions? drop them in the FAQ tab — i'm there to help!
3. want to invite friends? i've got a friendly message ready for u!

let's redefine how the world connects. 🚀

seriously though, if u need anything just holler! 😇
"""

def send_welcome_message(chat_id, topic_id, user_name):
    """Send welcome message to new member in General Chat only"""
    try:
        bot.send_message(
            chat_id,
            get_welcome_message(user_name),
            parse_mode="Markdown",
            message_thread_id=topic_id
        )
        print(f"✅ Welcome message sent to {user_name} in General Chat")
    except Exception as e:
        print(f"❌ Error sending welcome message: {e}")

# ============================================
# FAQ DATABASE - MMEETT Full Info
# ============================================

FAQ_DATABASE = {
    "PACKAGES": {
        "keywords": ["package", "packages", "tier", "tiers", "membership", "price", "prices", "pricing", "cost", "how much", "silver", "gold", "platinum", "diamond"],
        "response": """hey! we got 4 tiers:

🥈 **Silver** $200 USD (120 PV)
   Gratitude Bonus: 1.5x return (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Gratitude Bonus: 2x return (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Gratitude Bonus: 2.5x return (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Gratitude Bonus: 3x return (cap $16,200)

higher tier = bigger bonuses one

wanna know which one suits u ah? 😇
""",
    },
    "COMMISSION": {
        "keywords": ["commission", "earn", "earning", "money", "income", "bonus", "bonuses", "award", "awards", "payout", "roi"],
        "response": """ok so there's 7+2 bonus systems haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 floors, 0.3% each
🌐 **Sharing Award** — 20 generations, 0.4%

📊 **Tier Bonus** — 20%-40% (depends on ur level)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**

🎯 **Grade Difference Equal Prize** — 5%

🌍 **Global Dividend Award** — 6% (for 5-10 stars)

✈️ **Travel Points** — daily 10% increase

🙏 **Gratitude Bonus** — up to 3x return (profit sharing)

basically = more u build, more u earn lah 😇

want me explain any specific one ah?
""",
    },
    "RANKING": {
        "keywords": ["rank", "ranking", "star", "stars", "level", "explorer", "visionary", "upgrade", "promote"],
        "response": """we got 10 star levels one:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

each level = higher bonus percentage

requirements start from 10,000 PV and go up to millions depending on level

u're at what level now? can help u calculate what's next! 😇
""",
    },
    "CHARGING": {
        "keywords": ["charge", "charging", "battery", "power", "green light", "red light", "low battery", "50 hours", "full charge"],
        "response": """super easy one:

1️⃣ plug cable to MMEETT port
2️⃣ use 5V/0.5A adapter (DC-5V)
3️⃣ charge until light turn green

⏱️ battery = 50 hours total
💤 auto sleep after 10 min no activity

done 🔋
""",
    },
    "APP_DOWNLOAD": {
        "keywords": ["download", "app", "install", "application", "app store", "google play", "register", "sign up", "verification code"],
        "response": """app store or google play lah:

📲 **iOS**: App Store → search "MMEETT"
🤖 **Android**: Google Play → search "MMEETT"

after install:
• turn on bluetooth
• turn on NFC (for card writing)
• need Android 6+ or iOS 12+

if no verification code = check spam folder 😅

need help setting up? tag @ukkbasf leh
""",
    },
    "ACTIVATION": {
        "keywords": ["activate", "bind", "connect", "pair", "nfc", "card", "write", "link", "device", "trans"],
        "response": """ok here's how:

1️⃣ hold TRANS 1 sec (blue light = on)
2️⃣ white light flashes = ready to bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ place near phone (iPhone: top back)

to write card link:
• "Me" → "Activate MMEETT Device"
• select card → "Activate"
• phone NFC must be ON

got stuck? tag me leh 😇
""",
    },
    "RECORDING": {
        "keywords": ["record", "recording", "meeting", "call", "audio", "microphone", "start", "stop", "pause", "red light", "yellow light"],
        "response": """🎙️ **LIVE MODE** (no phone needed):
1. hold TRANS 1 sec (blue light)
2. switch MEETING up
3. vibration + RED light = recording

📞 **CALL MODE**:
1. hold TRANS 1 sec (blue light)
2. switch MEETING up
3. double-press TRANS (0.5 sec)
4. vibration + YELLOW light

⚠️ call mode: device must touch phone (no headphones)
❌ no pause feature (stop = new file)

got it? 😇
""",
    },
    "SYNC": {
        "keywords": ["sync", "transfer", "upload", "download", "wifi", "bluetooth", "file", "empty folder", "computer"],
        "response": """🔄 **Sync Recordings**:

1. connect device to app (Bluetooth)
2. app shows: "Files pending sync"
3. choose: Sync all OR select files
4. files auto-delete after sync

⚡️ transfer speeds:
• Bluetooth = ~tens of KB/sec (slow)
• WiFi = much faster (recommended)

📂 folder empty on computer? files auto-deleted after sync. export from app instead.

make sense ah? 😇
""",
    },
    "TRANSCRIPTION": {
        "keywords": ["transcribe", "transcript", "text", "convert", "write", "summary", "language", "translate"],
        "response": """📝 **Transcription**:

⏱️ time = ~50% of recording length
example: 1-hour recording = ~30 min

🌍 multi-language (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

pretty fast one! 😇
""",
    },
    "AI_CHAT": {
        "keywords": ["ai", "chat", "bot", "model", "gpt", "gemini", "deepseek", "search", "think mode", "mr mmeett"],
        "response": """🤖 **AI Chat Feature**:

1. go to "AI Chat" tab in app
2. chat with Mr. MMEETT agent
3. switch models: GPT, Gemini, DeepSeek
4. enable "Web Search" for real-time info
5. enable "Think Mode" for complex questions

💡 Think Mode = shows AI reasoning (DeepSeek/Gemini only)

want to try? 😇
""",
    },
    "SHIPPING": {
        "keywords": ["shipping", "delivery", "track", "order", "when arrive", "processing", "how long", "dispatch"],
        "response": """📦 **Shipping & Delivery**:

📦 processing: 3-5 business days
🚚 delivery: 6-15 business days

📍 track order:
App → "Me" → "Member" → "Orders"

🌍 worldwide shipping available

anything else ah? 😇
""",
    },
    "RETURNS": {
        "keywords": ["return", "refund", "exchange", "warranty", "repair", "broken", "20 day", "12 month", "defective"],
        "response": """🔄 **Returns & Warranty**:

🔄 returns: 20 days from purchase
• MMEETT Card, Membership, Computing power

🔧 warranty: 12 months from purchase
• free repairs during warranty
• need: serial number + proof of purchase

📞 contact: App → "Me" → "Customer Service"

got issues? tag @ukkbasf leh 😇
""",
    },
    "TRAVEL_POINTS": {
        "keywords": ["travel", "point", "points", "trip", "vacation", "bonus increase", "daily"],
        "response": """✈️ **Travel Points**:

daily 10% bonus increase one!

basically = every day ur bonus pool grows by 10%

use for:
• company trips
• events
• or convert to cash (depends on level)

pretty nice ah? 😇
""",
    },
    "GRADE_DIFFERENCE": {
        "keywords": ["grade difference", "equal prize", "team grade", "5 percent", "5%"],
        "response": """🎯 **Grade Difference Bonuses**:

**Team Grade Difference**:
earn from difference between ur level and ur team's level

**Grade Difference Equal Prize** = 5%
when u and ur referral same level, u still earn 5%

so even if u're same rank, still can earn! 😇

confusing ah? can explain more if u want!
""",
    },
    "GLOBAL_DIVIDEND": {
        "keywords": ["global", "dividend", "6 percent", "6%", "star", "5 star", "10 star"],
        "response": """🌍 **Global Dividend Award**:

6% of global pool shared among 5-10 star members

requirements:
• reach 5-star level minimum
• maintain performance

this is the big one lah — passive income from entire company growth! 😇

u're aiming for what level?
""",
    },
    "FAVORITE_COLOR": {
        "keywords": ["favourite color", "favorite color", "favourite colour", "favorite colour", "color", "colour", "fav color"],
        "response": """green for the colour of money lol 🤑🤑

(but seriously, MMEETT green like charging light one 🔋)
""",
    },
}

# Forward triggers (send to human admin)
FORWARD_TRIGGERS = [
    "bug", "crash", "error", "broken", "not working", "issue", "problem",
    "complaint", "angry", "unhappy", "scam", "fraud",
    "legal", "lawyer", "sue", "report",
]

# ============================================
# Helper Functions
# ============================================

def get_topic_id(message):
    """Extract topic ID from message"""
    if hasattr(message, 'message_thread_id'):
        return message.message_thread_id
    return None

def match_question(text):
    """Match question against FAQ database using word boundaries"""
    lower_text = text.lower()

    for category, data in FAQ_DATABASE.items():
        for keyword in data["keywords"]:
            kw = keyword.lower()
            # Use word boundary matching to prevent false positives
            if re.search(r'\b' + re.escape(kw) + r'\b', lower_text):
                return {"category": category, "response": data["response"]}

    return None

def should_forward_to_human(text):
    """Check if question should be forwarded to admin"""
    lower_text = text.lower()
    return any(trigger in lower_text for trigger in FORWARD_TRIGGERS)

def escape_markdown(text):
    """Escape markdown special characters in user-generated text"""
    special_chars = r"_*[]()"
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text

def get_conversational_fallback(user_name):
    """Friendly fallback when no FAQ match"""
    fallbacks = [
        "hmm that's a good one 🤔",
        "tbh i don't have that answer yet!",
        "oh interesting question! let me think...",
    ]
    
    return random.choice(fallbacks) + """

but i CAN help with:
• charging & battery 🔋
• app download & setup 📱
• device activation 🔗
• recording features 🎙️
• sync & transfer 🔄
• transcription 📝
• AI chat 🤖
• shipping 📦
• returns & warranty 🔄
• packages & pricing 💰
• commissions & bonuses 💸

or check the full FAQ: {faq_link}

need human help? @{admin_username} can assist! 😇
""".format(faq_link=FAQ_LINK, admin_username=ADMIN_USERNAME)

# ============================================
# Bot Handlers
# ============================================

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    """Handle /start and /help commands in DMs or groups"""
    response = """hey! i'm Vanessa, ur MMEETT guide 😇

i can help with:
• charging & battery 🔋
• app download & setup 📱
• device activation 🔗
• recording features 🎙️
• sync & transfer 🔄
• transcription 📝
• AI chat 🤖
• shipping 📦
• returns & warranty 🔄
• packages & pricing 💰
• commissions & bonuses 💸

just ask ur question in the FAQ tab!
or check the full FAQ: {faq_link}

need human help? @{admin_username} can assist!
""".format(faq_link=FAQ_LINK, admin_username=ADMIN_USERNAME)

    try:
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        print(f"❌ Error sending /start response: {e}")

@bot.message_handler(content_types=["new_chat_members"])
def handle_new_member(message):
    """Handle new members joining the group"""
    chat_id = message.chat.id
    topic_id = get_topic_id(message)
    
    # Only welcome in General Chat (Topic 5)
    if topic_id != GENERAL_CHAT_ID:
        print(f"⚠️ New member in wrong topic ({topic_id}), skipping welcome")
        return
    
    for new_user in message.new_chat_members:
        # Skip if the new member is a bot
        if new_user.is_bot:
            print(f"⚠️ Bot joined: {new_user.first_name}")
            continue
        
        # Get user name
        user_name = new_user.first_name
        if new_user.username:
            user_name = f"@{new_user.username}"
        else:
            user_name = new_user.first_name
        
        print(f"👋 New member joined: {user_name}")
        
        # Send welcome message
        send_welcome_message(chat_id, topic_id, user_name)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all incoming messages"""
    
    # Ignore messages from bots (including ourselves)
    if message.from_user.is_bot:
        return
    
    # Ignore messages without text
    if not message.text:
        return
    
    # Get topic ID
    topic_id = get_topic_id(message)
    if topic_id is None:
        print("⚠️ Message not in a topic, ignoring")
        return
    
    # Get user info
    text = message.text
    from_user = message.from_user.first_name
    if message.from_user.username:
        from_user = f"@{message.from_user.username}"
    
    print(f"📨 Message in Topic {topic_id} from {from_user}: {text[:50]}...")
    
    # ============================================
    # RULE: Only reply in FAQ topic (Topic 9)
    # ============================================
    if topic_id != FAQ_ID:
        # Not in FAQ tab - stay silent (no guidance messages)
        return
    
    # We're in FAQ tab - process the question
    
    # Check if question should be forwarded to human
    if should_forward_to_human(text):
        print("⚠️ Forwarding to admin...")
        
        forward_message = f"""⚠️ this needs human help

👤 from: {escape_markdown(from_user)}
❓ question: "{escape_markdown(text)}"

tagging @{ADMIN_USERNAME} for assistance...

────────────
💡 tip: full FAQ here:
{FAQ_LINK}"""
        
        try:
            bot.reply_to(message, forward_message, parse_mode="Markdown")
            print(f"📩 Notified @{ADMIN_USERNAME}")
        except Exception as e:
            print(f"❌ Error sending forward message: {e}")
        
        return
    
    # Check if question matches FAQ
    match = match_question(text)
    
    if match:
        print(f"✅ FAQ match: {match['category']}")
        try:
            bot.reply_to(message, match["response"], parse_mode="Markdown")
            print("✅ Response sent")
        except Exception as e:
            print(f"❌ Error sending FAQ response: {e}")
        return
    
    # No match - use conversational fallback
    print("ℹ️ No FAQ match, using conversational fallback")
    fallback = get_conversational_fallback(from_user)
    
    try:
        bot.reply_to(message, fallback, parse_mode="Markdown")
        print("✅ Fallback response sent")
    except Exception as e:
        print(f"❌ Error sending fallback: {e}")

# ============================================
# Main
# ============================================

if __name__ == "__main__":
    print("✅ Vanessa is running. Press Ctrl+C to stop.")
    bot.remove_webhook()
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f"❌ Polling error: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            import time
            time.sleep(5)

