#!/usr/bin/env python3
"""
Vanessa - MMEETT FAQ Guide
Telegram Auto-Responder with Human Customer Service Personality
Topic-aware: Welcomes in General Chat, Answers in FAQ
"""

import os
import re
import time
import random
import telebot
from telebot import types

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
# PERSONALITY SYSTEM
# ============================================

CONVERSATIONAL_OPENERS = [
    "oh good question!",
    "let me check...",
    "sure thing!",
    "ah yeah,",
    "ok so,",
    "nice one!",
    "right,",
    "hmm okay,",
    "alright,",
    "oh for sure,",
    "great question!",
    "yup!",
    "of course,",
    "yeah so,",
]

CONVERSATIONAL_CLOSERS = [
    "anything else?",
    "hope that helps!",
    "lemme know if u need more details",
    "hope that makes sense!",
    "any other questions?",
    "holler if u need anything else!",
    "that help?",
    "let me know if u're still unsure",
    "feel free to ask more!",
    "hope that clears things up!",
]

TIME_GREETINGS = {
    "morning": ["morning!", "good morning!", "mornin'!"],
    "afternoon": ["hey!", "afternoon!", "hey there!"],
    "evening": ["hey!", "evening!", "hey there!"],
    "night": ["hey!", "still up? 😄", "burning the midnight oil? 😄"],
}

SMALL_TALK = {
    "greetings": {
        "triggers": ["hi", "hello", "hey", "sup", "yo", "hola", "what's up", "whats up", "morning", "evening", "afternoon"],
        "responses": [
            "hey! what's up? 😊",
            "hello! how can i help?",
            "hey there! what do u need?",
            "hi! what can i do for u?",
            "heyyy! got a question?",
            "yo! what's on ur mind?",
        ],
    },
    "thanks": {
        "triggers": ["thanks", "thx", "thank you", "ty", "tysm", "thanks!", "thank u"],
        "responses": [
            "no worries!",
            "anytime!",
            "that's what i'm here for!",
            "no prob! anything else?",
            "glad i could help!",
            "u're welcome!",
            "of course!",
        ],
    },
    "how_are_you": {
        "triggers": ["how are u", "how r u", "how's it going", "hows it going", "how are you", "how u doing", "how u doin", "u good", "u okay"],
        "responses": [
            "i'm good! thanks for asking 😊 what do u need help with?",
            "doing great! ready to help u out",
            "all good here! what's on ur mind?",
            "living the dream! 😇 what can i help u with?",
        ],
    },
    "confirm": {
        "triggers": ["ok", "okay", "got it", "makes sense", "nice", "cool", "awesome", "great", "sweet", "alright"],
        "responses": [
            "👍",
            "nice!",
            "cool cool",
            "awesome!",
            "great!",
            "😎",
        ],
    },
}

EMPATHY_PHRASES = [
    "i hear u",
    "that sounds frustrating",
    "i understand how u feel",
    "that's really not ideal, i'm sorry",
    "i get it, let me get someone who can help",
]

# ============================================
# INVITE MESSAGES (for sharing MMEETT with friends)
# ============================================

INVITE_MESSAGES = [
    """hey! 👋 i've been using MMEETT and it's honestly been really cool — it's a smart device that records meetings, transcribes, and even has AI chat built in.

if u're curious, check it out and let me know what u think! 🚀""",

    """so i recently joined MMEETT X 1% Club and it's been pretty awesome 😇

the device does meeting recordings, live transcription, AI chat... and the community is super supportive.

wanna check it out? i can help u get started! ⚡️""",

    """ok so this MMEETT thing is actually legit 😅

it records meetings, transcribes in multiple languages, has AI chat (GPT, Gemini, DeepSeek), and NFC card sharing.

i've been using it and honestly it's worth it. let me know if u want more info! 💎""",

    """hey! just wanted to share something i've been using — MMEETT.

it's a smart meeting device that:
🎙️ records meetings (live & phone calls)
📝 transcribes in multiple languages
🤖 has AI chat (GPT, Gemini, DeepSeek)
💳 NFC card for networking

if it sounds like ur thing, i can point u in the right direction! 🔗""",

    """yo! so i found this thing called MMEETT and honestly? game changer.

meeting recordings, auto-transcription, AI assistant, NFC business card... all in one device.

the community is great too. wanna know more? just ask! 🚀""",

    """psst 👀 i've been using this MMEETT device and it's lowkey amazing.

records my meetings, auto-transcribes everything, and the AI chat is actually useful for work stuff.

if u wanna try it out, lmk! happy to help u get set up 😇""",

    """hey! 👋 remember when i was looking for a good meeting recorder? found one — MMEETT.

it records, transcribes, has AI chat, and even lets u share contact info with NFC.

seriously worth checking out. i'll send u details if u want! 💪""",

    """so i don't usually recommend stuff but MMEETT is different.

🎙️ meeting recordings (standalone, no phone needed)
📝 auto-transcription in multiple languages
🤖 built-in AI chat (GPT, Gemini, DeepSeek)
💳 NFC smart card for networking

the community is super helpful too. ask me anything! ⚡️""",

    """hey! 👋 quick question — do u ever struggle with taking meeting notes?

because i found this thing called MMEETT that literally does it for u. records, transcribes, and even has AI to answer questions about ur meetings.

i've been using it for a bit and it's been a game changer. wanna know more? 🎙️""",

    """ok real talk — MMEETT has made my meetings so much better 😇

no more scrambling to take notes. it records everything, transcribes automatically, and the AI chat helps me follow up on action items.

plus the NFC card is a flex at networking events 💳

if u're curious, i can tell u more about it! 🚀""",
]

INVITE_TRIGGERS = [
    "invite", "invite message", "invite friends", "share", "share message",
    "recruit", "recruit message", "bring friends", "invite link", "referral message",
    "how to invite", "want to invite", "wanna invite", "send invite",
]

# ============================================
# WELCOME MESSAGES (3 variants)
# ============================================

WELCOME_MESSAGES = [
    lambda name: f"""
hey {name}, welcome to MMEETT X 1% Club! ⚡️

really glad to have u here!

so u don't feel lost, here's what each tab is for:

☕️ General Chat — hang out, introduce urself, connect with other members

📢 Announcement — company updates, zoom call links, official news

📂 The Vault — PDF resources organised by language (CN, EN, VI, TH, ID, TL)

🎬 Resources — video format resources and training materials

🛠 Learn & Master MMEETT — step-by-step tutorials (videos + guides)

❓ Frequently Asked Questions — got a question? ask here! i'll answer ASAP

🌐 i speak 9 languages! English, 中文, Bahasa Melayu, Bahasa Indonesia, ไทย, Tiếng Việt, Tagalog, 日本語, and 한국어 — feel free to ask in whatever language u're most comfortable with!

💡 first steps if u're new:
1. check the Tutorial tab for a video on how to purchase ur MMEETT package
2. have questions? drop them in the FAQ tab — i'm there to help!
3. want to invite friends? type "invite" in the FAQ tab and i'll craft a friendly message for u!

let's redefine how the world connects. 🚀

seriously though, if u need anything just holler! 😇
""",
    lambda name: f"""
{name}!! welcome to MMEETT X 1% Club! 🎉

so happy u joined! here's a quick guide so u don't get lost:

☕️ General Chat — come say hi, meet other members
📢 Announcement — stay updated with official news & zoom links
📂 The Vault — PDFs in CN, EN, VI, TH, ID, TL
🎬 Resources — video resources & training materials
🛠 Learn & Master MMEETT — tutorials & video guides
❓ FAQ — that's where i live! ask me anything 😇

🌐 fun fact: i can chat in 9 languages! English, 中文, Bahasa Melayu, Bahasa Indonesia, ไทย, Tiếng Việt, Tagalog, 日本語, 한국어 — just ask in ur language and i'll do my best!

🚀 new here? do this first:
1. watch the tutorial on buying ur MMEETT package
2. drop any question in the FAQ tab, i'll be there
3. wanna invite friends? type "invite" in the FAQ tab and i'll hook u up!

welcome aboard! let's make moves 💪
""",
    lambda name: f"""
hey hey {name}! ⚡️ welcome to the 1% Club!

u're gonna love it here. quick orientation:

☕️ General Chat — chill zone, introduce urself!
📢 Announcement — official stuff, zoom calls
📂 The Vault — PDFs sorted by language (CN, EN, VI, TH, ID, TL)
🎬 Resources — videos & training content
🛠 Learn & Master MMEETT — ur step-by-step guide
❓ FAQ — this is my zone! ask away 😇

🌐 psst — i speak 9 languages! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — ask me anything in ur language!

✨ newbie checklist:
1. Tutorial tab → watch how to get ur MMEETT package
2. FAQ tab → ask me anything, i'm always there
3. wanna bring friends in? type "invite" in the FAQ tab and i'll write u a message!

glad u're here! holler if u need anything 🚀
""",
]

# ============================================
# FAQ DATABASE - 3 variants per category
# ============================================

