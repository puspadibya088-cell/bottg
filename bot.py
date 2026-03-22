import re
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode, ChatMemberStatus
from datetime import time

TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl" , "nunu", "santanu" , "puspa" ,"harshita","vanshika","shika"]

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
                    print("Error:", e)
        if "lakshya" in text:
            await send_lakshya_update(update)

# ================== 📨 Lakshya Update ==================
async def send_lakshya_update(update: Update):
    keyboard = [
        [InlineKeyboardButton("All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=ALL_CLASSES#Subjects_2")],
        [InlineKeyboardButton("Batch Details", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lecture Planner", url="https://www.pw.live/study-v2/batches/lakshya-jee-2027-181537/subjects/677938c3246e77380db0cb6f/subject-topics/topics/lecture-planner-%7C%7C-only-pdf-188305/contents?isNewPpjFlow=true&pageName=ALL_CLASSES&topic=Lecture+Planner+%7C%7C+Only+PDF&chapterId=67a1f05e0a0df377968f2e66&batchSubjectId=677938c3246e77380db0cb6f&isResources=true&contentOption=Lectures")],
        [InlineKeyboardButton("Lakshya JEE 2.0", url="https://www.pw.live/study-v2/batches/6994351acb3c3eb967dd60ee/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya JEE 3.0", url="https://www.pw.live/study-v2/batches/6994351a00ac8b885c6d88b2/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya NEET ", url="https://www.pw.live/study-v2/batches/6779346f920e596fe7f0e247/batch-overview?came_from=batch_listing#Description_1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🚀 *Lakshya 2027 Batch Update*\n\n"
        "• Batch Start Date: 6th April\n"
        "• Bridge Course Start: 25th March\n\n"
        "Select an option below to view details 👇"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# ================== ➕ Add Word (Admin Only) ==================
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    member = await chat.get_member(user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Sirf admin hi word add kar sakta hai!")
        return

    global blocked_words
    if context.args:
        new_word = context.args[0].lower()
        if new_word in blocked_words:
            await update.message.reply_text(f"⚠️ {new_word} already blocked!")
        else:
            blocked_words.append(new_word)
            await update.message.reply_text(f"✅ Added word: {new_word}")
            print("Updated blocked words:", blocked_words)

# ================== ➖ Remove Word (Admin Only) ==================
async def remove_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    member = await chat.get_member(user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Sirf admin hi word remove kar sakta hai!")
        return

    global blocked_words
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

# ================== 🆔 Get Chat & Topic ID ==================
async def get_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = update.message.message_thread_id
    await update.message.reply_text(f"Chat ID: {chat_id}\nThread ID: {thread_id}")
    print("Chat ID:", chat_id)
    print("Thread ID:", thread_id)

# ================== 🗳️ Attendance Poll ==================
DAYS = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
CURRENT_DAY_INDEX = 0

CHAT_ID = -1002800090700  # Your supergroup ID
ATTENDANCE_TOPIC_ID = 290  # Attendance topic thread ID

async def send_daily_poll(context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_DAY_INDEX
    bot = context.bot
    day_name = DAYS[CURRENT_DAY_INDEX]

    await bot.send_poll(
        chat_id=CHAT_ID,
        question=day_name,
        options=["P","A"],
        is_anonymous=False,
        message_thread_id=ATTENDANCE_TOPIC_ID
    )

    print(f"Poll sent for {day_name}")
    CURRENT_DAY_INDEX = (CURRENT_DAY_INDEX + 1) % len(DAYS)

# ================== 🚀 Setup Bot ==================
app = ApplicationBuilder().token(TOKEN).build()

# Command to send poll manually
async def send_poll_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_daily_poll(context)
    await update.message.reply_text("✅ Poll sent manually!")

# ================== Handlers ==================
app.add_handler(CommandHandler("addword", add_word))
app.add_handler(CommandHandler("removeword", remove_word))  # <-- add this
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_bad_messages))
app.add_handler(CommandHandler("getid", get_ids))
app.add_handler(CommandHandler("sendpoll", send_poll_now))

# Schedule attendance poll every Sunday 10 AM
app.job_queue.run_daily(send_daily_poll, time=time(hour=10, minute=0), days=(6,))  # Sunday=6

print("Bot is running...")
app.run_polling()
