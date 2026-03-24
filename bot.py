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
            await context.bot.set_message_reaction(
                chat_id=message.chat_id,
                message_id=message.message_id,
                reaction=[{"type": "emoji", "emoji": "🤬"}]
            )
        except:
            await message.reply_text("🤬")

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
        [InlineKeyboardButton("All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🚀 Lakshya 2027 Batch Update", reply_markup=reply_markup)

# ================== 🚀 MAIN ==================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_bad_messages))

print("Bot running 🚀")
app.run_polling()