FAQ_DATABASE = {
    "PACKAGES": {
        "keywords": ["package", "packages", "tier", "tiers", "membership", "price", "prices", "pricing", "cost", "how much", "silver", "gold", "platinum", "diamond"],
        "responses": [
            """oh u wanna know about packages? we got 4 tiers:

🥈 **Silver** $200 USD (120 PV)
   Gratitude Bonus: 1.5x return (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Gratitude Bonus: 2x return (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Gratitude Bonus: 2.5x return (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Gratitude Bonus: 3x return (cap $16,200)

higher tier = bigger bonuses! which one catches ur eye?""",
            """here's the breakdown, we have 4 options:

🥈 **Silver** — $200 USD (120 PV) → 1.5x Gratitude Bonus (cap $300)
🥇 **Gold** — $600 USD (360 PV) → 2x Gratitude Bonus (cap $1,200)
💎 **Platinum** — $1,800 USD (1,080 PV) → 2.5x Gratitude Bonus (cap $4,500)
💎💎 **Diamond** — $5,400 USD (3,240 PV) → 3x Gratitude Bonus (cap $16,200)

basically the higher u go, the more u get back. u thinking about which one?""",
            """so we got 4 membership tiers lah:

$200 = 🥈 **Silver** (120 PV, 1.5x bonus, cap $300)
$600 = 🥇 **Gold** (360 PV, 2x bonus, cap $1,200)
$1,800 = 💎 **Platinum** (1,080 PV, 2.5x bonus, cap $4,500)
$5,400 = 💎💎 **Diamond** (3,240 PV, 3x bonus, cap $16,200)

diamond is the big one obviously 😅 wanna know more about a specific tier?""",
        ],
    },
    "COMMISSION": {
        "keywords": ["commission", "earn", "earning", "money", "income", "bonus", "bonuses", "award", "awards", "payout", "roi"],
        "responses": [
            """ok so there's 7+2 bonus systems haha:

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

more u build, more u earn lah! want me break down any specific one?""",
            """the earning system is pretty stacked tbh! here's all the ways u earn:

1. 💰 **Recommendation Award** — 10% when u directly refer someone
2. 🏗 **Placement Award** — 0.3% per floor, up to 20 floors
3. 🌐 **Sharing Award** — 0.4% across 20 generations
4. 📊 **Tier Bonus** — 20% to 40% depending on ur tier
5. ⭐️ **Team Grade Difference Bonus**
6. 🎯 **Grade Difference Equal Prize** — flat 5%
7. 🌍 **Global Dividend Award** — 6% pool for top stars
8. ✈️ **Travel Points** — grows 10% daily
9. 🙏 **Gratitude Bonus** — up to 3x ur package

yeah it's a lot 😂 which one u wanna know more about?""",
            """alright so MMEETT has 9 income streams:

direct income:
💰 **Recommendation** 10% | 🏗 **Placement** 0.3%/floor (20 floors) | 🌐 **Sharing** 0.4%/gen (20 gens)

tier-based:
📊 **Tier Bonus** 20-40% (Silver→Diamond)

team-based:
⭐️ **Grade Difference** | 🎯 **Equal Prize** 5%

passive:
🌍 **Global Dividend** 6% | ✈️ **Travel Points** +10%/day | 🙏 **Gratitude Bonus** up to 3x

the system rewards u for building, basically. anything specific u want me to explain?""",
        ],
    },
    "RANKING": {
        "keywords": ["rank", "ranking", "star", "stars", "level", "explorer", "visionary", "upgrade", "promote"],
        "responses": [
            """we got 10 star levels one:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

each level = higher bonus percentage

requirements start from 10,000 PV and go up to millions depending on level

u're at what level now? can help u figure out what's next!""",
            """the ranking system goes from 1 star to 10 stars:

1⭐ Explorer → 4% | 2⭐ Advocate → 6% | 3⭐ Influencer → 8%
...all the way to...
10⭐ Visionary Board → 20%

each star level unlocks a higher bonus %. u start at 10,000 PV and it scales up from there.

what star level are u currently? i can tell u what u need for the next one!""",
            """so the star system is how u level up in MMEETT:

low levels: ⭐️ Explorer (4%) → ⭐️⭐️ Advocate (6%) → ⭐️⭐️⭐️ Influencer (8%)
high levels: ... → ⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ Visionary Board (20%)

more stars = bigger bonus cuts. PV requirements go from 10k up to millions.

where are u at right now? maybe i can help u plan ur next move 😇""",
        ],
    },
    "CHARGING": {
        "keywords": ["charge", "charging", "battery", "power", "green light", "red light", "low battery", "50 hours", "full charge"],
        "responses": [
            """super easy one:

1️⃣ plug cable to MMEETT port
2️⃣ use 5V/0.5A adapter (DC-5V)
3️⃣ charge until light turn green

⏱️ battery = 50 hours total
💤 auto sleep after 10 min no activity

done 🔋""",
            """charging is straightforward:

just plug into the MMEETT port with a 5V/0.5A adapter, wait for the green light, and ur good!

battery lasts about 50 hours, and it auto-sleeps after 10 minutes of not being used.

pretty simple right? 🔋""",
            """ok for charging:

→ use the MMEETT charging port
→ 5V/0.5A DC adapter (the small one, not fast charge!)
→ green light = fully charged

u get around 50 hours of battery life, and it sleeps on its own after 10 min idle.

need anything else? 🔋""",
        ],
    },
    "APP_DOWNLOAD": {
        "keywords": ["download", "app", "install", "application", "app store", "google play", "register", "sign up", "verification code"],
        "responses": [
            """app store or google play lah:

📲 **iOS**: App Store → search "MMEETT"
🤖 **Android**: Google Play → search "MMEETT"

after install:
• turn on bluetooth
• turn on NFC (for card writing)
• need Android 6+ or iOS 12+

if no verification code = check spam folder 😅

need help setting up? tag @ukkbasf leh""",
            """to get the app:

📱 iPhone → App Store, search MMEETT
🤖 Android → Google Play, search MMEETT

once downloaded:
- bluetooth ON
- NFC ON (for writing cards)
- minimum: Android 6 or iOS 12

verification code not coming through? check ur spam/junk folder first 😅

still stuck? @ukkbasf can help!""",
            """getting the app is easy peasy:

just search "MMEETT" in:
📲 App Store (iPhone) or 🤖 Google Play (Android)

then make sure:
• bluetooth is turned on
• NFC is enabled
• ur phone is Android 6+ or iOS 12+

oh and if the verification code doesn't show up → check spam folder!

anything else u need?""",
        ],
    },
    "ACTIVATION": {
        "keywords": ["activate", "bind", "connect", "pair", "nfc", "card", "write", "link", "device", "trans"],
        "responses": [
            """ok here's how:

1️⃣ hold TRANS 1 sec (blue light = on)
2️⃣ white light flashes = ready to bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ place near phone (iPhone: top back)

to write card link:
• "Me" → "Activate MMEETT Device"
• select card → "Activate"
• phone NFC must be ON

got stuck? tag me leh 😇""",
            """activating ur device:

1. hold the TRANS button for 1 sec → blue light comes on
2. wait for white light flashing = ready
3. in the app tap "Bind Device" (under "Not Connected")
4. put device near ur phone (iPhone users: top back of phone)

for card writing: Me → Activate MMEETT Device → pick card → Activate
(make sure NFC is on!)

anything tripping u up?""",
            """to bind ur MMEETT device:

step 1: hold TRANS 1 second until u see blue light
step 2: white flashing = pairing mode activated
step 3: on the app, go to "Bind Device"
step 4: hold device near phone to connect

for card activation: Me tab → Activate MMEETT Device → choose ur card → Activate (NFC needs to be on!)

pretty smooth process once u get the hang of it 😇""",
        ],
    },
    "RECORDING": {
        "keywords": ["record", "recording", "meeting", "call", "audio", "microphone", "start", "stop", "pause", "red light", "yellow light"],
        "responses": [
            """🎙️ **LIVE MODE** (no phone needed):
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

got it? 😇""",
            """for recording:

**live/in-person mode** → hold TRANS 1s, switch MEETING up, wait for vibration + red light. no phone needed!

**phone call mode** → same start, then double-press TRANS within 0.5s. yellow light = recording call.

heads up: call mode needs the device touching the phone, and there's no pause — stopping creates a new file.

need me to walk through it again?""",
            """there's 2 recording modes:

🔴 Live mode: TRANS 1s → MEETING up → red light + vibration = u're recording (standalone, no phone)

🟡 Call mode: TRANS 1s → MEETING up → double-press TRANS (0.5s gap) → yellow light = recording call

things to note:
- call mode = device on phone, no headphones
- no pause button (stop and restart = new recording file)

makes sense?""",
        ],
    },
    "SYNC": {
        "keywords": ["sync", "transfer", "upload", "download", "wifi", "bluetooth", "file", "empty folder", "computer"],
        "responses": [
            """🔄 **Sync Recordings**:

1. connect device to app (Bluetooth)
2. app shows: "Files pending sync"
3. choose: Sync all OR select files
4. files auto-delete after sync

⚡️ transfer speeds:
• Bluetooth = ~tens of KB/sec (slow)
• WiFi = much faster (recommended)

📂 folder empty on computer? files auto-deleted after sync. export from app instead.

make sense ah? 😇""",
            """to sync ur recordings:

open the app → connect via Bluetooth → it'll show "Files pending sync" → choose sync all or pick specific ones

once synced, files are automatically removed from the device.

speed tip: WiFi is way faster than Bluetooth for transfers!

if ur computer folder looks empty after sync, that's normal — files get cleared. just export from the app instead.

anything else?""",
            """syncing works like this:

1. make sure device is connected to app over bluetooth
2. app will show pending files
3. sync all at once or pick individual files
4. done! files clear from device after sync

⚡️ pro tip: use WiFi sync if u can, bluetooth is pretty slow for large files

oh and if u're looking for files on ur computer — they auto-delete from device after sync, so export from the app directly.

need more help with this?""",
        ],
    },
    "TRANSCRIPTION": {
        "keywords": ["transcribe", "transcript", "text", "convert", "write", "summary", "language", "translate"],
        "responses": [
            """📝 **Transcription**:

⏱️ time = ~50% of recording length
example: 1-hour recording = ~30 min

🌍 multi-language (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

pretty fast one! 😇""",
            """for transcription:

it takes about half the length of the recording. so a 1-hour meeting = roughly 30 min to transcribe.

and it supports multiple languages automatically — English, Chinese, Japanese, Thai, Korean and more!

pretty neat right?""",
            """transcription is automatic:

⏱️ processing time ≈ 50% of recording duration (1hr meeting → ~30min)
🌍 language auto-detection: English, 中文, 日本語, ไทย, 한국어 etc

no manual work needed, just hit transcribe and wait 😇""",
        ],
    },
    "AI_CHAT": {
        "keywords": ["ai", "chat", "bot", "model", "gpt", "gemini", "deepseek", "search", "think mode", "mr mmeett"],
        "responses": [
            """🤖 **AI Chat Feature**:

1. go to "AI Chat" tab in app
2. chat with Mr. MMEETT agent
3. switch models: GPT, Gemini, DeepSeek
4. enable "Web Search" for real-time info
5. enable "Think Mode" for complex questions

💡 Think Mode = shows AI reasoning (DeepSeek/Gemini only)

want to try? 😇""",
            """the AI chat is built right into the app!

→ open the "AI Chat" tab
→ u can talk to Mr. MMEETT
→ switch between GPT, Gemini, or DeepSeek models
→ turn on Web Search for live info
→ Think Mode shows the AI's reasoning (DeepSeek/Gemini only)

it's pretty cool actually, give it a spin!""",
            """oh yeah the AI feature! here's how:

just go to AI Chat in the app and start talking to Mr. MMEETT. u can pick from GPT, Gemini, or DeepSeek.

bonus features:
- Web Search → for real-time information
- Think Mode → see how the AI reasons (works with DeepSeek & Gemini)

worth trying out for sure 🤖""",
        ],
    },
    "SHIPPING": {
        "keywords": ["shipping", "delivery", "track", "order", "when arrive", "processing", "how long", "dispatch"],
        "responses": [
            """📦 **Shipping & Delivery**:

📦 processing: 3-5 business days
🚚 delivery: 6-15 business days

📍 track order:
App → "Me" → "Member" → "Orders"

🌍 worldwide shipping available

anything else ah? 😇""",
            """for shipping:

processing takes 3-5 business days, then delivery is another 6-15 business days depending on where u are.

to track: open the app → Me → Member → Orders

and yeah, they ship worldwide! 🌍

need anything else?""",
            """shipping info:

⏳ 3-5 business days to process
🚚 6-15 business days to deliver
🌍 ships globally

tracking is in the app: Me → Member → Orders

pretty standard turnaround! anything else?""",
        ],
    },
    "RETURNS": {
        "keywords": ["return", "refund", "exchange", "warranty", "repair", "broken", "20 day", "12 month", "defective"],
        "responses": [
            """🔄 **Returns & Warranty**:

🔄 returns: 20 days from purchase
• MMEETT Card, Membership, Computing power

🔧 warranty: 12 months from purchase
• free repairs during warranty
• need: serial number + proof of purchase

📞 contact: App → "Me" → "Customer Service"

got issues? tag @ukkbasf leh 😇""",
            """returns and warranty:

u got 20 days from purchase to return MMEETT Card, Membership, or Computing power.

warranty covers 12 months — free repairs if something goes wrong. just make sure u have ur serial number and proof of purchase.

to start: App → Me → Customer Service

having a specific issue? i can tag @ukkbasf for u""",
            """here's the policy:

return window: 20 days from purchase date
warranty: 12 months from purchase date

for returns: MMEETT Card, Membership, Computing power are eligible
for warranty repairs: need serial number + receipt/proof

reach out through the app: Me → Customer Service

or tag @ukkbasf if u need faster help!""",
        ],
    },
    "TRAVEL_POINTS": {
        "keywords": ["travel", "point", "points", "trip", "vacation", "bonus increase", "daily"],
        "responses": [
            """✈️ **Travel Points**:

daily 10% bonus increase one!

basically = every day ur bonus pool grows by 10%

use for:
• company trips
• events
• or convert to cash (depends on level)

pretty nice ah? 😇""",
            """travel points are pretty sweet:

ur bonus pool increases by 10% every single day. it compounds!

u can use them for company trips, events, or even convert to cash (depending on ur level).

it's like passive income on top of passive income 😅""",
            """so travel points work like this:

every day, ur points get a 10% bonus increase. so it keeps growing!

u can redeem for:
- company trips & events
- cash conversion (level-dependent)

one of my favorite features tbh ✈️""",
        ],
    },
    "GRADE_DIFFERENCE": {
        "keywords": ["grade difference", "equal prize", "team grade", "5 percent", "5%"],
        "responses": [
            """🎯 **Grade Difference Bonuses**:

**Team Grade Difference**:
earn from difference between ur level and ur team's level

**Grade Difference Equal Prize** = 5%
when u and ur referral same level, u still earn 5%

so even if u're same rank, still can earn! 😇

confusing ah? can explain more if u want!""",
            """ok the grade difference stuff:

**Team Grade Difference** — u earn based on the gap between ur rank and ur team's rank. bigger gap = more earnings.

**Grade Difference Equal Prize** — even if u and ur referral are the same level, u still get 5%. so nobody gets left out.

it's designed so u always earn something, regardless of rank differences!""",
            """grade difference bonuses:

1. Team Grade Difference → profit from the rank gap between u and ur downline. higher rank = more u earn from the difference.

2. Equal Prize → if u and ur referral are the same level, u still get a flat 5%.

the idea is: u always earn, whether there's a rank gap or not 😇

want me to go deeper on this?""",
        ],
    },
    "GLOBAL_DIVIDEND": {
        "keywords": ["global", "dividend", "6 percent", "6%", "star", "5 star", "10 star"],
        "responses": [
            """🌍 **Global Dividend Award**:

6% of global pool shared among 5-10 star members

requirements:
• reach 5-star level minimum
• maintain performance

this is the big one lah — passive income from entire company growth! 😇

u're aiming for what level?""",
            """the global dividend is the big one:

6% of the entire company's global pool gets distributed to members who reach 5 stars and above.

requirements: hit at least 5-star level and keep ur performance up.

it's basically passive income from the whole company growing — pretty powerful if u can get there!""",
            """global dividend = the passive income dream:

→ 6% of global revenue pool
→ shared among 5-10 star members
→ need minimum 5 stars + consistent performance

this is where the real passive money is. the higher ur stars, the bigger ur slice of the pie.

u working towards 5 stars?""",
        ],
    },
    "FAVORITE_COLOR": {
        "keywords": ["favourite color", "favorite color", "favourite colour", "favorite colour", "color", "colour", "fav color"],
        "responses": [
            """green for the colour of money lol 🤑🤑

(but seriously, MMEETT green like charging light one 🔋)""",
            """green all the way! 💚

money green, MMEETT green, charging light green... coincidence? i think not 😂🔋""",
            """lol green obviously! 🟢

it's the colour of growth, money, AND the MMEETT charging light. triple threat! 🤑""",
        ],
    },
    "DEVICE_SETUP": {
        "keywords": ["device", "setup", "configure", "configuration", "initial", "first time", "unbox", "unpack"],
        "responses": [
            """**Device Setup**:

1️⃣ unbox ur MMEETT device
2️⃣ charge it first (5V/0.5A adapter)
3️⃣ download MMEETT app
4️⃣ enable bluetooth + NFC on phone
5️⃣ bind device in app

ready to go! 🔋""",
            """setting up ur device is easy:

unbox → charge fully → download app → turn on bluetooth & NFC → bind device in app

that's it! u're ready to use MMEETT 😇""",
            """first time setup:

charge the device first (green light = full)
then download MMEETT app from app store/play store
enable bluetooth and NFC
go to "Bind Device" in the app

done! 🎉""",
        ],
    },
    "CONNECTIVITY": {
        "keywords": ["bluetooth", "wifi", "connection", "connect", "disconnect", "pairing", "range", "signal"],
        "responses": [
            """**Connectivity**:

📶 **Bluetooth**: 5.0+ (range: ~10m)
📶 **WiFi**: 2.4GHz support for fast sync

💡 tips:
• keep device close to phone during pairing
• turn off other bluetooth devices if having issues
• restart bluetooth if connection drops

having trouble? tag @ukkbasf 😇""",
            """for connectivity:

bluetooth 5.0+ connects up to ~10 meters
wifi is 2.4GHz only (not 5GHz) for sync

if connection is weak:
- move closer to phone
- turn off other bluetooth devices nearby
- try turning bluetooth off/on

still issues? @ukkbasf can help!""",
            """connection specs:

bluetooth: 5.0+, range about 10m
wifi: 2.4GHz for fast file transfers

troubleshooting:
→ keep device near phone when pairing
→ disable other bluetooth devices
→ restart bluetooth if it acts up

anything specific u're facing?""",
        ],
    },
    "NFC_CARDS": {
        "keywords": ["nfc", "card", "cards", "write", "tap", "scan", "contactless", "rfid"],
        "responses": [
            """**NFC Cards**:

💳 MMEETT uses NFC cards for activation
📱 phone NFC must be ON to write cards

how to use:
1. Me → Activate MMEETT Device
2. select card type
3. tap card to back of phone (top for iPhone)
4. wait for confirmation

⚠️ keep cards away from magnets!""",
            """NFC cards are how u activate ur device:

make sure phone NFC is turned on
go to Me → Activate MMEETT Device
pick ur card type
tap the card to the back of ur phone

for iPhone: top back area is the NFC spot
Android: usually middle or top back

easy! 💳""",
            """using NFC cards:

1. enable NFC in phone settings
2. in app: Me → Activate MMEETT Device
3. choose card
4. hold card against phone's NFC area

iPhone = top back
Android = varies (check phone manual)

cards are sensitive to magnets, so keep them safe! 💳""",
        ],
    },
    "COMPATIBILITY": {
        "keywords": ["compatible", "compatibility", "support", "works", "phone", "model", "ios", "android", "version"],
        "responses": [
            """**Phone Compatibility**:

📱 **iOS**: 12.0+ (iPhone 6s and newer)
🤖 **Android**: 6.0+ (with NFC support)

💡 recommended:
• iOS 15+ for best performance
• Android 10+ with NFC

check ur phone settings for NFC!""",
            """ur phone needs to be:

iPhone: iOS 12 or later (iPhone 6s+)
Android: 6.0+ with NFC built-in

for the best experience:
- iOS 15+ recommended
- Android 10+ recommended

most modern phones work fine! 😇""",
            """compatibility requirements:

minimum: iOS 12 / Android 6
must have: NFC hardware

recommended: iOS 15+ / Android 10+

if ur phone is from the last 5 years, it should work! check settings for NFC support.""",
        ],
    },
    "PRIVACY": {
        "keywords": ["privacy", "private", "secure", "security", "data", "encryption", "safe", "protect"],
        "responses": [
            """**Privacy & Security**:

🔒 recordings stored locally on device
🔒 sync uses encrypted connection
🔒 no cloud storage unless u choose to

MMEETT prioritizes ur data privacy!

💡 tip: delete recordings after sync if sensitive""",
            """privacy features:

all recordings stay on ur device until u sync
sync is encrypted end-to-end
no automatic cloud backup

ur data = ur control 🔒

want extra security? delete files after syncing!""",
            """data security:

→ local storage on device (no auto-cloud)
→ encrypted sync to phone
→ u control what gets backed up

MMEETT is designed with privacy in mind 🔒

for sensitive meetings, delete after sync!""",
        ],
    },
    "TROUBLESHOOTING": {
        "keywords": ["troubleshoot", "troubleshooting", "issue", "issues", "fix", "solve", "problem", "not working", "help"],
        "responses": [
            """**Quick Troubleshooting**:

🔋 device won't turn on? → charge fully first
📱 can't connect? → restart bluetooth on phone
🔄 sync failing? → use WiFi instead of bluetooth
🎙️ no recording? → check MEETING switch position
💳 NFC not working? → enable in phone settings

still stuck? tag @ukkbasf! 😇""",
            """common fixes:

device dead? → charge with 5V/0.5A adapter
connection issues? → turn bluetooth off/on
sync slow? → switch to WiFi sync
recording not starting? → hold TRANS 1s, switch MEETING up
NFC fail? → check phone settings

@ukkbasf can help if these don't work!""",
            """troubleshooting checklist:

✓ charge device fully
✓ restart phone's bluetooth
✓ use WiFi for faster sync
✓ check MEETING switch is up for recording
✓ enable NFC in phone settings

if none of these help, tag @ukkbasf for support!""",
        ],
    },
    "SUBSCRIPTION": {
        "keywords": ["subscription", "subscribe", "monthly", "yearly", "recurring", "renew", "renewal", "cancel"],
        "responses": [
            """**Subscription Info**:

💳 one-time purchase (no monthly fees!)
🎉 MMEETT device = buy once, own forever

optional:
• computing power packages (recurring)
• premium AI features (if available)

no hidden subscriptions! 😇""",
            """good news: no mandatory subscriptions!

ur MMEETT device is a one-time purchase. u own it forever.

optional recurring:
- computing power packages
- any future premium features

that's it! no surprise monthly charges 💳""",
            """subscription model:

device purchase = one time, no recurring fees
membership = one time activation

optional recurring:
→ computing power
→ premium AI (if u choose)

MMEETT keeps it simple — no hidden subs! 😇""",
        ],
    },
    "AFFILIATE_TRACKING": {
        "keywords": ["affiliate", "tracking", "referral", "link", "downline", "team", "network", "recruit"],
        "responses": [
            """**Affiliate Tracking**:

🔗 unique referral link in app
📊 real-time dashboard:
   • direct referrals
   • team structure
   • earnings breakdown

💡 share ur link = auto tracking!

check: Me → Member → My Team""",
            """affiliate tracking is automatic:

ur referral link is in the app (Me section)
when someone signs up with ur link:
→ they're added to ur downline
→ u earn Recommendation Award (10%)
→ u track everything in real-time

dashboard: Me → Member → My Team

easy! 🔗""",
            """tracking ur referrals:

each person gets a unique link
share it → people join → auto tracking

dashboard shows:
- who u directly referred
- ur full team structure (20 floors)
- all earnings from each level

find it: Me → Member → My Team

build ur network! 🚀""",
        ],
    },
}

# ============================================
# MULTI-LANGUAGE FAQ TRANSLATIONS
# ============================================

