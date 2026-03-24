import re
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ================== 🔑 CONFIG ==================
TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 🧠 MAIN MESSAGE HANDLER ==================
async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    # Force lowercase for NON-CASE SENSITIVE matching
    text = message.text.lower()
    
    # Clean text for profanity (removes special chars like @, ., #)
    clean_text_alpha = re.sub(r'[^a-z]', '', text)

    # ===== 🤬 REACT / FALLBACK (JOJO FEATURE) =====
    if "baccha" in text:
        try:
            await context.bot.set_message_reaction(
                chat_id=message.chat_id,
                message_id=message.message_id,
                reaction=[{"type": "emoji", "emoji": "🤬"}]
            )
        except:
            await message.reply_text("🤬")

    # ===== ❌ DELETE BAD WORDS (JOJO FEATURE) =====
    for word in blocked_words:
        if word in clean_text_alpha:
            try:
                await message.delete()
                print(f"Deleted: {text}")
                return # Stop processing after deletion
            except Exception as e:
                print("Error:", e)

    # ===== 🎯 NEW KEYWORD: LAKSHYA / JEE / 2027 =====
    if any(key in text for key in ["lakshya", "jee", "2027"]):
        keyboard = [
            [InlineKeyboardButton("📚 All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=ALL_CLASSES#Subjects_2")],
            [InlineKeyboardButton("🩺 Lakshya NEET", url="https://www.pw.live/study-v2/batches/6779346f920e596fe7f0e247/batch-overview?came_from=batch_listing#Description_1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response_text = (
            "📌 **Lakshya JEE 2027** - https://physicswallah.onelink.me\n\n"
            "**Lakshya JEE 2027 @₹5,000/-**\n"
            "*( Offers End on 31st March )*\n\n"
            "• LIVE Lectures by Top Faculties ( 2 Faculties Set )\n"
            "• DPP with Video Solution\n"
            "• Regular Tests + AITS\n"
            "• LIVE Doubt Resolution\n"
            "• Access to all Upcoming Lakshya 2027 Versions\n"
            "• Access to all Previous Arjuna 2026 Batches\n"
            "• Access to Parishram 2027\n"
            "• Digital Preparation KIT ✨\n"
            "• Mentorship by IITians\n"
            "• 6 Months PW Talk Subscription"
        )
        
        await message.reply_text(response_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return

    # ===== 🎯 KEYWORD: ARJUNA (JOJO FEATURE) =====
    if "arjuna" in text:
        keyboard = [
            [InlineKeyboardButton("Arjuna JEE 2027", url="https://www.pw.live")],
            [InlineKeyboardButton("Arjuna NEET 2027", url="https://www.pw.live")]
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

    # ===== 🎯 KEYWORD: PW (JOJO FEATURE) =====
    if "pw" in text:
        keyboard = [[InlineKeyboardButton("🌐 Go to Website", url="https://www.pw.live")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            "Physics Wallah is an Indian online education platform that provides accessible & comprehensive learning for students from Class 6 to 12.",
            reply_markup=reply_markup
        )
        return

# ================== 🚀 MAIN ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Catch all text messages that aren't commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))

    print("Bot is running with JOJO features... 🚀")
    app.run_polling()
