import re
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode, ChatMemberStatus
from datetime import time

TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 🧠 MAIN MESSAGE HANDLER ==================
async def delete_bad_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    clean_text = re.sub(r'[^a-zA-Z]', '', text)

# ===== 🤬 REACT / FALLBACK =====
if "baccha" in text:
    try:
        # Try reaction (may fail in some groups)
        await context.bot.set_message_reaction(
            chat_id=message.chat_id,
            message_id=message.message_id,
            reaction=[{"type": "emoji", "emoji": "🤬"}]
        )
    except:
        # Fallback (guaranteed works)
        await message.reply_text("🤬")
            )
        except Exception as e:
            print("Reaction error:", e)

    # ===== ❌ DELETE BAD WORDS =====
    for word in blocked_words:
        if word in clean_text:
            try:
                await message.delete()
                print(f"Deleted: {text}")
                return
            except Exception as e:
                print("Error:", e)

    # ===== 🎯 KEYWORD: LAKSHYA =====
    if "lakshya" in text:
        await send_lakshya_update(update)
        return

    # ===== 🎯 KEYWORD: ARJUNA =====
    if "arjuna" in text:
        keyboard = [
            [InlineKeyboardButton("Arjuna JEE 2027", url="https://www.pw.live/study-v2/batches/698ad3519549b300a5e1cc6a/batch-overview?came_from=batch_listing#Description_1")],
            [InlineKeyboardButton("Arjuna NEET 2027", url="https://www.pw.live/study-v2/batches/69897f0ad7c19b7b2f7cc35f/batch-overview?came_from=batch_listing#Description_1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "🔥 Hey! I think you're asking about PW Arjuna Batch\n\n"
            "📚 Course Duration:\n"
            "13 April 2026 - 31 January 2027\n\n"
            "👇 Check batches below:",
            reply_markup=reply_markup
        )
        return

    # ===== 🎯 KEYWORD: PW =====
    if "pw" in text:
        keyboard = [
            [InlineKeyboardButton("🌐 Go to Website", url="https://www.pw.live/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await message.reply_text(
            "Physics Wallah is an Indian online education platform that provides accessible & comprehensive learning for students from Class 6 to 12.",
            reply_markup=reply_markup
        )
        return

# ================== 📨 Lakshya Update ==================
async def send_lakshya_update(update: Update):
    keyboard = [
        [InlineKeyboardButton("All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=ALL_CLASSES#Subjects_2")],
        [InlineKeyboardButton("Batch Details", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lecture Planner", url="https://www.pw.live/study-v2/batches/lakshya-jee-2027-181537/subjects/677938c3246e77380db0cb6f/subject-topics/topics/lecture-planner-%7C%7C-only-pdf-188305/contents?isNewPpjFlow=true&pageName=ALL_CLASSES&topic=Lecture+Planner+%7C%7C+Only+PDF")],
        [InlineKeyboardButton("Lakshya JEE 2.0", url="https://www.pw.live/study-v2/batches/6994351acb3c3eb967dd60ee/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya JEE 3.0", url="https://www.pw.live/study-v2/batches/6994351a00ac8b885c6d88b2/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
        [InlineKeyboardButton("Lakshya NEET", url="https://www.pw.live/study-v2/batches/6779346f920e596fe7f0e247/batch-overview?came_from=batch_listing#Description_1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🚀 *Lakshya 2027 Batch Update*\n\n"
        "• Batch Start Date: 6th April\n"
        "• Bridge Course Start: 25th March\n\n"
        "Select an option below 👇"
    )

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

# ================== ➕ Add Word ==================
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    member = await chat.get_member(user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Only admin allowed!")
        return

    global blocked_words
    if context.args:
        new_word = context.args[0].lower()
        if new_word not in blocked_words:
            blocked_words.append(new_word)
            await update.message.reply_text(f"✅ Added: {new_word}")

# ================== ➖ Remove Word ==================
async def remove_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    member = await chat.get_member(user.id)

    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("❌ Only admin allowed!")
        return

    global blocked_words
    if context.args:
        word = context.args[0].lower()
        if word in blocked_words:
            blocked_words.remove(word)
            await update.message.reply_text(f"🗑️ Removed: {word}")

# ================== 🗳️ Poll ==================
DAYS = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
CURRENT_DAY_INDEX = 0

CHAT_ID = -1002800090700
ATTENDANCE_TOPIC_ID = 290

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

    CURRENT_DAY_INDEX = (CURRENT_DAY_INDEX + 1) % len(DAYS)

async def send_poll_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_daily_poll(context)
    await update.message.reply_text("✅ Poll sent!")

# ================== 🚀 MAIN ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("addword", add_word))
app.add_handler(CommandHandler("removeword", remove_word))
app.add_handler(CommandHandler("sendpoll", send_poll_now))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_bad_messages))

app.job_queue.run_daily(send_daily_poll, time=time(hour=10, minute=0), days=(6,))

print("Bot running 🚀")
app.run_polling()