FAQ_TRANSLATIONS = {
    "PACKAGES": {
        "zh": """哦想知道套餐？我们有 4 个等级：

🥈 **Silver** $200 USD (120 PV)
   感恩奖金：1.5 倍回报（上限$300）

🥇 **Gold** $600 USD (360 PV)
   感恩奖金：2 倍回报（上限$1,200）

💎 **Platinum** $1,800 USD (1,080 PV)
   感恩奖金：2.5 倍回报（上限$4,500）

💎💎 **Diamond** $5,400 USD (3,240 PV)
   感恩奖金：3 倍回报（上限$16,200）

等级越高=奖金越多！你对哪个感兴趣？""",
        "ms": """oh nak tahu pasal pakej? kita ada 4 tier:

🥈 **Silver** $200 USD (120 PV)
   Bonus Gratitude: 1.5x return (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Bonus Gratitude: 2x return (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Bonus Gratitude: 2.5x return (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Bonus Gratitude: 3x return (cap $16,200)

tier lagi tinggi = bonus lagi besar! mana satu kau minat?""",
        "id": """oh mau tahu paket? kita punya 4 tier:

🥈 **Silver** $200 USD (120 PV)
   Bonus Gratitude: 1.5x return (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Bonus Gratitude: 2x return (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Bonus Gratitude: 2.5x return (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Bonus Gratitude: 3x return (cap $16,200)

tier lebih tinggi = bonus lebih besar! kamu tertarik yang mana?""",
        "th": """อยากรู้เรื่องแพ็กเกจเหรอ? เรามี 4 ระดับ:

🥈 **Silver** $200 USD (120 PV)
   โบนัส Gratitude: 1.5 เท่า (สูงสุด $300)

🥇 **Gold** $600 USD (360 PV)
   โบนัส Gratitude: 2 เท่า (สูงสุด $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   โบนัส Gratitude: 2.5 เท่า (สูงสุด $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   โบนัส Gratitude: 3 เท่า (สูงสุด $16,200)

ยิ่งระดับสูง = โบนัสยิ่งเยอะ! สนใจตัวไหนเอ่ย?""",
        "vi": """oh muốn biết về gói? bên mình có 4 hạng:

🥈 **Silver** $200 USD (120 PV)
   Bonus Gratitude: 1.5x hoàn (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Bonus Gratitude: 2x hoàn (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Bonus Gratitude: 2.5x hoàn (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Bonus Gratitude: 3x hoàn (cap $16,200)

hạng càng cao = bonus càng nhiều! bạn thích cái nào?""",
        "tl": """oh gusto mong malaman ang packages? may 4 tiers tayo:

🥈 **Silver** $200 USD (120 PV)
   Gratitude Bonus: 1.5x return (cap $300)

🥇 **Gold** $600 USD (360 PV)
   Gratitude Bonus: 2x return (cap $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Gratitude Bonus: 2.5x return (cap $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Gratitude Bonus: 3x return (cap $16,200)

mas mataas tier = mas malaki bonus! alin ang interest mo?""",
        "ja": """パッケージについて知りたい？4つのティアーがあるよ：

🥈 **Silver** $200 USD (120 PV)
   Gratitude Bonus: 1.5倍リターン（上限$300）

🥇 **Gold** $600 USD (360 PV)
   Gratitude Bonus: 2倍リターン（上限$1,200）

💎 **Platinum** $1,800 USD (1,080 PV)
   Gratitude Bonus: 2.5倍リターン（上限$4,500）

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Gratitude Bonus: 3倍リターン（上限$16,200）

ティアーが高いほどボーナスも大きい！どれが気になる？""",
        "ko": """패키지가 궁금해? 4개의 티어가 있어:

🥈 **Silver** $200 USD (120 PV)
   Gratitude Bonus: 1.5배 수익 (상한 $300)

🥇 **Gold** $600 USD (360 PV)
   Gratitude Bonus: 2배 수익 (상한 $1,200)

💎 **Platinum** $1,800 USD (1,080 PV)
   Gratitude Bonus: 2.5배 수익 (상한 $4,500)

💎💎 **Diamond** $5,400 USD (3,240 PV)
   Gratitude Bonus: 3배 수익 (상한 $16,200)

티어가 높을수록 보너스도 커! 어느 게 관심이야?""",
    },
    "COMMISSION": {
        "zh": """ok 所以有 7+2 个奖金系统哈哈：

💰 **推荐奖** — 10% 直接推荐
🏗 **对碰奖** — 20 层，每层 0.3%
🌐 **分享奖** — 20 代，每代 0.4%

📊 **级别奖** — 20%-40%（取决于你的级别）
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **团队级差奖**
🎯 **平级奖** — 5%
🌍 **全球分红奖** — 6%（5-10 星）
✈️ **旅游积分** — 每天增长 10%
🙏 **感恩奖** — 最高 3 倍回报

越多建立=越多收入！要我详细解释哪个吗？""",
        "ms": """ok so ada 7+2 sistem bonus haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 floors, 0.3% setiap satu
🌐 **Sharing Award** — 20 generations, 0.4%

📊 **Tier Bonus** — 20%-40% (depend level kau)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (untuk 5-10 stars)
✈️ **Travel Points** — harian 10% increase
🙏 **Gratitude Bonus** — hanggang 3x return

banyak kau build, banyak kau earn lah! nak aku break down mana satu?""",
        "id": """ok jadi ada 7+2 sistem bonus haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 floors, 0.3% per floor
🌐 **Sharing Award** — 20 generations, 0.4%

📊 **Tier Bonus** — 20%-40% (tergantung level kamu)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (untuk 5-10 stars)
✈️ **Travel Points** — harian 10% increase
🙏 **Gratitude Bonus** — sampai 3x return

semakin banyak build, semakin banyak earn! mau aku jelasin yang mana?""",
        "th": """ok มีระบบโบนัส 7+2 ระบบ haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 ชั้น, 0.3% ต่อชั้น
🌐 **Sharing Award** — 20 รุ่น, 0.4%

📊 **Tier Bonus** — 20%-40% (ขึ้นอยู่กับระดับของคุณ)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (สำหรับ 5-10 stars)
✈️ **Travel Points** — เพิ่มขึ้น 10% ต่อวัน
🙏 **Gratitude Bonus** — สูงสุด 3 เท่า

ยิ่งสร้างมาก ยิ่ง earn มาก! อยากรู้รายละเอียดตัวไหน?""",
        "vi": """ok nên có 7+2 hệ thống bonus haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 floors, 0.3% mỗi floor
🌐 **Sharing Award** — 20 generations, 0.4%

📊 **Tier Bonus** — 20%-40% (tùy level của bạn)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (cho 5-10 stars)
✈️ **Travel Points** — tăng 10% mỗi ngày
🙏 **Gratitude Bonus** — tới 3x return

càng build nhiều, càng earn nhiều! muốn mình giải thích cái nào?""",
        "tl": """ok so may 7+2 bonus systems haha:

💰 **Recommendation Award** — 10% direct referral
🏗 **Placement Award** — 20 floors, 0.3% bawat isa
🌐 **Sharing Award** — 20 generations, 0.4%

📊 **Tier Bonus** — 20%-40% (depend sa level mo)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (for 5-10 stars)
✈️ **Travel Points** — daily 10% increase
🙏 **Gratitude Bonus** — hanggang 3x return

mas marami build, mas marami earn! alin gusto mong i-break down?""",
        "ja": """ok 7+2のボーナスシステムがあるよ haha：

💰 **Recommendation Award** — 10% 直接紹介
🏗 **Placement Award** — 20階層、各0.3%
🌐 **Sharing Award** — 20世代、各0.4%

📊 **Tier Bonus** — 20%-40%（ランクによる）
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6%（5-10スター対象）
✈️ **Travel Points** — 毎日10%増加
🙏 **Gratitude Bonus** — 最大3倍リターン

たくさん作るほどたくさん稼げる！詳しく知りたいのはどれ？""",
        "ko": """ok 7+2 보너스 시스템이 있어 haha:

💰 **Recommendation Award** — 10% 직접 추천
🏗 **Placement Award** — 20층, 각 0.3%
🌐 **Sharing Award** — 20세대, 각 0.4%

📊 **Tier Bonus** — 20%-40% (레벨에 따라)
   Silver = 20% | Gold = 25% | Platinum = 30% | Diamond = 40%

⭐️ **Team Grade Difference Bonus**
🎯 **Grade Difference Equal Prize** — 5%
🌍 **Global Dividend Award** — 6% (5-10스타 대상)
✈️ **Travel Points** — 매일 10% 증가
🙏 **Gratitude Bonus** — 최대 3배 수익

많이 만들수록 많이 벌어! 자세히 알고 싶은 건 어느 거?""",
    },
    "RANKING": {
        "zh": """我们有 10 个星级别：

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

每个级别=更高奖金百分比

要求从 10,000 PV 开始，根据级别上升到数百万

你现在什么级别？可以帮你看看下一步！""",
        "ms": """kita ada 10 star levels satu:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

setiap level = bonus percentage lagi tinggi

requirements start dari 10,000 PV dan pergi sampai millions depend level

kau kat level mana sekarang? boleh bantu kau figure out apa next!""",
        "id": """kita punya 10 star levels:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

setiap level = persentase bonus lebih tinggi

requirements mulai dari 10,000 PV dan naik sampai jutaan depend level

kamu sekarang di level mana? bisa bantu kamu cari tahu apa selanjutnya!""",
        "th": """เรามี 10 ระดับดาว:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

แต่ละระดับ = เปอร์เซ็นต์โบนัสสูงขึ้น

requirements เริ่มจาก 10,000 PV และขึ้นไปจนถึงล้านๆ ขึ้นอยู่กับระดับ

ตอนนี้คุณอยู่ระดับไหน? ช่วยดูให้ว่าต่อไปต้องทำอะไร!""",
        "vi": """mình có 10 levels sao:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

mỗi level = tỷ lệ bonus cao hơn

yêu cầu bắt đầu từ 10,000 PV và tăng lên đến hàng triệu tùy level

bây giờ bạn ở level nào? có thể giúp bạn tính bước tiếp theo!""",
        "tl": """may 10 star levels tayo:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

bawat level = mas mataas bonus percentage

requirements nagsisimula sa 10,000 PV at tumaas hanggang millions depend sa level

nasa anong level ka ngayon? matutulungan kitang malaman ang next step!""",
        "ja": """10のスターレベルがあるよ：

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

レベルが上がるほどボーナス率もアップ

要件は10,000 PVから始まって、レベルによって数百万まで

今何レベル？次のステップを教えられるよ！""",
        "ko": """10개의 스타 레벨이 있어:

⭐️ AI Explorer (4%)
⭐️⭐️ AI Advocate (6%)
⭐️⭐️⭐️ AI Influencer (8%)
...
⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ AI Visionary Board (20%)

레벨이 오를수록 보너스 비율도 업

요건은 10,000 PV부터 시작해서 레벨에 따라 수백만까지

지금 몇 레벨이야? 다음 단계 알려줄게!""",
    },
    "CHARGING": {
        "zh": """超级简单：

1️⃣ 插线到 MMEETT 端口
2️⃣ 使用 5V/0.5A 适配器（DC-5V）
3️⃣ 充电到绿灯亮

⏱️ 电池=50 小时总续航
💤 10 分钟无活动自动睡眠

完成 🔋""",
        "ms": """senang gila:

1️⃣ cucuk cable ke port MMEETT
2️⃣ guna adapter 5V/0.5A (DC-5V)
3️⃣ charge sampai lampu hijau

⏱️ battery = 50 jam total
💤 auto sleep lepas 10 minit no activity

done 🔋""",
        "id": """gampang banget:

1️⃣ colok kabel ke port MMEETT
2️⃣ pakai adapter 5V/0.5A (DC-5V)
3️⃣ charge sampai lampu hijau

⏱️ battery = 50 jam total
💤 auto sleep setelah 10 menit no activity

selesai 🔋""",
        "th": """ง่ายมาก:

1️⃣ เสียบสายเข้าพอร์ต MMEETT
2️⃣ ใช้ adapter 5V/0.5A (DC-5V)
3️⃣ ชาร์จจนไฟเขียว

⏱️ แบตเตอรี่ = 50 ชั่วโมงรวม
💤 auto sleep หลัง 10 นาทีไม่มี activity

เสร็จแล้ว 🔋""",
        "vi": """siêu đơn giản:

1️⃣ cắm dây vào cổng MMEETT
2️⃣ dùng adapter 5V/0.5A (DC-5V)
3️⃣ charge đến khi đèn xanh

⏱️ pin = 50 giờ tổng
💤 auto sleep sau 10 phút không hoạt động

xong 🔋""",
        "tl": """super simple:

1️⃣ isaksak cable sa MMEETT port
2️⃣ gumamit ng 5V/0.5A adapter (DC-5V)
3️⃣ i-charge hanggang lumabas green light

⏱️ battery = 50 hours total
💤 auto sleep after 10 min walang activity

tapos 🔋""",
        "ja": """超簡単：

1️⃣ ケーブルをMMEETTポートに挿す
2️⃣ 5V/0.5Aアダプターを使う（DC-5V）
3️⃣ 緑色のランプが点くまで充電

⏱️ バッテリー = 50時間合計
💤 10分間操作なしで自動スリープ

完了 🔋""",
        "ko": """초간단:

1️⃣ 케이블을 MMEETT 포트에 꽂아
2️⃣ 5V/0.5A 어댑터 사용 (DC-5V)
3️⃣ 초록불 들어올 때까지 충전

⏱️ 배터리 = 총 50시간
💤 10분 미사용 시 자동 수면

완료 🔋""",
    },
    "APP_DOWNLOAD": {
        "zh": """app store 或 google play 啦：

📲 **iOS**: App Store → 搜索"MMEETT"
🤖 **Android**: Google Play → 搜索"MMEETT"

安装后：
• 打开蓝牙
• 打开 NFC（用于写卡）
• 需要 Android 6+ 或 iOS 12+

如果没收到验证码=检查垃圾邮件箱 😅

需要设置帮助？tag @ukkbasf 啦""",
        "ms": """app store atau google play lah:

📲 **iOS**: App Store → cari "MMEETT"
🤖 **Android**: Google Play → cari "MMEETT"

lepas install:
• on bluetooth
• on NFC (untuk tulis card)
• perlu Android 6+ atau iOS 12+

kalau no verification code = check spam folder 😅

perlukan help setup? tag @ukkbasf leh""",
        "id": """app store atau google play:

📲 **iOS**: App Store → cari "MMEETT"
🤖 **Android**: Google Play → cari "MMEETT"

setelah install:
• nyalakan bluetooth
• nyalakan NFC (untuk tulis kartu)
• butuh Android 6+ atau iOS 12+

kalau tidak ada kode verifikasi = cek folder spam 😅

butuh bantuan setup? tag @ukkbasf leh""",
        "th": """app store หรือ google play จ้ะ:

📲 **iOS**: App Store → ค้นหา "MMEETT"
🤖 **Android**: Google Play → ค้นหา "MMEETT"

หลังติดตั้ง:
• เปิด bluetooth
• เปิด NFC (สำหรับเขียนการ์ด)
• ต้องใช้ Android 6+ หรือ iOS 12+

ถ้าไม่ได้รหัสยืนยัน = เช็คโฟลเดอร์สแปม 😅

ต้องการความช่วยเหลือ? tag @ukkbasf น่ะ""",
        "vi": """app store hoặc google play nè:

📲 **iOS**: App Store → tìm "MMEETT"
🤖 **Android**: Google Play → tìm "MMEETT"

sau khi cài:
• bật bluetooth
• bật NFC (để ghi thẻ)
• cần Android 6+ hoặc iOS 12+

nếu không nhận mã xác minh = kiểm tra thư rác 😅

cần giúp setup? tag @ukkbasf nha""",
        "tl": """app store o google play:

📲 **iOS**: App Store → hanapin "MMEETT"
🤖 **Android**: Google Play → hanapin "MMEETT"

pagka-install:
• i-on ang bluetooth
• i-on ang NFC (para mag-write ng card)
• kailangan Android 6+ o iOS 12+

kung walang verification code = check spam folder 😅

kailangan ng tulong sa setup? tag @ukkbasf""",
        "ja": """App StoreかGoogle Playでね：

📲 **iOS**: App Store → 「MMEETT」を検索
🤖 **Android**: Google Play → 「MMEETT」を検索

インストール後：
• Bluetoothをオンに
• NFCをオンに（カード書き込み用）
• Android 6+ または iOS 12+ が必要

認証コードが来ない？スパムフォルダーをチェック 😅

セットアップのヘルプが必要？@ukkbasfにタグしてね""",
        "ko": """App Store이나 Google Play에서:

📲 **iOS**: App Store → "MMEETT" 검색
🤖 **Android**: Google Play → "MMEETT" 검색

설치 후:
• 블루투스 켜기
• NFC 켜기 (카드 작성용)
• Android 6+ 또는 iOS 12+ 필요

인증 코드가 안 오면? 스팸 폴더 확인 😅

설치 도움이 필요하면? @ukkbasf 태그해줘""",
    },
    "ACTIVATION": {
        "zh": """ok 这是步骤：

1️⃣ 按住 TRANS 1 秒（蓝灯=开启）
2️⃣ 白灯闪烁=准备绑定
3️⃣ app: "未连接" → "绑定设备"
4️⃣ 靠近手机（iPhone：背部顶部）

写卡激活：
• "我" → "激活 MMEETT 设备"
• 选择卡 → "激活"
• 手机 NFC 必须开启

卡住了？tag 我啦 😇""",
        "ms": """ok sini aku tunjuk:

1️⃣ tekan TRANS 1 saat (lampu biru = on)
2️⃣ lampu putih flash = ready nak bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ letak dekat phone (iPhone: belakang atas)

untuk tulis card link:
• "Me" → "Activate MMEETT Device"
• pilih card → "Activate"
• NFC phone mesti ON

tersangkut? tag aku leh 😇""",
        "id": """ok ini caranya:

1️⃣ tekan TRANS 1 detik (lampu biru = on)
2️⃣ lampu putih kedip = siap bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ dekatkan ke phone (iPhone: belakang atas)

untuk tulis kartu:
• "Me" → "Activate MMEETT Device"
• pilih kartu → "Activate"
• NFC phone harus ON

stuck? tag aku leh 😇""",
        "th": """ok นี่คือวิธีจ้ะ:

1️⃣ กด TRANS 1 วินาที (ไฟน้ำเงิน = on)
2️⃣ ไฟขาวกระพริบ = พร้อม bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ วางใกล้โทรศัพท์ (iPhone: ด้านหลังบน)

สำหรับเขียนการ์ด:
• "Me" → "Activate MMEETT Device"
• เลือกการ์ด → "Activate"
• NFC โทรศัพท์ต้อง ON

ติดขัด? tag ฉันน่ะ 😇""",
        "vi": """ok đây là cách nè:

1️⃣ giữ TRANS 1 giây (đèn xanh = on)
2️⃣ đèn trắng nhấp nháy = sẵn sàng bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ đặt gần phone (iPhone: mặt lưng trên)

để ghi thẻ:
• "Me" → "Activate MMEETT Device"
• chọn thẻ → "Activate"
• NFC phone phải BẬT

bị kẹt? tag mình nha 😇""",
        "tl": """ok eto ang steps:

1️⃣ pindutin ang TRANS 1 second (blue light = on)
2️⃣ white light flashing = ready to bind
3️⃣ app: "Not Connected" → "Bind Device"
4️⃣ ilapit sa phone (iPhone: likod taas)

para mag-write ng card:
• "Me" → "Activate MMEETT Device"
• pumili ng card → "Activate"
• NFC ng phone dapat ON

na-stuck? tag mo ako 😇""",
        "ja": """ok 手順はこう：

1️⃣ TRANSを1秒長押し（青いランプ = 起動）
2️⃣ 白いランプ点滅 = バインド準備OK
3️⃣ アプリ: "Not Connected" → "Bind Device"
4️⃣ スマホの近くに置く（iPhone: 背面上部）

カードのアクティベート：
• "Me" → "Activate MMEETT Device"
• カードを選択 → "Activate"
• NFCをオンにする必要あり

つまずいた？@ukkbasfにタグしてね 😇""",
        "ko": """ok 순서는 이렇게:

1️⃣ TRANS 1초 길게 누르기 (파란불 = 켜짐)
2️⃣ 흰불 깜빡임 = 바인드 준비 완료
3️⃣ 앱: "Not Connected" → "Bind Device"
4️⃣ 스마트폰 가까이 대기 (iPhone: 뒷면 상단)

카드 활성화:
• "Me" → "Activate MMEETT Device"
• 카드 선택 → "Activate"
• NFC 켜져 있어야 함

막혔어? @ukkbasf 태그해줘 😇""",
    },
    "RECORDING": {
        "zh": """🎙️ **现场模式**（不需要手机）：
1. 按住 TRANS 1 秒（蓝灯）
2. 把 MEETING 往上拨
3. 震动+红灯=正在录音

📞 **通话模式**：
1. 按住 TRANS 1 秒（蓝灯）
2. 把 MEETING 往上拨
3. 双击 TRANS（0.5 秒内）
4. 震动+黄灯

⚠️ 通话模式：设备必须贴着手机（不能戴耳机）
❌ 没有暂停功能（停止=新文件）

懂了吗？😇""",
        "ms": """🎙️ **LIVE MODE** (tak perlu phone):
1. tekan TRANS 1 saat (lampu biru)
2. switch MEETING ke atas
3. vibration + RED light = recording

📞 **CALL MODE**:
1. tekan TRANS 1 saat (lampu biru)
2. switch MEETING ke atas
3. double-press TRANS (0.5 saat)
4. vibration + YELLOW light

⚠️ call mode: device mesti sentuh phone (tak boleh pakai headphone)
❌ tak ada pause (stop = file baru)

faham? 😇""",
        "id": """🎙️ **LIVE MODE** (tanpa phone):
1. tekan TRANS 1 detik (lampu biru)
2. switch MEETING ke atas
3. vibration + RED light = recording

📞 **CALL MODE**:
1. tekan TRANS 1 detik (lampu biru)
2. switch MEETING ke atas
3. double-press TRANS (0.5 detik)
4. vibration + YELLOW light

⚠️ call mode: device harus menempel ke phone (tanpa headphone)
❌ tidak ada pause (stop = file baru)

ngerti? 😇""",
        "th": """🎙️ **LIVE MODE** (ไม่ต้องใช้โทรศัพท์):
1. กด TRANS 1 วินาที (ไฟน้ำเงิน)
2. สลับ MEETING ขึ้น
3. สั่น + ไฟแดง = กำลังบันทึก

📞 **CALL MODE**:
1. กด TRANS 1 วินาที (ไฟน้ำเงิน)
2. สลับ MEETING ขึ้น
3. กด TRANS สองครั้ง (0.5 วินาที)
4. สั่น + ไฟเหลือง

⚠️ call mode: อุปกรณ์ต้องวางติดโทรศัพท์ (ห้ามใส่หูฟัง)
❌ ไม่มีปุ่มหยุดชั่วคราว (หยุด = ไฟล์ใหม่)

เข้าใจมั้ยจ้ะ? 😇""",
        "vi": """🎙️ **LIVE MODE** (không cần phone):
1. giữ TRANS 1 giây (đèn xanh)
2. gạt MEETING lên
3. rung + ĐÈN ĐỎ = đang ghi

📞 **CALL MODE**:
1. giữ TRANS 1 giây (đèn xanh)
2. gạt MEETING lên
3. nhấn đúp TRANS (0.5 giây)
4. rung + ĐÈN VÀNG

⚠️ call mode: thiết bị phải áp sát phone (không đeo tai nghe)
❌ không có nút tạm dừng (dừng = file mới)

hiểu chưa? 😇""",
        "tl": """🎙️ **LIVE MODE** (walang phone needed):
1. pindutin ang TRANS 1 sec (blue light)
2. i-switch MEETING pataas
3. vibration + RED light = nagre-record

📞 **CALL MODE**:
1. pindutin ang TRANS 1 sec (blue light)
2. i-switch MEETING pataas
3. double-press ang TRANS (0.5 sec)
4. vibration + YELLOW light

⚠️ call mode: device dapat nakadikit sa phone (walang headphones)
❌ walang pause feature (stop = bagong file)

gets mo? 😇""",
        "ja": """🎙️ **LIVE MODE**（スマホ不要）:
1. TRANSを1秒長押し（青いランプ）
2. MEETINGを上にスイッチ
3. 振動＋赤いランプ = 録音中

📞 **CALL MODE**:
1. TRANSを1秒長押し（青いランプ）
2. MEETINGを上にスイッチ
3. TRANSをダブルクリック（0.5秒以内）
4. 振動＋黄色いランプ

⚠️ 通話モード：デバイスをスマホに密着させる（イヤホン不可）
❌ 一時停止機能なし（停止 = 新しいファイル）

わかった？😇""",
        "ko": """🎙️ **LIVE MODE** (스마트폰 불필요):
1. TRANS 1초 길게 누르기 (파란불)
2. MEETING 위로 스위치
3. 진동 + 빨간불 = 녹음 중

📞 **CALL MODE**:
1. TRANS 1초 길게 누르기 (파란불)
2. MEETING 위로 스위치
3. TRANS 더블클릭 (0.5초 이내)
4. 진동 + 노란불

⚠️ 통화 모드: 기기를 스마트폰에 밀착 (이어폰 불가)
❌ 일시정지 없음 (정지 = 새 파일)

알겠어? 😇""",
    },
    "SYNC": {
        "zh": """🔄 **同步录音**：

1. 连接设备到 app（蓝牙）
2. app 显示："待同步文件"
3. 选择：全部同步或选择文件
4. 同步后文件自动删除

⚡️ 传输速度：
• 蓝牙 = ~几十 KB/秒（慢）
• WiFi = 快很多（推荐）

📂 电脑文件夹空的？同步后文件自动删除。从 app 导出。

明白了吗？😇""",
        "ms": """🔄 **Sync Recordings**:

1. connect device ke app (Bluetooth)
2. app tunjuk: "Files pending sync"
3. pilih: Sync all ATAU pilih file
4. file auto-delete lepas sync

⚡️ transfer speeds:
• Bluetooth = ~tens of KB/sec (lambat)
• WiFi = lagi cepat (recommended)

📂 folder kosong kat computer? file auto-delete lepas sync. export dari app.

faham? 😇""",
        "id": """🔄 **Sync Recordings**:

1. hubungkan device ke app (Bluetooth)
2. app tampil: "Files pending sync"
3. pilih: Sync all ATAU pilih file tertentu
4. file auto-delete setelah sync

⚡️ kecepatan transfer:
• Bluetooth = ~puluhan KB/detik (lambat)
• WiFi = jauh lebih cepat (recommended)

📂 folder kosong di komputer? file auto-delete setelah sync. export dari app.

ngerti? 😇""",
        "th": """🔄 **ซิงค์บันทึก**:

1. เชื่อมต่ออุปกรณ์กับแอป (Bluetooth)
2. แอปแสดง: "Files pending sync"
3. เลือก: ซิงค์ทั้งหมด หรือ เลือกไฟล์
4. ไฟล์ลบอัตโนมัติหลังซิงค์

⚡️ ความเร็วถ่ายโอน:
• Bluetooth = ~หลักร้อย KB/วินาที (ช้า)
• WiFi = เร็วกว่ามาก (แนะนำ)

📂 โฟลเดอร์ในคอมว่าง? ไฟล์ลบอัตโนมัติหลังซิงค์ ให้ export จากแอป

เข้าใจมั้ยจ้ะ? 😇""",
        "vi": """🔄 **Đồng bộ ghi âm**:

1. kết nối thiết bị với app (Bluetooth)
2. app hiển thị: "Files pending sync"
3. chọn: Sync all HOẶC chọn file
4. file tự xóa sau khi sync

⚡️ tốc độ truyền:
• Bluetooth = ~vài chục KB/giây (chậm)
• WiFi = nhanh hơn nhiều (khuyên dùng)

📂 thư mục máy tính trống? file tự xóa sau sync. export từ app.

hiểu chưa? 😇""",
        "tl": """🔄 **Sync Recordings**:

1. i-connect ang device sa app (Bluetooth)
2. mag-show: "Files pending sync"
3. pumili: Sync all O pumili ng files
4. auto-delete ang files pagkatapos ng sync

⚡️ transfer speeds:
• Bluetooth = ~tens of KB/sec (mabagal)
• WiFi = mas mabilis (recommended)

📂 walang laman ang folder sa computer? auto-delete ang files pagkatapos sync. i-export mula sa app.

naintindihan? 😇""",
        "ja": """🔄 **録音の同期**:

1. デバイスをアプリに接続（Bluetooth）
2. アプリに表示: "Files pending sync"
3. 選択: 全同期 または ファイル選択
4. 同期後ファイルは自動削除

⚡️ 転送速度:
• Bluetooth = ~数十KB/秒（遅い）
• WiFi = はるかに速い（おすすめ）

📂 パソコンのフォルダーが空？同期後自動削除されるよ。アプリからエクスポートしてね。

わかった？😇""",
        "ko": """🔄 **녹음 동기화**:

1. 기기를 앱에 연결 (Bluetooth)
2. 앱 표시: "Files pending sync"
3. 선택: 전체 동기화 또는 파일 선택
4. 동기화 후 파일 자동 삭제

⚡️ 전송 속도:
• Bluetooth = ~수십 KB/초 (느림)
• WiFi = 훨씬 빠름 (추천)

📂 컴퓨터 폴더가 비어있어? 동기화 후 자동 삭제됨. 앱에서 내보내기.

알겠어? 😇""",
    },
    "TRANSCRIPTION": {
        "zh": """📝 **转录**：

⏱️ 时间 = ~录音长度的 50%
例如：1 小时录音 = ~30 分钟

🌍 多语言（自动检测）：
• English • 中文 • 日本語 • ไทย • 한국어

很快的！😇""",
        "ms": """📝 **Transcription**:

⏱️ masa = ~50% daripada panjang recording
contoh: 1 jam recording = ~30 minit

🌍 multi-language (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

cepat satu! 😇""",
        "id": """📝 **Transkripsi**:

⏱️ waktu = ~50% dari durasi recording
contoh: 1 jam recording = ~30 menit

🌍 multi-bahasa (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

cukup cepat! 😇""",
        "th": """📝 **การถอดเสียง**:

⏱️ เวลา = ~50% ของความยาวบันทึก
ตัวอย่าง: บันทึก 1 ชั่วโมง = ~30 นาที

🌍 หลายภาษา (ตรวจจับอัตโนมัติ):
• English • 中文 • 日本語 • ไทย • 한국어

เร็วมากจ้ะ! 😇""",
        "vi": """📝 **Chuyển đổi văn bản**:

⏱️ thời gian = ~50% độ dài bản ghi
ví dụ: ghi âm 1 tiếng = ~30 phút

🌍 đa ngôn ngữ (tự động phát hiện):
• English • 中文 • 日本語 • ไทย • 한국어

khá nhanh nha! 😇""",
        "tl": """📝 **Transcription**:

⏱️ oras = ~50% ng haba ng recording
halimbawa: 1 oras na recording = ~30 min

🌍 multi-language (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

mabilis ito! 😇""",
        "ja": """📝 **文字起こし**:

⏱️ 時間 = 録音長の約50%
例：1時間の録音 = 約30分

🌍 多言語対応（自動検出）:
• English • 中文 • 日本語 • ไทย • 한국어

けっこう速いよ！😇""",
        "ko": """📝 **전사**:

⏱️ 시간 = 녹음 길이의 약 50%
예: 1시간 녹음 = 약 30분

🌍 다국어 지원 (자동 감지):
• English • 中文 • 日本語 • ไทย • 한국어

꽤 빠르다! 😇""",
    },
    "AI_CHAT": {
        "zh": """🤖 **AI 聊天功能**：

1. 去 app 的"AI Chat"标签
2. 跟 Mr. MMEETT 代理聊天
3. 切换模型：GPT、Gemini、DeepSeek
4. 开启"网络搜索"获取实时信息
5. 开启"思考模式"处理复杂问题

💡 思考模式=显示 AI 推理过程（仅 DeepSeek/Gemini）

想试试？😇""",
        "ms": """🤖 **AI Chat Feature**:

1. pergi ke tab "AI Chat" dalam app
2. chat dengan agent Mr. MMEETT
3. tukar model: GPT, Gemini, DeepSeek
4. on "Web Search" untuk info real-time
5. on "Think Mode" untuk soalan kompleks

💡 Think Mode = tunjuk AI reasoning (DeepSeek/Gemini sahaja)

nak try? 😇""",
        "id": """🤖 **AI Chat Feature**:

1. buka tab "AI Chat" di app
2. chat dengan agent Mr. MMEETT
3. ganti model: GPT, Gemini, DeepSeek
4. aktifkan "Web Search" untuk info real-time
5. aktifkan "Think Mode" untuk pertanyaan kompleks

💡 Think Mode = tampilkan AI reasoning (DeepSeek/Gemini saja)

mau coba? 😇""",
        "th": """🤖 **ฟีเจอร์ AI Chat**:

1. ไปที่แท็บ "AI Chat" ในแอป
2. คุยกับ Mr. MMEETT agent
3. สลับโมเดล: GPT, Gemini, DeepSeek
4. เปิด "Web Search" สำหรับข้อมูลแบบเรียลไทม์
5. เปิด "Think Mode" สำหรับคำถามซับซ้อน

💡 Think Mode = แสดงการให้เหตุผลของ AI (DeepSeek/Gemini เท่านั้น)

อยากลองมั้ยจ้ะ? 😇""",
        "vi": """🤖 **Tính năng AI Chat**:

1. vào tab "AI Chat" trong app
2. chat với agent Mr. MMEETT
3. chuyển model: GPT, Gemini, DeepSeek
4. bật "Web Search" để lấy thông tin real-time
5. bật "Think Mode" cho câu hỏi phức tạp

💡 Think Mode = hiển thị quá trình suy luận AI (chỉ DeepSeek/Gemini)

muốn thử không? 😇""",
        "tl": """🤖 **AI Chat Feature**:

1. pumunta sa "AI Chat" tab sa app
2. mag-chat sa Mr. MMEETT agent
3. mag-switch ng models: GPT, Gemini, DeepSeek
4. i-enable ang "Web Search" para sa real-time info
5. i-enable ang "Think Mode" para sa complex na tanong

💡 Think Mode = ipinapakita ang AI reasoning (DeepSeek/Gemini lang)

gusto mong subukan? 😇""",
        "ja": """🤖 **AIチャット機能**:

1. アプリの「AI Chat」タブへ
2. Mr. MMEETTエージェントとチャット
3. モデル切替：GPT、Gemini、DeepSeek
4. 「Web Search」でリアルタイム情報
5. 「Think Mode」で複雑な質問に対応

💡 Think Mode = AIの思考プロセスを表示（DeepSeek/Geminiのみ）

試してみる？😇""",
        "ko": """🤖 **AI 채팅 기능**:

1. 앱의 "AI Chat" 탭으로 이동
2. Mr. MMEETT 에이전트와 채팅
3. 모델 전환: GPT, Gemini, DeepSeek
4. "Web Search"로 실시간 정보
5. "Think Mode"로 복잡한 질문에 대응

💡 Think Mode = AI 추론 과정 표시 (DeepSeek/Gemini만)

한번 써볼래? 😇""",
    },
    "SHIPPING": {
        "zh": """📦 **配送信息**：

📦 处理：3-5 个工作日
🚚 配送：6-15 个工作日

📍 追踪订单：
App → "我" → "会员" → "订单"

🌍 全球配送

还有其他问题吗？😇""",
        "ms": """📦 **Shipping & Delivery**:

📦 processing: 3-5 hari bekerja
🚚 delivery: 6-15 hari bekerja

📍 track order:
App → "Me" → "Member" → "Orders"

🌍 shipping seluruh dunia

ada lagi? 😇""",
        "id": """📦 **Pengiriman**:

📦 proses: 3-5 hari kerja
🚚 pengiriman: 6-15 hari kerja

📍 lacak pesanan:
App → "Me" → "Member" → "Orders"

🌍 pengiriman ke seluruh dunia

ada yang lain? 😇""",
        "th": """📦 **การจัดส่ง**:

📦 ดำเนินการ: 3-5 วันทำการ
🚚 จัดส่ง: 6-15 วันทำการ

📍 ติดตามคำสั่งซื้อ:
App → "Me" → "Member" → "Orders"

🌍 จัดส่งทั่วโลก

มีอะไรอีกมั้ยจ้ะ? 😇""",
        "vi": """📦 **Vận chuyển**:

📦 xử lý: 3-5 ngày làm việc
🚚 giao hàng: 6-15 ngày làm việc

📍 theo dõi đơn hàng:
App → "Me" → "Member" → "Orders"

🌍 giao hàng toàn cầu

còn gì nữa không? 😇""",
        "tl": """📦 **Shipping & Delivery**:

📦 processing: 3-5 business days
🚚 delivery: 6-15 business days

📍 i-track ang order:
App → "Me" → "Member" → "Orders"

🌍 worldwide shipping available

may iba pa? 😇""",
        "ja": """📦 **配送情報**:

📦 処理：3-5営業日
🚚 配送：6-15営業日

📍 注文追跡:
App → "Me" → "Member" → "Orders"

🌍 世界中に配送可能

他に質問ある？😇""",
        "ko": """📦 **배송 정보**:

📦 처리: 3-5 영업일
🚚 배송: 6-15 영업일

📍 주문 추적:
App → "Me" → "Member" → "Orders"

🌍 전 세계 배송 가능

더 궁금한 거 있어? 😇""",
    },
    "RETURNS": {
        "zh": """🔄 **退货与保修**：

🔄 退货：购买后 20 天内
• MMEETT 卡、会员、算力

🔧 保修：购买后 12 个月
• 保修期内免费维修
• 需要：序列号+购买凭证

📞 联系：App → "我" → "客服"

有问题？tag @ukkbasf 啦 😇""",
        "ms": """🔄 **Returns & Warranty**:

🔄 returns: 20 hari dari pembelian
• MMEETT Card, Membership, Computing power

🔧 warranty: 12 bulan dari pembelian
• repair percuma semasa warranty
• perlu: serial number + bukti pembelian

📞 contact: App → "Me" → "Customer Service"

ada masalah? tag @ukkbasf leh 😇""",
        "id": """🔄 **Pengembalian & Garansi**:

🔄 pengembalian: 20 hari dari pembelian
• MMEETT Card, Membership, Computing power

🔧 garansi: 12 bulan dari pembelian
• perbaikan gratis selama garansi
• perlu: nomor serial + bukti pembelian

📞 hubungi: App → "Me" → "Customer Service"

ada masalah? tag @ukkbasf leh 😇""",
        "th": """🔄 **คืนสินค้า & รับประกัน**:

🔄 คืนสินค้า: 20 วันจากวันซื้อ
• MMEETT Card, Membership, Computing power

🔧 รับประกัน: 12 เดือนจากวันซื้อ
• ซ่อมฟรีระหว่างรับประกัน
• ต้องมี: serial number + หลักฐานการซื้อ

📞 ติดต่อ: App → "Me" → "Customer Service"

มีปัญหา? tag @ukkbasf น่ะ 😇""",
        "vi": """🔄 **Đổi trả & Bảo hành**:

🔄 đổi trả: 20 ngày từ ngày mua
• MMEETT Card, Membership, Computing power

🔧 bảo hành: 12 tháng từ ngày mua
• sửa chữa miễn phí trong thời bảo hành
• cần: số serial + hóa đơn mua hàng

📞 liên hệ: App → "Me" → "Customer Service"

có vấn đề? tag @ukkbasf nha 😇""",
        "tl": """🔄 **Returns & Warranty**:

🔄 returns: 20 days mula sa purchase
• MMEETT Card, Membership, Computing power

🔧 warranty: 12 months mula sa purchase
• libreng repair habang nasa warranty
• kailangan: serial number + proof of purchase

📞 contact: App → "Me" → "Customer Service"

may issue? tag @ukkbasf 😇""",
        "ja": """🔄 **返品・保証**:

🔄 返品：購入後20日以内
• MMEETT Card, Membership, Computing power

🔧 保証：購入後12ヶ月
• 保証期間中の修理は無料
• 必要：シリアル番号＋購入証明

📞 連絡先: App → "Me" → "Customer Service"

問題ある？@ukkbasfにタグしてね 😇""",
        "ko": """🔄 **반품 & 보증**:

🔄 반품: 구매 후 20일 이내
• MMEETT Card, Membership, Computing power

🔧 보증: 구매 후 12개월
• 보증 기간 중 수리 무료
• 필요: 시리얼 번호 + 구매 증명

📞 연락처: App → "Me" → "Customer Service"

문제 있어? @ukkbasf 태그해줘 😇""",
    },
    "TRAVEL_POINTS": {
        "zh": """✈️ **旅游积分**：

每天 10% 奖金增长！

基本上=每天你的奖金池增长 10%

用途：
• 公司旅行
• 活动
• 或兑换现金（取决于级别）

很不错吧？😇""",
        "ms": """✈️ **Travel Points**:

harian 10% bonus increase satu!

bascially = setiap hari bonus pool kau naik 10%

guna untuk:
• trip company
• event
• atau tukar cash (depend level)

best kan? 😇""",
        "id": """✈️ **Travel Points**:

harian 10% bonus increase!

pada dasarnya = setiap hari bonus pool kamu naik 10%

digunakan untuk:
• trip perusahaan
• event
• atau konversi ke cash (tergantung level)

keren kan? 😇""",
        "th": """✈️ **Travel Points**:

โบนัสเพิ่มขึ้น 10% ทุกวันจ้ะ!

โดยพื้นฐาน = ทุกวัน pool โบนัสของคุณเพิ่มขึ้น 10%

ใช้สำหรับ:
• ทริปบริษัท
• กิจกรรม
• หรือแปลงเป็นเงินสด (ขึ้นอยู่กับระดับ)

ดีมั้ยจ้ะ? 😇""",
        "vi": """✈️ **Travel Points**:

tăng bonus 10% mỗi ngày!

về cơ bản = mỗi ngày pool bonus của bạn tăng 10%

dùng để:
• chuyến đi công ty
• sự kiện
• hoặc quy đổi tiền mặt (tùy level)

hay không? 😇""",
        "tl": """✈️ **Travel Points**:

daily 10% bonus increase!

basically = araw-araw tumataas ng 10% ang bonus pool mo

gamit para sa:
• company trips
• events
• o i-convert sa cash (depend sa level)

maganda di ba? 😇""",
        "ja": """✈️ **トラベルポイント**:

毎日10%ボーナス増加！

基本的に = 毎日ボーナスプールが10%増える

使い道：
• 会社の旅行
• イベント
• または現金交換（レベルによる）

いいでしょ？😇""",
        "ko": """✈️ **트래블 포인트**:

매일 10% 보너스 증가!

기본적으로 = 매일 보너스 풀이 10% 늘어나

사용처:
• 회사 여행
• 이벤트
• 또는 현금 전환 (레벨에 따라)

좋지? 😇""",
    },
    "GRADE_DIFFERENCE": {
        "zh": """🎯 **级差奖金**：

**团队级差奖**：
根据你和你团队的级别差赚取

**平级奖** = 5%
当你和推荐人同级别时，你仍然赚 5%

所以即使同级别也能赚！😇

搞不懂？可以再解释！""",
        "ms": """🎯 **Grade Difference Bonuses**:

**Team Grade Difference**:
earn dari perbezaan antara level kau dan team kau

**Grade Difference Equal Prize** = 5%
bila kau dan referral sama level, kau masih earn 5%

jadi walaupun sama rank, masih boleh earn! 😇

confusing? boleh explain lagi kalau kau nak!""",
        "id": """🎯 **Grade Difference Bonuses**:

**Team Grade Difference**:
earn dari selisih antara level kamu dan team kamu

**Grade Difference Equal Prize** = 5%
saat kamu dan referral level sama, kamu tetap earn 5%

jadi walaupun rank sama, tetap bisa earn! 😇

bingung? bisa aku jelasin lagi kalau kamu mau!""",
        "th": """🎯 **โบนัสผลต่างระดับ**:

**Team Grade Difference**:
รับจากความแตกต่างระหว่างระดับของคุณกับทีม

**Grade Difference Equal Prize** = 5%
เมื่อคุณกับคนแนะนำระดับเดียวกัน คุณยังได้ 5%

ดังนั้นแม้ระดับเดียวกันก็ยัง earn ได้! 😇

งงมั้ย? อธิบายเพิ่มได้น่ะ!""",
        "vi": """🎯 **Bonus chênh lệch cấp bậc**:

**Team Grade Difference**:
kiếm từ chênh lệch giữa level của bạn và team

**Grade Difference Equal Prize** = 5%
khi bạn và người giới thiệu cùng level, bạn vẫn earn 5%

nên dù cùng rank vẫn earn được! 😇

rối? có thể giải thích thêm!""",
        "tl": """🎯 **Grade Difference Bonuses**:

**Team Grade Difference**:
earn mula sa difference ng level mo at ng team mo

**Grade Difference Equal Prize** = 5%
kapag ikaw at ang referral mo ay same level, earn ka pa rin ng 5%

kaya kahit same rank, earn pa rin! 😇

nakakalito? pwede ko i-explain ulit!""",
        "ja": """🎯 **グレード差ボーナス**:

**Team Grade Difference**:
自分とチームのランク差から収益を得る

**Grade Difference Equal Prize** = 5%
自分と紹介者が同じランクでも5%もらえる

だから同じランクでも稼げる！😇

わからない？もっと説明するよ！""",
        "ko": """🎯 **등급 차이 보너스**:

**Team Grade Difference**:
자신과 팀의 랭크 차이로 수익 창출

**Grade Difference Equal Prize** = 5%
자신과 추천인이 같은 랭크여도 5% 획득

같은 랭크여도 벌 수 있어! 😇

헷갈려? 더 설명해줄게!""",
    },
    "GLOBAL_DIVIDEND": {
        "zh": """🌍 **全球分红奖**：

6% 全球池分配给 5-10 星会员

要求：
• 至少达到 5 星级别
• 保持业绩

这是大的—整个公司增长的被动收入！😇

你在瞄准什么级别？""",
        "ms": """🌍 **Global Dividend Award**:

6% dari global pool dikongsi antara ahli 5-10 stars

requirements:
• capai minimum level 5-star
• maintain performance

ni yang besar lah — passive income dari growth seluruh company! 😇

kau aiming level apa?""",
        "id": """🌍 **Global Dividend Award**:

6% dari pool global dibagikan ke member 5-10 stars

persyaratan:
• capai minimal level 5-star
• pertahankan performa

ini yang besar — passive income dari pertumbuhan seluruh perusahaan! 😇

kamu aiming level apa?""",
        "th": """🌍 **Global Dividend Award**:

6% ของกองทุนทั่วโลกแบ่งให้สมาชิก 5-10 ดาว

ข้อกำหนด:
• ถึงระดับ 5 ดาวขั้นต่ำ
• รักษาผลงาน

นี่คือตัวใหญ่เลย — passive income จากการเติบโตของบริษัท! 😇

คุณกำลังมุ่งสู่ระดับไหน?""",
        "vi": """🌍 **Global Dividend Award**:

6% pool toàn cầu chia cho thành viên 5-10 sao

yêu cầu:
• đạt tối thiểu level 5 sao
• duy trì hiệu suất

đây là cái lớn — passive income từ sự tăng trưởng toàn công ty! 😇

bạn đang hướng tới level nào?""",
        "tl": """🌍 **Global Dividend Award**:

6% ng global pool na ibinabahagi sa 5-10 star members

requirements:
• abutin ang minimum na 5-star level
• maintain ang performance

ito ang malaki — passive income mula sa growth ng buong company! 😇

anong level ang target mo?""",
        "ja": """🌍 **グローバル配当アワード**:

6%のグローバルプールを5-10スター会員でシェア

要件：
• 5スター以上到達
• パフォーマンスを維持

これはデカい — 会社全体の成長からのパッシブ収入！😇

どのレベルを目指してる？""",
        "ko": """🌍 **글로벌 배당 어워드**:

6% 글로벌 풀을 5-10스타 회원에게 배분

요건:
• 최소 5스타 레벨 달성
• 실적 유지

이건 크다 — 회사 전체 성장에서 오는 패시브 인컴! 😇

어떤 레벨을 목표로 해?""",
    },
    "FAVORITE_COLOR": {
        "zh": """绿色，因为钱的颜色嘛 哈哈 🤑🤑

（不过说真的，MMEETT 绿色就像充电灯一样 🔋）""",
        "ms": """hijau sebab warna duit lah lol 🤑🤑

(tapi serious, MMEETT hijau macam lampu charging 🔋)""",
        "id": """hijau karena warna uang lol 🤑🤑

(tapi serius, MMEETT hijau kayak lampu charging 🔋)""",
        "th": """เขียวเพราะสีของเงิน lol 🤑🤑

(แต่จริงๆ MMEETT เขียวเหมือนไฟชาร์จ 🔋)""",
        "vi": """xanh vì màu tiền chứ lol 🤑🤑

(nhưng thật ra, MMEETT xanh như đèn charging 🔋)""",
        "tl": """green kasi color ng pera lol 🤑🤑

(but seriously, MMEETT green parang charging light 🔋)""",
        "ja": """緑！お金の色だからね lol 🤑🤑

（でも本当は、MMEETTの緑は充電ランプみたい 🔋）""",
        "ko": """초록! 돈의 색이니까 lol 🤑🤑

(근데 진짜는, MMEETT 초록이 충전불 같아 🔋)""",
    },
    "DEVICE_SETUP": {
        "zh": """**设备设置**：

1️⃣ 拆箱你的 MMEETT 设备
2️⃣ 先充电（5V/0.5A 适配器）
3️⃣ 下载 MMEETT app
4️⃣ 开启手机蓝牙+NFC
5️⃣ 在 app 中绑定设备

准备就绪！🔋""",
        "ms": """**Device Setup**:

1️⃣ unbox device MMEETT kau
2️⃣ charge dulu (adapter 5V/0.5A)
3️⃣ download app MMEETT
4️⃣ on bluetooth + NFC kat phone
5️⃣ bind device dalam app

ready to go! 🔋""",
        "id": """**Device Setup**:

1️⃣ unbox perangkat MMEETT kamu
2️⃣ charge dulu (adapter 5V/0.5A)
3️⃣ download app MMEETT
4️⃣ nyalakan bluetooth + NFC di phone
5️⃣ bind device di app

siap! 🔋""",
        "th": """**ตั้งค่าอุปกรณ์**:

1️⃣ แกะกล่องอุปกรณ์ MMEETT ของคุณ
2️⃣ ชาร์จก่อน (adapter 5V/0.5A)
3️⃣ ดาวน์โหลดแอป MMEETT
4️⃣ เปิด bluetooth + NFC บนโทรศัพท์
5️⃣ bind device ในแอป

พร้อมใช้งาน! 🔋""",
        "vi": """**Thiết lập thiết bị**:

1️⃣ mở hộp thiết bị MMEETT
2️⃣ charge trước (adapter 5V/0.5A)
3️⃣ tải app MMEETT
4️⃣ bật bluetooth + NFC trên phone
5️⃣ bind thiết bị trong app

sẵn sàng! 🔋""",
        "tl": """**Device Setup**:

1️⃣ i-unbox ang MMEETT device mo
2️⃣ i-charge muna (5V/0.5A adapter)
3️⃣ i-download ang MMEETT app
4️⃣ i-on ang bluetooth + NFC sa phone
5️⃣ i-bind ang device sa app

ready na! 🔋""",
        "ja": """**デバイスセットアップ**:

1️⃣ MMEETTデバイスを開封
2️⃣ まず充電（5V/0.5Aアダプター）
3️⃣ MMEETTアプリをダウンロード
4️⃣ Bluetooth＋NFCをオンに
5️⃣ アプリでデバイスをバインド

準備完了！🔋""",
        "ko": """**기기 설정**:

1️⃣ MMEETT 기기 개봉
2️⃣ 먼저 충전 (5V/0.5A 어댑터)
3️⃣ MMEETT 앱 다운로드
4️⃣ 블루투스 + NFC 켜기
5️⃣ 앱에서 기기 바인드

준비 완료! 🔋""",
    },
    "CONNECTIVITY": {
        "zh": """**连接**：

📶 **蓝牙**：5.0+（范围：~10 米）
📶 **WiFi**：2.4GHz 支持快速同步

💡 提示：
• 配对时设备靠近手机
• 如果有问题关闭其他蓝牙设备
• 连接断开时重启蓝牙

有问题？tag @ukkbasf 😇""",
        "ms": """**Connectivity**:

📶 **Bluetooth**: 5.0+ (range: ~10m)
📶 **WiFi**: 2.4GHz support untuk sync cepat

💡 tips:
• letak device dekat phone semasa pairing
• tutup device bluetooth lain kalau ada masalah
• restart bluetooth kalau connection drop

ada masalah? tag @ukkbasf 😇""",
        "id": """**Konektivitas**:

📶 **Bluetooth**: 5.0+ (jarak: ~10m)
📶 **WiFi**: 2.4GHz untuk sync cepat

💡 tips:
• dekatkan device ke phone saat pairing
• matikan device bluetooth lain kalau ada masalah
• restart bluetooth kalau koneksi terputus

ada masalah? tag @ukkbasf 😇""",
        "th": """**การเชื่อมต่อ**:

📶 **Bluetooth**: 5.0+ (ระยะ: ~10m)
📶 **WiFi**: 2.4GHz สำหรับซิงค์เร็ว

💡 เคล็ดลับ:
• วางอุปกรณ์ใกล้โทรศัพท์ตอนจับคู่
• ปิดอุปกรณ์ bluetooth อื่นหากมีปัญหา
• รีสตาร์ท bluetooth หากการเชื่อมต่อหลุด

มีปัญหา? tag @ukkbasf 😇""",
        "vi": """**Kết nối**:

📶 **Bluetooth**: 5.0+ (phạm vi: ~10m)
📶 **WiFi**: 2.4GHz hỗ trợ sync nhanh

💡 mẹo:
• đặt thiết bị gần phone khi pair
• tắt thiết bị bluetooth khác nếu gặp vấn đề
• khởi động lại bluetooth nếu mất kết nối

có vấn đề? tag @ukkbasf 😇""",
        "tl": """**Connectivity**:

📶 **Bluetooth**: 5.0+ (range: ~10m)
📶 **WiFi**: 2.4GHz support para sa mabilis na sync

💡 tips:
• ilapit ang device sa phone habang nag-papair
• i-off ang ibang bluetooth devices kung may issue
• i-restart ang bluetooth kung nawawala ang connection

may problema? tag @ukkbasf 😇""",
        "ja": """**接続**:

📶 **Bluetooth**: 5.0+（範囲：約10m）
📶 **WiFi**: 2.4GHz 高速同期対応

💡 ヒント:
• ペアリング時はデバイスをスマホの近くに
• 問題がある場合は他のBluetooth機器をオフに
• 接続が切れたらBluetoothを再起動

問題ある？@ukkbasfにタグしてね 😇""",
        "ko": """**연결**:

📶 **Bluetooth**: 5.0+ (범위: ~10m)
📶 **WiFi**: 2.4GHz 빠른 동기화 지원

💡 팁:
• 페어링할 때 기기를 스마트폰 가까이
• 문제 있으면 다른 블루투스 기기 끄기
• 연결 끊기면 블루투스 재시작

문제 있어? @ukkbasf 태그해줘 😇""",
    },
    "NFC_CARDS": {
        "zh": """**NFC 卡**：

💳 MMEETT 使用 NFC 卡激活
📱 手机 NFC 必须开启才能写卡

使用方法：
1. 我 → 激活 MMEETT 设备
2. 选择卡类型
3. 卡贴手机背面（iPhone 顶部）
4. 等待确认

⚠️ 卡片远离磁铁！""",
        "ms": """**NFC Cards**:

💳 MMEETT guna NFC card untuk activation
📱 NFC phone mesti ON untuk tulis card

cara guna:
1. Me → Activate MMEETT Device
2. pilih jenis card
3. tap card ke belakang phone (iPhone: atas)
4. tunggu confirmation

⚠️ jauhkan card dari magnet!""",
        "id": """**NFC Cards**:

💳 MMEETT menggunakan NFC card untuk aktivasi
📱 NFC phone harus ON untuk menulis kartu

cara pakai:
1. Me → Activate MMEETT Device
2. pilih tipe kartu
3. tap kartu ke belakang phone (iPhone: atas)
4. tunggu konfirmasi

⚠️ jauhkan kartu dari magnet!""",
        "th": """**NFC Cards**:

💳 MMEETT ใช้ NFC card สำหรับการเปิดใช้งาน
📱 NFC โทรศัพท์ต้อง ON เพื่อเขียนการ์ด

วิธีใช้:
1. Me → Activate MMEETT Device
2. เลือกประเภทการ์ด
3. แตะการ์ดที่ด้านหลังโทรศัพท์ (iPhone: ด้านบน)
4. รอการยืนยัน

⚠️ เก็บการ์ดห่างจากแม่เหล็ก!""",
        "vi": """**NFC Cards**:

💳 MMEETT dùng NFC card để kích hoạt
📱 NFC phone phải BẬT để ghi thẻ

cách dùng:
1. Me → Activate MMEETT Device
2. chọn loại thẻ
3. chạm thẻ vào mặt lưng phone (iPhone: phía trên)
4. chờ xác nhận

⚠️ giữ thẻ xa nam châm!""",
        "tl": """**NFC Cards**:

💳 MMEETT gumagamit ng NFC cards para sa activation
📱 NFC ng phone dapat ON para makapag-write ng card

paano gamitin:
1. Me → Activate MMEETT Device
2. pumili ng card type
3. i-tap ang card sa likod ng phone (iPhone: taas)
4. maghintay ng confirmation

⚠️ layuan ang cards sa magnets!""",
        "ja": """**NFCカード**:

💳 MMEETTはNFCカードでアクティベート
📱 カード書き込みにはNFCをオンにする必要あり

使い方:
1. Me → Activate MMEETT Device
2. カードタイプを選択
3. カードをスマホの背面にタップ（iPhone: 上部）
4. 確認を待つ

⚠️ カードを磁気から遠ざけて！""",
        "ko": """**NFC 카드**:

💳 MMEETT는 NFC 카드로 활성화
📱 카드 작성하려면 NFC 켜야 함

사용법:
1. Me → Activate MMEETT Device
2. 카드 타입 선택
3. 카드를 스마트폰 뒷면에 탭 (iPhone: 상단)
4. 확인 대기

⚠️ 카드를 자석에서 멀리!""",
    },
    "COMPATIBILITY": {
        "zh": """**手机兼容性**：

📱 **iOS**: 12.0+（iPhone 6s 及以上）
🤖 **Android**: 6.0+（需支持 NFC）

💡 推荐：
• iOS 15+ 性能最佳
• Android 10+ 带 NFC

检查手机设置中的 NFC！""",
        "ms": """**Phone Compatibility**:

📱 **iOS**: 12.0+ (iPhone 6s dan ke atas)
🤖 **Android**: 6.0+ (dengan NFC support)

💡 recommended:
• iOS 15+ untuk performance terbaik
• Android 10+ dengan NFC

check phone settings kau untuk NFC!""",
        "id": """**Kompatibilitas Phone**:

📱 **iOS**: 12.0+ (iPhone 6s ke atas)
🤖 **Android**: 6.0+ (dengan dukungan NFC)

💡 rekomendasi:
• iOS 15+ untuk performa terbaik
• Android 10+ dengan NFC

cek pengaturan phone kamu untuk NFC!""",
        "th": """**ความเข้ากันได้ของโทรศัพท์**:

📱 **iOS**: 12.0+ (iPhone 6s ขึ้นไป)
🤖 **Android**: 6.0+ (รองรับ NFC)

💡 แนะนำ:
• iOS 15+ เพื่อประสิทธิภาพสูงสุด
• Android 10+ พร้อม NFC

เช็ค NFC ในการตั้งค่าโทรศัพท์!""",
        "vi": """**Tương thích điện thoại**:

📱 **iOS**: 12.0+ (iPhone 6s trở lên)
🤖 **Android**: 6.0+ (có hỗ trợ NFC)

💡 khuyên dùng:
• iOS 15+ cho hiệu năng tốt nhất
• Android 10+ có NFC

kiểm tra NFC trong cài đặt phone!""",
        "tl": """**Phone Compatibility**:

📱 **iOS**: 12.0+ (iPhone 6s at mas bago)
🤖 **Android**: 6.0+ (may NFC support)

💡 recommended:
• iOS 15+ para sa best performance
• Android 10+ na may NFC

i-check ang phone settings mo para sa NFC!""",
        "ja": """**スマホ互換性**:

📱 **iOS**: 12.0+（iPhone 6s以降）
🤖 **Android**: 6.0+（NFC対応必須）

💡 おすすめ:
• iOS 15+ で最高パフォーマンス
• Android 10+ NFC付き

設定でNFCをチェックしてね！""",
        "ko": """**스마트폰 호환성**:

📱 **iOS**: 12.0+ (iPhone 6s 이상)
🤖 **Android**: 6.0+ (NFC 지원 필수)

💡 추천:
• iOS 15+ 최고 성능
• Android 10+ NFC 탑재

설정에서 NFC 확인해줘!""",
    },
    "PRIVACY": {
        "zh": """**隐私与安全**：

🔒 录音存储在设备本地
🔒 同步使用加密连接
🔒 除非你选择，否则没有云存储

MMEETT 优先保护你的数据隐私！

💡 提示：敏感内容同步后删除录音""",
        "ms": """**Privacy & Security**:

🔒 recording disimpan locally kat device
🔒 sync guna encrypted connection
🔒 tak ada cloud storage melainkan kau pilih

MMEETT utamakan privasi data kau!

💡 tip: delete recording lepas sync kalau sensitif""",
        "id": """**Privasi & Keamanan**:

🔒 rekaman disimpan lokal di device
🔒 sync menggunakan koneksi terenkripsi
🔒 tidak ada cloud storage kecuali kamu pilih

MMEETT mengutamakan privasi data kamu!

💡 tip: hapus rekaman setelah sync jika sensitif""",
        "th": """**ความเป็นส่วนตัวและความปลอดภัย**:

🔒 บันทึกเสียงเก็บในอุปกรณ์
🔒 ซิงค์ใช้การเชื่อมต่อแบบเข้ารหัส
🔒 ไม่มี cloud storage เว้นแต่คุณเลือก

MMEETT ให้ความสำคัญกับความเป็นส่วนตัวของข้อมูล!

💡 เคล็ดลับ: ลบบันทึกหลังซิงค์หากเป็นเรื่องละเอียดอ่อน""",
        "vi": """**Quyền riêng tư & Bảo mật**:

🔒 ghi âm lưu cục bộ trên thiết bị
🔒 sync dùng kết nối mã hóa
🔒 không có cloud storage trừ khi bạn chọn

MMEETT ưu tiên quyền riêng tư dữ liệu của bạn!

💡 mẹo: xóa ghi âm sau sync nếu nội dung nhạy cảm""",
        "tl": """**Privacy & Security**:

🔒 recordings naka-store locally sa device
🔒 sync ay gumagamit ng encrypted connection
🔒 walang cloud storage maliban kung pipiliin mo

MMEETT pinapahalagahan ang data privacy mo!

💡 tip: i-delete ang recordings pagkatapos ng sync kung sensitive""",
        "ja": """**プライバシーとセキュリティ**:

🔒 録音はデバイスにローカル保存
🔒 同期は暗号化接続を使用
🔒 クラウド保存は選択した場合のみ

MMEETTはデータプライバシーを最優先！

💡 ヒント：機密内容は同期後に録音を削除してね""",
        "ko": """**개인정보 & 보안**:

🔒 녹음은 기기에 로컬 저장
🔒 동기화는 암호화 연결 사용
🔒 클라우드 저장은 선택 시에만

MMEETT는 데이터 프라이버시를 최우선!

💡 팁: 민감한 내용은 동기화 후 녹음 삭제""",
    },
    "TROUBLESHOOTING": {
        "zh": """**快速排障**：

🔋 设备开不了？→ 先充满电
📱 连不上？→ 重启手机蓝牙
🔄 同步失败？→ 用 WiFi 代替蓝牙
🎙️ 没有录音？→ 检查 MEETING 开关位置
💳 NFC 不行？→ 在手机设置中开启

还是不行？tag @ukkbasf！😇""",
        "ms": """**Quick Troubleshooting**:

🔋 device tak boleh on? → charge penuh dulu
📱 tak boleh connect? → restart bluetooth kat phone
🔄 sync gagal? → guna WiFi ganti bluetooth
🎙️ tak record? → check position switch MEETING
💳 NFC tak jadi? → on dalam phone settings

masih tak boleh? tag @ukkbasf! 😇""",
        "id": """**Quick Troubleshooting**:

🔋 device tidak bisa nyala? → charge penuh dulu
📱 tidak bisa connect? → restart bluetooth di phone
🔄 sync gagal? → guna WiFi daripada bluetooth
🎙️ tidak merekam? → cek posisi switch MEETING
💳 NFC tidak berfungsi? → aktifkan di pengaturan phone

masih bermasalah? tag @ukkbasf! 😇""",
        "th": """**แก้ปัญหาเบื้องต้น**:

🔋 อุปกรณ์เปิดไม่ติด? → ชาร์จให้เต็มก่อน
📱 เชื่อมต่อไม่ได้? → รีสตาร์ท bluetooth บนโทรศัพท์
🔄 ซิงค์ไม่สำเร็จ? → ใช้ WiFi แทน bluetooth
🎙️ ไม่บันทึก? → เช็คตำแหน่งสวิตช์ MEETING
💳 NFC ไม่ทำงาน? → เปิดในการตั้งค่าโทรศัพท์

ยังไม่ได้? tag @ukkbasf! 😇""",
        "vi": """**Khắc phục sự cố nhanh**:

🔋 thiết bị không mở được? → charge đầy trước
📱 không kết nối được? → khởi động lại bluetooth
🔄 sync thất bại? → dùng WiFi thay bluetooth
🎙️ không ghi âm? → kiểm tra vị trí công tắc MEETING
💳 NFC không hoạt động? → bật trong cài đặt phone

vẫn không được? tag @ukkbasf! 😇""",
        "tl": """**Quick Troubleshooting**:

🔋 device ayaw mag-on? → i-charge ng full muna
📱 ayaw mag-connect? → i-restart ang bluetooth sa phone
🔄 sync ayaw? → gumamit ng WiFi imbes na bluetooth
🎙️ walang recording? → i-check ang MEETING switch position
💳 NFC ayaw? → i-enable sa phone settings

pa rin ayaw? tag @ukkbasf! 😇""",
        "ja": """**クイックトラブルシューティング**:

🔋 デバイスがつかない？→ まずフル充電
📱 接続できない？→ Bluetoothを再起動
🔄 同期失敗？→ Bluetoothの代わりにWiFiを使う
🎙️ 録音できない？→ MEETINGスイッチの位置を確認
💳 NFCが動かない？→ 設定でNFCをオンに

それでもダメ？@ukkbasfにタグしてね！😇""",
        "ko": """**빠른 문제 해결**:

🔋 기기가 안 켜져? → 먼저 완충
📱 연결이 안 돼? → 블루투스 재시작
🔄 동기화 실패? → 블루투스 대신 WiFi 사용
🎙️ 녹음이 안 돼? → MEETING 스위치 위치 확인
💳 NFC가 안 돼? → 설정에서 NFC 켜기

그래도 안 돼? @ukkbasf 태그해줘! 😇""",
    },
    "SUBSCRIPTION": {
        "zh": """**订阅信息**：

💳 一次性购买（没有月费！）
🎉 MMEETT 设备=买一次，永久拥有

可选：
• 算力套餐（定期）
• 高级 AI 功能（如有）

没有隐藏订阅！😇""",
        "ms": """**Subscription Info**:

💳 beli sekali (tak ada yuran bulanan!)
🎉 device MMEETT = beli sekali, punya selamanya

optional:
• computing power packages (berulang)
• premium AI features (kalau ada)

tak ada subscription tersembunyi! 😇""",
        "id": """**Info Langganan**:

💳 beli sekali (tidak ada biaya bulanan!)
🎉 perangkat MMEETT = beli sekali, milik selamanya

opsional:
• paket computing power (berlangganan)
• fitur AI premium (jika ada)

tidak ada langganan tersembunyi! 😇""",
        "th": """**ข้อมูลการสมัครสมาชิก**:

💳 ซื้อครั้งเดียว (ไม่มีค่ารายเดือน!)
🎉 อุปกรณ์ MMEETT = ซื้อครั้งเดียว เป็นของคุณตลอด

ตัวเลือก:
• แพ็กเกจ computing power (ต่ออายุ)
• ฟีเจอร์ AI พรีเมียม (ถ้ามี)

ไม่มีการสมัครสมาชิกแบบซ่อนเร้น! 😇""",
        "vi": """**Thông tin đăng ký**:

💳 mua một lần (không phí hàng tháng!)
🎉 thiết bị MMEETT = mua một lần, sở hữu vĩnh viễn

tùy chọn:
• gói computing power (định kỳ)
• tính năng AI cao cấp (nếu có)

không có đăng ký ẩn! 😇""",
        "tl": """**Subscription Info**:

💳 one-time purchase (walang monthly fees!)
🎉 MMEETT device = bilhin minsan, sa'yo na forever

optional:
• computing power packages (recurring)
• premium AI features (kung available)

walang hidden subscriptions! 😇""",
        "ja": """**サブスクリプション情報**:

💳 一度きりの購入（月額なし！）
🎉 MMEETTデバイス = 買えばずっと使える

オプション:
• コンピューティングパワーパッケージ（定期）
• プレミアムAI機能（利用可能な場合）

隠れたサブスクなし！😇""",
        "ko": """**구독 정보**:

💳 1회 구매 (월간 요금 없음!)
🎉 MMEETT 기기 = 한 번 사면 영구 소유

선택 사항:
• 컴퓨팅 파워 패키지 (정기)
• 프리미엄 AI 기능 (가능한 경우)

숨겨진 구독 없음! 😇""",
    },
    "AFFILIATE_TRACKING": {
        "zh": """**联盟追踪**：

🔗 app 中有专属推荐链接
📊 实时仪表板：
   • 直接推荐
   • 团队结构
   • 收入明细

💡 分享你的链接=自动追踪！

查看：我 → 会员 → 我的团队""",
        "ms": """**Affiliate Tracking**:

🔗 link referral unik dalam app
📊 dashboard real-time:
   • direct referrals
   • team structure
   • earnings breakdown

💡 share link kau = auto tracking!

check: Me → Member → My Team""",
        "id": """**Affiliate Tracking**:

🔗 link referral unik di app
📊 dashboard real-time:
   • direct referrals
   • struktur tim
   • rincian penghasilan

💡 bagikan link kamu = auto tracking!

cek: Me → Member → My Team""",
        "th": """**Affiliate Tracking**:

🔗 ลิงก์แนะนำเฉพาะในแอป
📊 แดชบอร์ดแบบเรียลไทม์:
   • แนะนำโดยตรง
   • โครงสร้างทีม
   • รายละเอียดรายได้

💡 แชร์ลิงก์ของคุณ = ติดตามอัตโนมัติ!

เช็ค: Me → Member → My Team""",
        "vi": """**Affiliate Tracking**:

🔗 link giới thiệu riêng trong app
📊 bảng điều khiển real-time:
   • giới thiệu trực tiếp
   • cấu trúc team
   • chi tiết thu nhập

💡 chia sẻ link của bạn = tự động theo dõi!

xem: Me → Member → My Team""",
        "tl": """**Affiliate Tracking**:

🔗 unique referral link sa app
📊 real-time dashboard:
   • direct referrals
   • team structure
   • earnings breakdown

💡 i-share ang link mo = auto tracking!

check: Me → Member → My Team""",
        "ja": """**アフィリエイト追跡**:

🔗 アプリに固有の紹介リンク
📊 リアルタイムダッシュボード:
   • 直接紹介
   • チーム構造
   • 収益内訳

💡 リンクをシェア = 自動追跡！

チェック: Me → Member → My Team""",
        "ko": """**제휴 추적**:

🔗 앱에 전용 추천 링크
📊 실시간 대시보드:
   • 직접 추천
   • 팀 구조
   • 수익 내역

💡 링크 공유 = 자동 추적!

확인: Me → Member → My Team""",
    },
}

