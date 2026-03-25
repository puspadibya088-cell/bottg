import re
from datetime import datetime
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ================== 🔑 CONFIG ==================
TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# Full Schedule Data from Image (March/April 2026)
# Format: { "YYYY-MM-DD": {"subject": "...", "faculty": "..."} }
SCHEDULE = {
    "2026-03-26": {"subject": "Mathematics", "faculty": "Sachin Jakhar Sir"},
    "2026-03-28": {"subject": "Physical Chemistry", "faculty": "Faisal Razaq Sir"},
    "2026-03-31": {"subject": "Inorganic Chemistry", "faculty": "Om Pandey Sir"},
    "2026-04-01": {"subject": "Organic Chemistry", "faculty": "Pankaj Sijariya Sir"},
    "2026-04-02": {"subject": "Physics", "faculty": "Rahul Yadav Sir"},
}

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 📅 BRIDGE COURSE HANDLER (/bridge) ==================
async def bridge_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Find the next class based on current date
    today_dt = datetime.now()
    next_class_date = None
    
    # Sort keys to find the closest upcoming date
    for date_str in sorted(SCHEDULE.keys()):
        class_dt = datetime.strptime(date_str, "%Y-%m-%d")
        if class_dt >= today_dt:
            next_class_date = date_str
            break
            
    if next_class_date:
        class_info = SCHEDULE[next_class_date]
        display_date = datetime.strptime(next_class_date, "%Y-%m-%d").strftime('%A, %B %d, %Y')
        
        # 1. Beautified Message
        reminder_text = (
            f"🚀 *LAKSHYA JEE BRIDGE COURSE UPDATE* 🚀\n\n"
            f"Hey! A gentle reminder for the most recent class:\n\n"
            f"📚 *Class:* {class_info['subject']}\n"
            f"👨‍🏫 *Faculty:* {class_info['faculty']}\n"
            f"📅 *Date:* {display_date}\n"
            f"⏰ *Time:* TBD (Check PW App)\n\n"
            f"✨ _Prepare well and stay focused!_"
        )
        await update.message.reply_text(reminder_text, parse_mode=ParseMode.MARKDOWN)

        # 2. Telegram Poll
        await context.bot.send_poll(
            chat_id=update.message.chat_id,
            question=f"Will you attend the {class_info['subject']} class?",
            options=["✅ Yes, absolutely!", "❌ No, I'll watch later"],
            is_anonymous=False,
            allows_multiple_answers=False
        )
    else:
        await update.message.reply_text("🏁 *Bridge Course Completed!* No upcoming classes found in the schedule.", parse_mode=ParseMode.MARKDOWN)

# ================== 🧠 MAIN MESSAGE HANDLER ==================
async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
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
                return 
            except:
                pass

    # ===== 🎯 KEYWORD: LAKSHYA / JEE / 2027 =====
    if any(key in text for key in ["lakshya", "jee", "2027"]):
        keyboard = [
            [InlineKeyboardButton("📚 All Classes", url="https://www.pw.live")],
            [InlineKeyboardButton("🩺 Lakshya NEET", url="https://www.pw.live")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        response_text = "📌 *Lakshya JEE 2027 @₹5,000/-*\n*( Offers End on 31st March )*\n\n• LIVE Lectures\n• DPP with Video Solution\n• Digital Preparation KIT ✨"
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
            "🔥 Hey! I think you're asking about PW Arjuna Batch\n\n📚 Course Duration:\n13 April 2026 - 31 January 2027",
            reply_markup=reply_markup
        )
        return

    # ===== 🎯 KEYWORD: PW (JOJO FEATURE) =====
    if "pw" in text:
        keyboard = [[InlineKeyboardButton("🌐 Go to Website", url="https://www.pw.live")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            "Physics Wallah is an Indian online education platform that provides accessible learning for students from Class 6 to 12.",
            reply_markup=reply_markup
        )
        return

# ================== 🚀 MAIN ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add Command Handler for /bridge (you can change this to /bcr if preferred)
    app.add_handler(CommandHandler("bridge", bridge_schedule_handler))
    
    # Catch all text messages for previous features
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))

    print("Bot is running with ALL features & /bridge command... 🚀")
    app.run_polling()
