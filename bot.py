#!/usr/bin/env python3
"""
Vanessa - MMEETT FAQ Bot
Telegram Auto-Responder with Personality
Topic-aware: Welcomes in General Chat, Answers in FAQ
"""

import os
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

print("🤖 Vanessa - MMEETT FAQ Bot started...")
print(f"📍 Monitoring group: {GROUP_ID}")
print(f"💬 General Chat Topic: {GENERAL_CHAT_ID}")
print(f"❓ FAQ Topic: {FAQ_ID}")
print(f"👤 Admin: @{ADMIN_USERNAME}")

# ============================================
# WELCOME MESSAGE
# ============================================

def get_welcome_message(user_name):
    """Generate welcome message for new members"""
    return f"""
Hey {user_name}, welcome to MMEETT X 1% Club! ⚡️

I'm Vanessa, your MMEETT guide bot. Glad to have you here!

📍 *Quick Navigation:*

☕️ *General Chat* — Hang out, introduce yourself, connect with other members

📢 *Announcement* — Company updates, Zoom call links, official news

📂 *The Vault* — Company PPT slides + professional resources (multiple languages)

🛠 *Learn & Master MMEETT* — Step-by-step tutorials (videos + guides)

❓ *Frequently Asked Questions* — Got a question? Ask here! I'll answer ASAP

💡 *First Steps:*
1. Check the Tutorial tab for a video on how to purchase your MMEETT package
2. Have questions? Drop them in the FAQ tab — I'm there to help!
3. Want to invite friends? I've got a friendly message ready for you!

Let's redefine how the world connects. 🚀
"""

def send_welcome_message(chat_id, topic_id, user_name, user_id):
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
# FAQ DATABASE - MMEETT Hardware/App Focus
# ============================================