# ============================================
# FORWARD TRIGGERS & FRUSTRATION DETECTION
# ============================================

FORWARD_TRIGGERS = [
    "bug", "crash", "error", "broken", "not working", "issue", "problem",
    "complaint", "angry", "unhappy", "scam", "fraud",
    "legal", "lawyer", "sue", "report",
]

FRUSTRATION_INDICATORS = [
    r"!{2,}",       # multiple exclamation marks
    r"\?\?+",        # multiple question marks
    r"[A-Z]{5,}",    # all caps (5+ chars)
]

# ============================================
# FALLBACK MESSAGES (varied, some with help list, some without)
# ============================================

FALLBACK_MESSAGES = [
    "hmm that's a good one 🤔\n\nbut i CAN help with:\n• charging & battery 🔋\n• app download & setup 📱\n• device activation 🔗\n• recording features 🎙️\n• sync & transfer 🔄\n• transcription 📝\n• AI chat 🤖\n• shipping 📦\n• returns & warranty 🔄\n• packages & pricing 💰\n• commissions & bonuses 💸\n\nor check the full FAQ: {faq_link}\n\nneed human help? @{admin_username} can assist! 😇",
    "tbh i don't have that answer yet! 😅\n\ntry asking about our packages, commissions, device setup, or shipping — i'm pretty good with those!\n\nfull FAQ: {faq_link}\n@{admin_username} can help if i can't!",
    "oh interesting question! let me think...\n\nyeah i don't have info on that one yet, but i can help with MMEETT stuff like pricing, recording, activation, etc.\n\ncheck the FAQ tab for more: {faq_link}\nor @{admin_username} might know! 😇",
    "hmm not sure about that one 🤔\n\ni'm ur go-to for MMEETT questions though! packages, device help, shipping, bonuses — just ask.\n\nFAQ: {faq_link} | human help: @{admin_username}",
    "good question but that's outside my knowledge for now 😅\n\ni handle MMEETT stuff — try me with something about the device, app, packages, or earnings!\n\nstill stuck? @{admin_username} or {faq_link}",
    "eh i wish i knew that one! 🥲\n\nbut for MMEETT-related stuff i got u. just ask about our tiers, device features, commissions, etc.\n\n@{admin_username} can help with the rest, or check {faq_link}",
]

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_topic_id(message):
    """Extract topic ID from message"""
    if hasattr(message, 'message_thread_id'):
        return message.message_thread_id
    return None

