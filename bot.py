import os
import re
import json
from datetime import datetime, timedelta, time as dt_time
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.constants import ParseMode
from telegram.constants import ChatMemberStatus
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

parse_mode=ParseMode.MARKDOWN

# ================== CONFIG ==================
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = int(os.environ.get('CHAT_ID', -1002800090700))  # Your supergroup ID
ATTENDANCE_TOPIC_ID = int(os.environ.get('ATTENDANCE_TOPIC_ID', 290))
TIMEZONE = pytz.timezone("Asia/Kolkata")
PROJECTS_FILE = "projects.json"
UPDATE_INTERVAL = 60  # seconds
message_id = None
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita","vanshika","shika"]
DAYS = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
CURRENT_DAY_INDEX = 0
# ============================================

# ================ Bad Words Filter ==================
async def delete_bad_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        text = message.text.lower()
        clean_text = re.sub(r'[^a-zA-Z]', '', text)
        for word in blocked_words:
            if word in clean_text:
                try:
                    await message.delete()
                    print(f"Deleted: {text}")
                    break
                except Exception as e:
                    print("Error deleting:", e)
        if "lakshya" in text:
            await send_lakshya_update(update)

# ================ Lakshya Batch Update ==================
async def send_lakshya_update(update: Update):
    keyboard = [
        [InlineKeyboardButton("All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=ALL_CLASSES#Subjects_2")],
        [InlineKeyboardButton("Batch Details", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lecture Planner", url="https://www.pw.live/study-v2/batches/lakshya-jee-2027-181537/subjects/677938c3246e77380db0cb6f/subject-topics/topics/lecture-planner-%7C%7C-only-pdf-188305/contents?isNewPpjFlow=true&pageName=ALL_CLASSES&topic=Lecture+Planner+%7C%7C+Only+PDF&chapterId=67a1f05e0a0df377968f2e66&batchSubjectId=677938c3246e77380db0cb6f&isResources=true&contentOption=Lectures")],
        [InlineKeyboardButton("Lakshya JEE 2.0", url="https://www.pw.live/study-v2/batches/6994351acb3c3eb967dd60ee/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya JEE 3.0", url="https://www.pw.live/study-v2/batches/6994351a00ac8b885c6d88b2/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya NEET", url="https://www.pw.live/study-v2/batches/6779346f920e596fe7f0e247/batch-overview?came_from=batch_listing#Description_1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🚀 *Lakshya 2027 Batch Update*\n\n"
        "• Batch Start Date: 6th April\n"
        "• Bridge Course Start: 25th March\n\n"
        "Select an option below to view details 👇"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# ================ Add/Remove Blocked Words (Admin Only) ==================
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await update.effective_chat.get_member(user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Sirf admin hi word add kar sakta hai!")
        return
    if context.args:
        new_word = context.args[0].lower()
        if new_word in blocked_words:
            await update.message.reply_text(f"⚠️ {new_word} already blocked!")
        else:
            blocked_words.append(new_word)
            await update.message.reply_text(f"✅ Added word: {new_word}")
            print("Updated blocked words:", blocked_words)

async def remove_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    member = await update.effective_chat.get_member(user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Sirf admin hi word remove kar sakta hai!")
        return
    if context.args:
        word_to_remove = context.args[0].lower()
        if word_to_remove in blocked_words:
            blocked_words.remove(word_to_remove)
            await update.message.reply_text(f"🗑️ Removed word: {word_to_remove}")
            print("Updated blocked words:", blocked_words)
        else:
            await update.message.reply_text(f"⚠️ {word_to_remove} not in blocked list!")
    else:
        await update.message.reply_text("⚠️ Usage: /removeword <word>")

# ================ Get Chat & Thread IDs ==================
async def get_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = update.message.message_thread_id
    await update.message.reply_text(f"Chat ID: {chat_id}\nThread ID: {thread_id}")
    print("Chat ID:", chat_id, "Thread ID:", thread_id)

# ================ Attendance Poll ==================
CURRENT_DAY_INDEX = 0
async def send_daily_poll(context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_DAY_INDEX
    day_name = DAYS[CURRENT_DAY_INDEX]
    await context.bot.send_poll(
        chat_id=CHAT_ID,
        question=day_name,
        options=["P","A"],
        is_anonymous=False,
        message_thread_id=ATTENDANCE_TOPIC_ID
    )
    print(f"Poll sent for {day_name}")
    CURRENT_DAY_INDEX = (CURRENT_DAY_INDEX + 1) % len(DAYS)

async def send_poll_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_daily_poll(context)
    await update.message.reply_text("✅ Poll sent manually!")

# ================ Multi-Project Countdown ==================
message_id = None
def load_projects():
    with open(PROJECTS_FILE, "r") as f:
        data = json.load(f)
    projects = []
    for p in data.get("projects", []):
        projects.append({"name": p["name"], "deadline": datetime.fromisoformat(p["deadline"])})
    return projects

def get_countdown_text():
    now = datetime.now(TIMEZONE)
    projects = load_projects()
    lines = []
    for proj in projects:
        diff = proj["deadline"] - now
        if diff.total_seconds() <= 0:
            lines.append(f"🚨 {proj['name']} deadline reached! Submit now!")
            continue
        days, remainder = divmod(diff.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_seconds = (proj["deadline"] - (proj["deadline"] - timedelta(days=7))).total_seconds()
        filled_blocks = int((total_seconds - diff.total_seconds()) / total_seconds * 10)
        bar = "█"*filled_blocks + "-"*(10-filled_blocks)
        lines.append(f"⏰ {proj['name']}:\n{int(days)}d {int(hours)}h {int(minutes)}m left\n[{bar}]")
    return "\n\n".join(lines)

async def update_countdown_job(context: ContextTypes.DEFAULT_TYPE):
    global message_id
    text = get_countdown_text()
    if message_id:
        try:
            await context.bot.edit_message_text(chat_id=CHAT_ID, message_id=message_id, text=text)
        except Exception as e:
            print("Error updating countdown:", e)
    else:
        msg = await context.bot.send_message(chat_id=CHAT_ID, text=text)
        message_id = msg.message_id

# ================ Setup Bot ==================
app = ApplicationBuilder().token(TOKEN).build()

# Handlers
app.add_handler(CommandHandler("addword", add_word))
app.add_handler(CommandHandler("removeword", remove_word))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_bad_messages))
app.add_handler(CommandHandler("getid", get_ids))
app.add_handler(CommandHandler("sendpoll", send_poll_now))

# Schedule Attendance Poll every Sunday 10AM
app.job_queue.run_daily(send_daily_poll, time=dt_time(hour=10, minute=0), days=(6,))  # Sunday=6

# Schedule Countdown updates every minute
app.job_queue.run_repeating(update_countdown_job, interval=UPDATE_INTERVAL, first=0)

# Run the bot
print("✅ Bot is running...")
app.run_polling()