FAQ_DATABASE = {
    "CHARGING": {
        "keywords": ["charge", "charging", "battery", "power", "green light", "red light", "low battery", "50 hours", "充电", "电池", "电源", "绿灯", "红灯"],
        "response": """🔋 *Charging MMEETT:*

1️⃣ Connect cable to MMEETT port
2️⃣ Plug into 5V/0.5A adapter (DC-5V)
3️⃣ Charge until light turns green

⏱️ Battery: 50 hours total
💤 Auto-sleep: 10 min inactivity

📚 Full FAQ: {faq_link}

────────────────

🇬🇧 *为 MMEETT 充电:*

1️⃣ 将充电线连接到 MMEETT 充电埠
2️⃣ 插入 5V/0.5A 电源适配器
3️⃣ 充电直到指示灯变绿

⏱️ 电池：总计 50 小时
💤 自动睡眠：10 分钟无操作

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "APP_DOWNLOAD": {
        "keywords": ["download", "app", "install", "application", "bluetooth", "register", "sign up", "verification code", "下载", "应用", "安装", "蓝牙", "注册", "验证码"],
        "response": """📱 *Download MMEETT App:*
📲 iOS: App Store → Search "MMEETT"
🤖 Android: Google Play → Search "MMEETT"

✅ After install:
• Enable Bluetooth access
• Enable NFC (for card writing)
• Requires: Android 6+ or iOS 12+

📧 No verification code? Check spam folder.

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *下载 MMEETT 应用:*

📲 iOS: App Store → 搜索"MMEETT"
🤖 Android: Google Play → 搜索"MMEETT"

✅ 安装后:
• 启用蓝牙访问权限
• 启用 NFC（用于名片写入）
• 需要：Android 6+ 或 iOS 12+

📧 没收到验证码？检查垃圾邮件夹。

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "DEVICE_ACTIVATION": {
        "keywords": ["activate", "bind", "connect", "pair", "nfc", "card", "write", "link", "激活", "绑定", "连接", "NFC", "名片", "写入"],
        "response": """🔗 *Activate/Bind Device:*

1️⃣ Hold TRANS 1 sec (blue light = on)
2️⃣ White light flashes = ready to bind
3️⃣ App: "Not Connected" → "Bind Device"
4️⃣ Place near phone (iPhone: top back)

📝 Write card link:
• "Me" → "Activate MMEETT Device"
• Select card → "Activate"
• Phone NFC must be ON

📚 Full FAQ: {faq_link}

────────────────

🇨 *激活/绑定设备:*

1️⃣ 长按 TRANS 1 秒（蓝灯=已开机）
2️⃣ 白灯闪烁=准备绑定
3️⃣ 应用："未连接"→"绑定设备"
4️⃣ 靠近手机（iPhone：背面顶部）

📝 写入名片链接:
• "我"→"启用 MMEETT 装置"
• 选择名片→"启用"
• 手机必须开启 NFC

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "RECORDING": {
        "keywords": ["record", "recording", "meeting", "call", "audio", "microphone", "start", "stop", "pause", "录音", "会议", "通话", "音频", "麦克风"],
        "response": """🎙️ *Start Recording:*

🎙 LIVE MODE (no phone needed):
1️⃣ Hold TRANS 1 sec (blue light)
2️⃣ Switch MEETING up
3️⃣ Vibration + RED light = recording

📞 CALL MODE:
1️⃣ Hold TRANS 1 sec (blue light)
2️⃣ Switch MEETING up
3️⃣ Double-press TRANS (0.5 sec)
4️⃣ Vibration + YELLOW light

⚠️ Call mode: Device must touch phone (no headphones)
❌ No pause feature (stop = new file)

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *开始录音:*

🎙 现场模式（无需手机）:
1️⃣ 长按 TRANS 1 秒（蓝灯）
2️⃣ 向上拨动 MEETING 开关
3️⃣ 震动 + 红灯 = 录音开始

📞 通话模式:
1️⃣ 长按 TRANS 1 秒（蓝灯）
2️⃣ 向上拨动 MEETING 开关
3️⃣ 0.5 秒内连按两下 TRANS
4️⃣ 震动 + 黄灯

⚠️ 通话模式：设备必须紧贴手机（不可用耳机）
❌ 无暂停功能（停止=新文件）

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "SYNC_TRANSFER": {
        "keywords": ["sync", "transfer", "upload", "download", "wifi", "bluetooth", "file", "empty folder", "同步", "传输", "上传", "下载", "WiFi", "蓝牙", "文件"],
        "response": """🔄 *Sync Recordings:*

1️⃣ Connect device to app (Bluetooth)
2️⃣ App shows: "Files pending sync"
3️⃣ Choose: Sync all OR select files
4️⃣ Files auto-delete after sync

⚡️ Transfer speeds:
• Bluetooth: ~tens of KB/sec (slow)
• WiFi: Much faster (recommended)

📂 Folder empty on computer? Files auto-deleted after sync. Export from app instead.

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *同步录音:*

1️⃣ 连接设备到应用（蓝牙）
2️⃣ 应用提示："有待同步文件"
3️⃣ 选择：全部同步或部分同步
4️⃣ 同步后文件自动删除

⚡️ 传输速度:
• 蓝牙：约每秒几十 KB（慢）
• WiFi: 更快（推荐）

📂 电脑文件夹为空？同步后文件自动删除。请从应用导出。

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "TRANSCRIPTION": {
        "keywords": ["transcribe", "transcript", "text", "convert", "write", "summary", "language", "转写", "文字", "转换", "书写", "摘要", "语言"],
        "response": """📝 *Transcription:*

⏱️ Time: ~50% of recording length
Example: 1-hour recording = ~30 min

🌍 Multi-language (auto-detect):
• English • 中文 • 日本語 • ไทย • 한국어

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *转写:*

⏱️ 时间：约录音时长的一半
例如：1 小时录音 = 约 30 分钟

🌍 多语言（自动识别）:
• 英文 • 中文 • 日文 • 泰文 • 韩文

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "AI_CHAT": {
        "keywords": ["ai", "chat", "bot", "model", "gpt", "gemini", "deepseek", "search", "think mode", "AI", "聊天", "机器人", "模型", "搜索"],
        "response": """🤖 *AI Chat Feature:*

1️⃣ Go to "AI Chat" tab in app
2️⃣ Chat with Mr. MMEETT agent
3️⃣ Switch models: GPT, Gemini, DeepSeek
4️⃣ Enable "Web Search" for real-time info
5️⃣ Enable "Think Mode" for complex questions

💡 Think Mode: Shows AI reasoning (DeepSeek/Gemini only)

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *AI 聊天功能:*
1️⃣ 进入应用"AI 聊天"标签
2️⃣ 与 MMEETT 先生智能代理聊天
3️⃣ 切换模型：GPT、Gemini、DeepSeek
4️⃣ 启用"全网搜索"获取实时信息
5️⃣ 启用"思考模式"处理复杂问题

💡 思考模式：显示 AI 推理过程（仅 DeepSeek/Gemini）

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "SHIPPING": {
        "keywords": ["shipping", "delivery", "track", "order", "when arrive", "processing", "运送", "送达", "追踪", "订单", "多久到"],
        "response": """📦 *Shipping & Delivery:*

📦 Processing: 3-5 business days
🚚 Delivery: 6-15 business days

📍 Track order:
App → "Me" → "Member" → "Orders"

🌍 Worldwide shipping available

📚 Full FAQ: {faq_link}

────────────────

🇨 *运送与送达:*

 处理：3-5 个工作日
🚚 送达：6-15 个工作日

📍 追踪订单:
应用→"我"→"会员"→"订单"

🌍 提供全球运送服务

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
    "RETURNS_WARRANTY": {
        "keywords": ["return", "refund", "exchange", "warranty", "repair", "broken", "20 day", "12 month", "退货", "退款", "换货", "保修", "维修", "坏了"],
        "response": """🔄 *Returns & Warranty:*

🔄 Returns: 20 days from purchase
• MMEETT Card, Membership, Computing power

🔧 Warranty: 12 months from purchase
• Free repairs during warranty
• Need: serial number + proof of purchase

📞 Contact: App → "Me" → "Customer Service"

📚 Full FAQ: {faq_link}

────────────────

🇨🇳 *退换与保修:*

🔄 退货：购买后 20 天内
• MMEETT 卡、会员、算力服务

🔧 保修：自购买日起 12 个月
• 保修期内免费维修
• 需提供：序列号 + 购买证明

📞 联系：应用→"我"→"客服"

📚 完整 FAQ: {faq_link}""".format(faq_link=FAQ_LINK),
    },
}

# Forward triggers (send to human admin)
FORWARD_TRIGGERS = [
    "price", "cost", "how much", "expensive", "cheap", "discount", "promo",
    "bulk", "wholesale", "partnership", "collaborate", "reseller", "distributor",
    "bug", "crash", "error", "broken", "not working", "issue", "problem",
    "refund", "complaint", "angry", "unhappy",
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
    """Match question against FAQ database"""
    lower_text = text.lower()
    
    for category, data in FAQ_DATABASE.items():
        for keyword in data["keywords"]:
            if keyword.lower() in lower_text:
                return {"category": category, "response": data["response"]}
    
    return None

def should_forward_to_human(text):
    """Check if question should be forwarded to admin"""
    lower_text = text.lower()
    return any(trigger in lower_text for trigger in FORWARD_TRIGGERS)

def get_invitation_message():
    """Generate friend-to-friend invitation message"""
    return """
Hey! 👋

I just found this AI platform that's actually legit — not another course or "guru" stuff.

It's called MMEETT. Basically helps you create content, automate DMs, translate into 140+ languages, and even build AI cards for networking.

I'm testing it out myself and figured you might find it useful too. No pressure at all — just thought I'd share.

Check it out if you're curious: {vault_link}

Lmk what you think!
""".format(vault_link=VAULT_LINK)

def get_conversational_fallback(user_name):
    """Friendly fallback when no FAQ match"""
    import random
    fallbacks = [
        f"Hey {user_name}, hmm that's a good one! 🤔 Let me think...",
        f"Great question, {user_name}! I don't have that in my FAQ yet.",
        f"Thanks for asking, {user_name}! I'm still learning too.",
    ]
    
    return random.choice(fallbacks) + """

Here's what I *can* help with:
• Charging & battery 🔋
• App download & setup 📱
• Device activation 🔗
• Recording features 🎙️
• Sync & transfer 🔄
• Transcription 📝
• AI Chat 🤖
• Shipping 📦
• Returns & warranty 🔄

Or check the full FAQ: {faq_link}

Need human help? @{admin_username} can assist!
""".format(faq_link=FAQ_LINK, admin_username=ADMIN_USERNAME)

def get_wrong_tab_guidance(user_name, topic_id):
    """Guide users to the correct tab"""
    if topic_id != FAQ_ID:
        return f"""
Hey {user_name}! 👋

Great question! For faster answers, could you ask this in the *Frequently Asked Questions* tab? That's where I live and can help you best! ❓

I'll keep an eye out for your question there! 😊
"""
    return None

# ============================================
# Bot Handlers
# ============================================

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
            user_name += f" @{new_user.username}"
        
        print(f"👋 New member joined: {user_name}")
        
        # Send welcome message
        send_welcome_message(chat_id, topic_id, user_name, new_user.id)

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
        from_user += f" @{message.from_user.username}"
    
    print(f"📨 Message in Topic {topic_id} from {from_user}: {text[:50]}...")
    
    # Check if message is in FAQ tab
    if topic_id != FAQ_ID:
        # Not in FAQ tab - check if it's a question
        if "?" in text or any(kw in text.lower() for kw in ["how", "what", "when", "where", "why", "can", "do", "does"]):
            # It's a question but in wrong tab
            guidance = get_wrong_tab_guidance(from_user, topic_id)
            if guidance:
                try:
                    bot.reply_to(message, guidance, parse_mode="Markdown")
                    print(f"✅ Sent wrong tab guidance to {from_user}")
                except Exception as e:
                    print(f"❌ Error sending guidance: {e}")
        return
    
    # We're in FAQ tab - process the question
    
    # Check if question should be forwarded to human
    if should_forward_to_human(text):
        print("⚠️ Forwarding to admin...")
        
        forward_message = f"""⚠️ *Question Needs Human Help*
👤 From: {from_user}
❓ Question: "{text}"

📩 Forwarding to @{ADMIN_USERNAME} for assistance...

────────────
💡 Tip: Check full FAQ:
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
    bot.infinity_polling()