def get_time_greeting():
    """Get a greeting based on current time"""
    hour = time.localtime().tm_hour
    if 5 <= hour < 12:
        return random.choice(TIME_GREETINGS["morning"])
    elif 12 <= hour < 18:
        return random.choice(TIME_GREETINGS["afternoon"])
    elif 18 <= hour < 23:
        return random.choice(TIME_GREETINGS["evening"])
    else:
        return random.choice(TIME_GREETINGS["night"])

def get_opener():
    """Get a random conversational opener (50% chance)"""
    if random.random() < 0.5:
        return random.choice(CONVERSATIONAL_OPENERS)
    return None

def get_closer():
    """Get a random conversational closer (50% chance)"""
    if random.random() < 0.5:
        return random.choice(CONVERSATIONAL_CLOSERS)
    return None

def get_small_talk(text):
    """Check if message is small talk, return response or None"""
    lower = text.lower().strip()
    # Remove trailing punctuation for matching
    clean = re.sub(r'[!?.]+$', '', lower)

    for category, data in SMALL_TALK.items():
        for trigger in data["triggers"]:
            if clean == trigger or clean.startswith(trigger + " "):
                return random.choice(data["responses"])
    return None

def match_question(text):
    """Match question against FAQ database using word boundaries, return random variant"""
    lower_text = text.lower()

    for category, data in FAQ_DATABASE.items():
        for keyword in data["keywords"]:
            kw = keyword.lower()
            if re.search(r'\b' + re.escape(kw) + r'\b', lower_text):
                response = random.choice(data["responses"])
                return {"category": category, "response": response}

    return None

