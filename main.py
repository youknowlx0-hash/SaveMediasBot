import json
from telegram import *
from telegram.ext import *
from config import *
from downloader import download_video
from youtube import search_youtube

# -------- DB --------
def load():
    try:
        return json.load(open("db.json"))
    except:
        return {"users": {}}

def save(db):
    json.dump(db, open("db.json", "w"), indent=4)

# -------- START --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text1 = "How to use the bot? 👇"
    
    text2 = """🔗 Send me a link
to a post on Instagram, YouTube, TikTok, etc. — in a few seconds, the photo, text, or video will be yours!

🔎 To search for videos on YouTube
use the search button👇"""

    buttons = [
        [InlineKeyboardButton("🔎 Search Video", callback_data="yt_search")],
        [InlineKeyboardButton("➕ Add Bot to Chat", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("📨 Invite Friend", switch_inline_query="")]
    ]

    await update.message.reply_text(text1)
    await update.message.reply_text(text2, reply_markup=InlineKeyboardMarkup(buttons))

# -------- MENU --------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📥 My options:

▫️ Instagram: reels, posts & stories
▫️ Pinterest: videos & stories
▫️ Tiktok: videos, photos & audio
▫️ Twitter (X): videos & voice
▫️ Vk: videos & clips
▫️ Reddit: videos & gifs
▫️ Twitch: clips
▫️ Vimeo
▫️ Ok: video
▫️ Tumblr: videos & audio
▫️ Dailymotion: videos
▫️ Likee: videos
▫️ Soundcloud
▫️ Apple Music
▫️ Spotify

⭐️ Subscription: not active
"""

    buttons = [
        [InlineKeyboardButton("➕ Add Bot", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("📞 Support", url="https://t.me/YOUR_ID")],
        [InlineKeyboardButton("🌐 Language", callback_data="lang")],
        [InlineKeyboardButton("📨 Invite Friend", switch_inline_query="")],
        [InlineKeyboardButton("💎 Subscription", callback_data="sub")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# -------- YT SEARCH --------
async def yt_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Send search query 🔎")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if "http" in msg:
        await update.message.reply_text("📥 Downloading...")
        file = download_video(msg)
        await update.message.reply_video(video=open(file, "rb"))
    else:
        results = search_youtube(msg)
        for v in results:
            await update.message.reply_text(f"{v['title']}\n{v['url']}")

# -------- SUBSCRIPTION --------
async def subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🚫 Don't want to see ads?

No ads (subscriptions/mailing)
for a month

Discount! 149❌ → 99 Stars"""

    buttons = [
        [InlineKeyboardButton("💎 Buy - 99 Stars", pay=True)],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ]

    await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# -------- CALLBACK --------
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data

    if data == "yt_search":
        await yt_search_handler(update, context)

    elif data == "sub":
        await subscription(update, context)

# -------- MAIN --------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CallbackQueryHandler(callbacks))
app.add_handler(MessageHandler(filters.TEXT, handle_text))

app.run_polling()