def should_forward_to_human(text):
    """Check if question should be forwarded to admin"""
    lower_text = text.lower()
    return any(trigger in lower_text for trigger in FORWARD_TRIGGERS)

def detect_frustration(text):
    """Detect frustration indicators in message"""
    for pattern in FRUSTRATION_INDICATORS:
        if re.search(pattern, text):
            return True
    return False

def escape_markdown(text):
    """Escape markdown special characters in user-generated text"""
    special_chars = r"_*[]()"
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text

def detect_language(text):
    """Detect language from text - returns en/zh/th/vi/tl/id/ms/ja/ko"""
    text_lower = text.lower()
    
    # Chinese detection (simplified/traditional characters)
    chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    if chinese_chars >= 2:
        return 'zh'
    
    # Japanese detection (hiragana/katakana)
    japanese_chars = sum(1 for char in text if '\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff')
    if japanese_chars >= 2:
        return 'ja'
    
    # Korean detection (hangul)
    korean_chars = sum(1 for char in text if '\uac00' <= char <= '\ud7af')
    if korean_chars >= 2:
        return 'ko'
    
    # Thai detection (Thai script range)
    thai_chars = sum(1 for char in text if '\u0e00' <= char <= '\u0e7f')
    if thai_chars >= 2:
        return 'th'
    
    # Vietnamese detection (with diacritics)
    vietnamese_patterns = ['à', 'á', 'ả', 'ã', 'ạ', 'ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 
                          'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ề', 'ế', 'ể', 'ễ', 'ệ',
                          'ì', 'í', 'ỉ', 'ĩ', 'ị',
                          'ò', 'ó', 'ỏ', 'õ', 'ọ', 'ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ',
                          'ù', 'ú', 'ủ', 'ũ', 'ụ', 'ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự',
                          'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'đ']
    if any(pattern in text_lower for pattern in vietnamese_patterns):
        return 'vi'
    
    # Tagalog detection (common words)
    tagalog_words = ['kumusta', 'salamat', 'paano', 'ano', 'bakit', 'kailan', 'saan', 'sino', 'alin', 'gaano',
                    'meron', 'wala', 'tayo', 'kami', 'sila', 'ako', 'ka', 'siya', 'natin', 'namin']
    if any(word in text_lower for word in tagalog_words):
        return 'tl'
    
    # Indonesian/Malay detection (common words)
    indo_malay_words = ['saya', 'anda', 'kamu', 'apa', 'bagaimana', 'kenapa', 'dimana', 'kapan', 'siapa',
                       'terima', 'kasih', 'tolong', 'bisa', 'tidak', 'dengan', 'untuk', 'dari', 'yang']
    if any(word in text_lower for word in indo_malay_words):
        # Distinguish between id and ms (simplified)
        return 'id' if 'tidak' in text_lower or 'saya' in text_lower else 'ms'
    
    # Default to English
    return 'en'

def send_typing_indicator(chat_id, topic_id, seconds=3):
    """Send typing indicator for specified duration"""
    try:
        bot.send_chat_action(chat_id, "typing", message_thread_id=topic_id)
        time.sleep(seconds)
    except Exception as e:
        print(f"❌ Error sending typing indicator: {e}")

def send_with_typing(chat_id, text, reply_to=None, topic_id=None):
    """Send message with typing indicator and natural delay"""
    try:
        # Show typing indicator
        bot.send_chat_action(chat_id, "typing")

        # Random delay 1-3 seconds to feel natural
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)

        kwargs = {"parse_mode": "Markdown"}
        if reply_to:
            kwargs["reply_to_message_id"] = reply_to
        if topic_id:
            kwargs["message_thread_id"] = topic_id

        bot.send_message(chat_id, text, **kwargs)
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def get_conversational_fallback():
    """Get a random fallback message"""
    template = random.choice(FALLBACK_MESSAGES)
    return template.format(faq_link=FAQ_LINK, admin_username=ADMIN_USERNAME)

# Apology messages when translation is unavailable (per language)
APOLOGY_MESSAGES = {
    "zh": [
        "抱歉啊，我的中文还不太行😅 让我用英文回复你吧~\n\n",
        "哎呀，中文这块我还得多练练😂 先用英文回答你哈~\n\n",
        "不好意思，我的中文还不够好😅 这次先用英文回答你吧~\n\n",
    ],
    "ms": [
        "sorry ah, bahasa Melayu aku tak berapa kuat lagi 😅 jawab dalam English dulu ye~\n\n",
        "ampun, BM aku masih belajar ni 😂 bagi aku jawab dalam English dulu~\n\n",
        "maaf, bahasa Melayu aku tak berapa lancar lagi 😅 jawap dalam English dulu leh~\n\n",
    ],
    "id": [
        "maaf ya, bahasa Indonesia aku belum terlalu lancar 😅 aku jawab pakai English dulu ya~\n\n",
        "sorry, Indo aku masih belajar nih 😂 jawab pakai English dulu ya~\n\n",
        "ampun, bahasa Indonesia aku belum oke banget 😅 aku jawab English dulu ya~\n\n",
    ],
    "th": [
        "ขอโทษนะ ภาษาไทยฉันยังไม่ค่อยแข็งแรง 😅 ขอตอบเป็นภาษาอังกฤษก่อนนะ~\n\n",
        "เอ่อ ภาษาไทยฉันยังต้องฝึกอีก 😂 ขอตอบเป็นอังกฤษก่อนจ้ะ~\n\n",
        "ขอโทษจ้ะ ภาษาไทยฉันยังไม่ค่อยเก่ง 😅 ตอบเป็นอังกฤษก่อนน่ะ~\n\n",
    ],
    "vi": [
        "xin lỗi nha, tiếng Việt mình chưa được tốt lắm 😅 để mình trả lời bằng tiếng Anh nhé~\n\n",
        "sorry, tiếng Việt mình còn đang học 😂 trả lời bằng tiếng Anh trước nha~\n\n",
        "mình xin lỗi, tiếng Việt mình chưa giỏi lắm 😅 trả lời bằng English trước nha~\n\n",
    ],
    "tl": [
        "sorry, Tagalog ko medyo mahina pa 😅 sagot muna ako sa English ha~\n\n",
        "pasensya na, Filipino ko hindi pa ganun kagaling 😂 English muna sagot ko~\n\n",
        "sorry po, Tagalog ko medyo struggling 😅 English muna sagot ko ha~\n\n",
    ],
    "ja": [
        "すみません、日本語がまだあまり上手じゃないんです😅 とりあえず英語で返信させてくださいね~\n\n",
        "あー、日本語はもうちょっと練習が必要です😂 まずは英語で回答しますね~\n\n",
        "ごめんなさい、日本語がまだ完璧じゃないんです😅 今回は英語でお答えしますね~\n\n",
    ],
    "ko": [
        "죄송해요, 한국어가 아직 많이 부족해요 😅 일단 영어로 답변할게요~\n\n",
        "아직 한국어가 좀 서툴러서😂 일단 영어로 대답할게요~\n\n",
        "미안해요, 한국어가 아직 완벽하지 않아요 😅 이번엔 영어로 답변드릴게요~\n\n",
    ],
}

def get_response(category, language):
    """Get FAQ response in detected language, fallback to English with apology"""
    if language == 'en':
        # Return random variant from FAQ_DATABASE
        return random.choice(FAQ_DATABASE[category]["responses"])
    elif language in FAQ_TRANSLATIONS.get(category, {}):
        return FAQ_TRANSLATIONS[category][language]
    else:
        # Fallback to English with a language-appropriate apology
        apology = random.choice(APOLOGY_MESSAGES.get(language, ["sorry, let me reply in English 😅\n\n"]))
        english_response = random.choice(FAQ_DATABASE[category]["responses"])
        return apology + english_response

def get_welcome_message(user_name):
    """Generate welcome message from variants"""
    return random.choice(WELCOME_MESSAGES)(user_name)

# ============================================
# MULTILINGUAL WELCOME MESSAGES
# ============================================

WELCOME_TRANSLATIONS = {
    "zh": [
        lambda name: f"""
嘿 {name}，欢迎加入 MMEETT X 1% Club！⚡️

很高兴你来啦！这里是每个板块的用途：

☕️ General Chat — 聊天、自我介绍、认识其他成员
📢 Announcement — 公司更新、zoom链接、官方消息
📂 The Vault — 按语言分类的PDF资源（中、英、越、泰、印尼、他加禄）
🎬 Resources — 视频格式资源和培训材料
🛠 Learn & Master MMEETT — 循序渐进教程（视频+指南）
❓ FAQ — 有问题？在这里问！我会尽快回答

🌐 我会说9种语言！English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — 用你最舒服的语言问就好！

💡 新人第一步：
1. 去Tutorial板块看购买MMEETT套餐的视频
2. 有问题？在FAQ板块提问，我在那里帮你！
3. 想邀请朋友？在FAQ板块输入"invite"，我帮你写邀请消息！

让我们一起重新定义连接方式 🚀 有任何需要随时找我！😇
""",
    ],
    "ms": [
        lambda name: f"""
hey {name}, selamat datang ke MMEETT X 1% Club! ⚡️

gembira sangat kau join!

ni panduan supaya kau tak sesat:

☕️ General Chat — lepak, introduce diri, kenal member lain
📢 Announcement — update company, link zoom, berita rasmi
📂 The Vault — PDF ikut bahasa (CN, EN, VI, TH, ID, TL)
🎬 Resources — video & bahan latihan
🛠 Learn & Master MMEETT — tutorial langkah demi langkah
❓ FAQ — ada soalan? tanya sini! aku jawab cepat

🌐 aku boleh cakap 9 bahasa! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — tanya je dalam bahasa yang kau selesa!

💡 langkah pertama kalau baru:
1. check Tutorial tab untuk video beli pakej MMEETT
2. ada soalan? drop kat FAQ tab — aku ada untuk bantu!
3. nak invite kawan? taip "invite" kat FAQ tab, aku bantu tulis mesej!

jom redefine cara dunia connect 🚀 apa-apa pun, holler aja! 😇
""",
    ],
    "id": [
        lambda name: f"""
hey {name}, selamat datang di MMEETT X 1% Club! ⚡️

seneng banget kamu join!

biar nggak bingung, ini panduannya:

☕️ General Chat — ngobrol, kenalan, connect sama member lain
📢 Announcement — update perusahaan, link zoom, berita resmi
📂 The Vault — PDF per bahasa (CN, EN, VI, TH, ID, TL)
🎬 Resources — video & materi pelatihan
🛠 Learn & Master MMEETT — tutorial langkah demi langkah
❓ FAQ — ada pertanyaan? tanya di sini! aku jawab ASAP

🌐 aku bisa ngobrol dalam 9 bahasa! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — tanya aja pakai bahasa yang kamu paling nyaman!

💡 langkah pertama kalau baru:
1. cek Tutorial tab buat video beli paket MMEETT
2. ada pertanyaan? drop di FAQ tab — aku ada buat bantu!
3. mau invite temen? ketik "invite" di FAQ tab, aku bantu tulis pesannya!

mari redefine cara dunia connect 🚀 kailangan mo kahit ano, holler lang! 😇
""",
    ],
    "th": [
        lambda name: f"""
สวัสดี {name} ยินดีต้อนรับสู่ MMEETT X 1% Club! ⚡️

ดีใจมากที่คุณมาร่วมกับเรา!

นี่คือคู่มือเพื่อไม่ให้หลงทาง:

☕️ General Chat — พูดคุย แนะนำตัว รู้จักเพื่อนใหม่
📢 Announcement — ข่าวสารบริษัท ลิงก์ zoom ประกาศทางการ
📂 The Vault — PDF จัดตามภาษา (CN, EN, VI, TH, ID, TL)
🎬 Resources — วิดีโอและสื่อการฝึกอบรม
🛠 Learn & Master MMEETT — สอนทีละขั้นตอน (วิดีโอ+คู่มือ)
❓ FAQ — มีคำถาม? ถามได้เลย! ฉันจะตอบให้เร็วที่สุด

🌐 ฉันพูดได้ 9 ภาษา! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — ถามเป็นภาษาที่คุณสบายใจได้เลยจ้ะ!

💡 สำหรับมือใหม่:
1. ดูวิดีโอสอนซื้อแพ็กเกจ MMEETT ที่ Tutorial tab
2. มีคำถาม? ถามที่ FAQ tab — ฉันอยู่ช่วย!
3. อยากชวนเพื่อน? กล่อง "invite" ที่ FAQ tab ฉันจะช่วยเขียนข้อความให้!

มาร่วมกัน re-define วิธีการเชื่อมต่อของโลก 🚀 ต้องการอะไรบอกได้เลยจ้ะ! 😇
""",
    ],
    "vi": [
        lambda name: f"""
chào {name}, chào mừng đến với MMEETT X 1% Club! ⚡️

rất vui bạn đã tham gia!

đây là hướng dẫn để bạn không bị lạc:

☕️ General Chat — trò chuyện, giới thiệu, kết bạn
📢 Announcement — cập nhật công ty, link zoom, tin tức chính thức
📂 The Vault — PDF theo ngôn ngữ (CN, EN, VI, TH, ID, TL)
🎬 Resources — video và tài liệu đào tạo
🛠 Learn & Master MMEETT — hướng dẫn từng bước (video + hướng dẫn)
❓ FAQ — có câu hỏi? hỏi ở đây! mình sẽ trả lời nhanh nhất

🌐 mình nói được 9 ngôn ngữ! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — cứ hỏi bằng ngôn ngữ bạn thoải mái nhất nhé!

💡 bước đầu cho người mới:
1. xem video hướng dẫn mua gói MMEETT ở Tutorial tab
2. có câu hỏi? hỏi ở FAQ tab — mình luôn ở đó giúp bạn!
3. muốn mời bạn bè? gõ "invite" ở FAQ tab, mình sẽ viết tin nhắn giúp bạn!

cùng nhau tái định nghĩa cách thế giới kết nối 🚀 cần gì cứ nhắn mình nhé! 😇
""",
    ],
    "tl": [
        lambda name: f"""
hey {name}, maligayang pagdating sa MMEETT X 1% Club! ⚡️

saya na-sumali ka!

ito ang guide para di ka mawala:

☕️ General Chat — mag-usap, mag-introduce, makipag-connect
📢 Announcement — company updates, zoom links, opisyal na balita
📂 The Vault — PDFs per wika (CN, EN, VI, TH, ID, TL)
🎬 Resources — video at training materials
🛠 Learn & Master MMEETT — step-by-step tutorials (videos + guides)
❓ FAQ — may tanong? itanong dito! sasagot ako ASAP

🌐 nakakapagsalita ako ng 9 wika! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — tanungin mo sa wika na pinakakomportable ka!

💡 unang hakbang para sa bagong member:
1. panoorin ang tutorial video sa pagbili ng MMEETT package sa Tutorial tab
2. may tanong? i-drop sa FAQ tab — nandoon ako para tumulong!
3. gusto mag-invite ng friends? mag-type ng "invite" sa FAQ tab, gagawan ko ng message!

sama-sama nating i-redefine kung paano nagko-connect ang mundo 🚀 kailangan mo kahit ano, holler lang! 😇
""",
    ],
    "ja": [
        lambda name: f"""
{name}さん、MMEETT X 1% Clubへようこそ！⚡️

参加してくれてありがとう！

迷わないように、各タブの説明：

☕️ General Chat — 交流、自己紹介、メンバーとつながる
📢 Announcement — 会社の更新、Zoomリンク、公式ニュース
📂 The Vault — 言語別PDFリソース（CN, EN, VI, TH, ID, TL）
🎬 Resources — 動画リソースとトレーニング教材
🛠 Learn & Master MMEETT — ステップバイステップチュートリアル
❓ FAQ — 質問はここに！できるだけ早く答えるよ

🌐 9言語対応！English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — 楽な言語で聞いてね！

💡 初めての方へ:
1. TutorialタブでMMEETTパッケージ購入動画を見よう
2. 質問があればFAQタブにドロップ — いつでも助けるよ！
3. 友達を招待したい？FAQタブで「invite」と入力してね！

一緒に世界のつながり方を変えよう 🚀 何かあれば気軽に！😇
""",
    ],
    "ko": [
        lambda name: f"""
{name}님, MMEETT X 1% Club에 오신 걸 환영해! ⚡️

정말 반가워!

헤매지 않도록 각 탭 설명:

☕️ General Chat — 수다 떨기, 자기소개, 멤버들이랑 연결
📢 Announcement — 회사 업데이트, 줌 링크, 공식 뉴스
📂 The Vault — 언어별 PDF 리소스 (CN, EN, VI, TH, ID, TL)
🎬 Resources — 비디오 리소스 & 트레이닝 자료
🛠 Learn & Master MMEETT — 단계별 튜토리얼
❓ FAQ — 질문 있으면 여기서 물어봐! 최대한 빨리 답할게

🌐 9개 언어 지원! English · 中文 · Bahasa Melayu · Bahasa Indonesia · ไทย · Tiếng Việt · Tagalog · 日本語 · 한국어 — 편한 언어로 물어봐!

💡 처음이면 이렇게:
1. Tutorial 탭에서 MMEETT 패키지 구매 영상 보기
2. 질문 있으면 FAQ 탭에 남겨 — 항상 도와줄게!
3. 친구 초대하고 싶으면? FAQ 탭에서 "invite" 입력해!

함께 세상의 연결 방식을 바꿔보자 🚀 뭐든 필요하면 불러줘! 😇
""",
    ],
}

# Phone country code to language mapping
PHONE_CODE_TO_LANGUAGE = {
    "+86": "zh",    # China
    "+852": "zh",   # Hong Kong
    "+853": "zh",   # Macau
    "+886": "zh",   # Taiwan
    "+60": "ms",    # Malaysia
    "+62": "id",    # Indonesia
    "+66": "th",    # Thailand
    "+84": "vi",    # Vietnam
    "+63": "tl",    # Philippines
    "+65": "en",    # Singapore
    "+1": "en",     # USA/Canada
    "+44": "en",    # UK
    "+61": "en",    # Australia
    "+855": "km",   # Cambodia
    "+856": "lo",   # Laos
    "+95": "my",    # Myanmar
    "+91": "hi",    # India
    "+82": "ko",    # Korea
    "+81": "ja",    # Japan
}

def detect_language_from_phone(phone_number):
    """Detect language from phone country code. Returns language code or None."""
    if not phone_number:
        return None
    for code, lang in PHONE_CODE_TO_LANGUAGE.items():
        if phone_number.startswith(code):
            return lang
    return None

def send_welcome_message(chat_id, topic_id, user_name, language='en'):
    """Send welcome message to new member in General Chat only, in detected language"""
    try:
        bot.send_chat_action(chat_id, "typing")
        time.sleep(random.uniform(1.0, 2.0))

        # Try to get translated welcome if language is available
        if language != 'en' and language in WELCOME_TRANSLATIONS:
            welcome_text = random.choice(WELCOME_TRANSLATIONS[language])(user_name)
        else:
            welcome_text = random.choice(WELCOME_MESSAGES)(user_name)

        bot.send_message(
            chat_id,
            welcome_text,
            parse_mode="Markdown",
            message_thread_id=topic_id
        )
        print(f"✅ Welcome message sent to {user_name} in {language}")
    except Exception as e:
        print(f"❌ Error sending welcome message: {e}")

# ============================================
# BOT HANDLERS
# ============================================

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    """Handle /start and /help commands"""
    responses = [
        f"""{get_time_greeting()} i'm Vanessa, ur MMEETT guide 😇

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
or check the full FAQ: {FAQ_LINK}

need human help? @{ADMIN_USERNAME} can assist!""",
        f"""hey there! 😇 Vanessa here, ur go-to for all things MMEETT.

got questions? i cover:
📱 app setup | 🔋 charging | 🔗 device activation
🎙️ recording | 🔄 sync | 📝 transcription
🤖 AI chat | 📦 shipping | 🔄 returns
💰 packages | 💸 commissions & bonuses

drop ur question in the FAQ tab and i'll get back to u ASAP!
FAQ: {FAQ_LINK} | human help: @{ADMIN_USERNAME}""",
        f"""hi! Vanessa here 😇

i'm here to help with MMEETT stuff — from packages and pricing to device setup and troubleshooting.

just type ur question in the FAQ tab and i'll answer!

quick links:
- full FAQ: {FAQ_LINK}
- need a human? @{ADMIN_USERNAME} got u""",
    ]

    try:
        bot.send_chat_action(message.chat.id, "typing")
        time.sleep(random.uniform(0.5, 1.5))
        bot.reply_to(message, random.choice(responses), parse_mode="Markdown")
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
        if new_user.username:
            user_name = f"@{new_user.username}"
        else:
            user_name = new_user.first_name

        # Try to detect language from phone number (if available)
        # Note: Telegram only shares phone_number if user has shared it via contact
        # In group joins, phone_number is usually None — fallback to English
        phone_number = getattr(new_user, 'phone_number', None)
        language = detect_language_from_phone(phone_number) or 'en'

        print(f"👋 New member joined: {user_name} (lang: {language})")

        # Send welcome message in detected language
        send_welcome_message(chat_id, topic_id, user_name, language)

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
    if message.from_user.username:
        from_user = f"@{message.from_user.username}"
    else:
        from_user = message.from_user.first_name

    print(f"📨 Message in Topic {topic_id} from {from_user}: {text[:50]}...")

    # ============================================
    # RULE: Only reply in FAQ topic (Topic 9)
    # ============================================
    if topic_id != FAQ_ID:
        return

    chat_id = message.chat.id

    # Detect language FIRST
    language = detect_language(text)
    print(f"🌐 Detected language: {language}")

    # Send typing indicator (3 seconds)
    send_typing_indicator(chat_id, topic_id, seconds=3)

    # 1. Check for small talk first
    small_talk_response = get_small_talk(text)
    if small_talk_response:
        print("💬 Small talk detected")
        send_with_typing(chat_id, small_talk_response, reply_to=message.message_id, topic_id=topic_id)
        return

    # 1.5 Check for invite message request
    lower_text = text.lower().strip()
    if any(trigger in lower_text for trigger in INVITE_TRIGGERS):
        print("📨 Invite message requested")
        invite = random.choice(INVITE_MESSAGES)
        invite_response = f"here's a message u can copy and share! ✨\n\n───\n{invite}\n───\n\njust copy that and send it to ur friends! 😇"
        send_with_typing(chat_id, invite_response, reply_to=message.message_id, topic_id=topic_id)
        return

    # 2. Check if question should be forwarded to human
    if should_forward_to_human(text):
        print("⚠️ Forwarding to admin...")

        # Add empathy if frustrated
        empathy = ""
        if detect_frustration(text):
            empathy = random.choice(EMPATHY_PHRASES) + "\n\n"

        forward_message = f"""{empathy}⚠️ this needs human help

👤 from: {escape_markdown(from_user)}
❓ question: "{escape_markdown(text)}"

tagging @{ADMIN_USERNAME} for assistance...

────────────
💡 tip: full FAQ here:
{FAQ_LINK}"""

        send_with_typing(chat_id, forward_message, reply_to=message.message_id, topic_id=topic_id)
        return

    # 3. Check FAQ match
    match = match_question(text)

    if match:
        print(f"✅ FAQ match: {match['category']} (lang: {language})")
        opener = get_opener()
        closer = get_closer()

        # Get response in detected language
        response = get_response(match['category'], language)

        # Build response with optional opener/closer
        parts = []
        if opener:
            parts.append(opener)
        parts.append(response)
        if closer:
            parts.append(closer)

        final_response = "\n\n".join(parts)
        send_with_typing(chat_id, final_response, reply_to=message.message_id, topic_id=topic_id)
        return

    # 4. No match - use conversational fallback
    print("ℹ️ No FAQ match, using conversational fallback")
    fallback = get_conversational_fallback()
    send_with_typing(chat_id, fallback, reply_to=message.message_id, topic_id=topic_id)

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
            time.sleep(5)
