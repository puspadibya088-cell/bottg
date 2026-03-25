import re
from datetime import datetime
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ================== 🔑 CONFIG ==================
TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# Schedule Data from Image (March/April 2026)
SCHEDULE = {
    "2026-03-26": {"subject": "Mathematics", "faculty": "Sachin Jakhar Sir"},
    "2026-03-28": {"subject": "Physical Chemistry", "faculty": "Faisal Razaq Sir"},
    "2026-03-31": {"subject": "Inorganic Chemistry", "faculty": "Om Pandey Sir"},
    "2026-04-01": {"subject": "Organic Chemistry", "faculty": "Pankaj Sijariya Sir"},
    "2026-04-02": {"subject": "Physics", "faculty": "Rahul Yadav Sir"},
}

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 🧠 MAIN MESSAGE HANDLER ==================
async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    clean_text_alpha = re.sub(r'[^a-z]', '', text)

    # ===== 🔔 NEW FEATURE: LAKSHYA SCHEDULE REMINDER & POLL =====
    if any(key in text for key in ["update", "schedule", "today"]):
        # Using 2026-03-26 for testing since today is 25th
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        if today_date in SCHEDULE:
            class_info = SCHEDULE[today_date]
            
            # 1. Send Beautified Message
            reminder_text = (
                f"🚀 *LAKSHYA JEE BRIDGE COURSE UPDATE* 🚀\n\n"
                f"Hey! A gentle reminder for today's class:\n\n"
                f"📚 *Class:* {class_info['subject']}\n"
                f"👨‍🏫 *Faculty:* {class_info['faculty']}\n"
                f"📅 *Date:* {datetime.now().strftime('%A, %B %d, %Y')}\n"
                f"⏰ *Time:* TBD (Check PW App)\n\n"
                f"✨ _Prepare well and stay focused!_"
            )
            await message.reply_text(reminder_text, parse_mode=ParseMode.MARKDOWN)

            # 2. Send Telegram Poll
            await context.bot.send_poll(
                chat_id=message.chat_id,
                question=f"Will you attend today's {class_info['subject']} class?",
                options=["✅ Yes, absolutely!", "❌ No, I'll watch later"],
                is_anonymous=False,
                allows_multiple_answers=False
            )
        else:
            await message.reply_text("📅 *No classes scheduled for today.* Keep revising!", parse_mode=ParseMode.MARKDOWN)
        return

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
                return 
            except Exception as e:
                print("Error:", e)

    # ===== 🎯 KEYWORD: LAKSHYA / JEE / 2027 =====
    if any(key in text for key in ["lakshya", "jee", "2027"]):
        keyboard = [
            [InlineKeyboardButton("📚 All Classes", url="https://www.pw.live")],
            [InlineKeyboardButton("🩺 Lakshya NEET", url="https://www.pw.live")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        response_text = (
            "📌 **Lakshya JEE 2027** - https://physicswallah.onelink.me\n\n"
            "**Lakshya JEE 2027 @₹5,000/-**\n"
            "*( Offers End on 31st March )*\n\n"
            "• LIVE Lectures by Top Faculties\n"
            "• DPP with Video Solution\n"
            "• Access to all Upcoming Lakshya 2027 Versions\n"
            "• Digital Preparation KIT ✨"
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
            "📚 Course Duration:\n13 April 2026 - 31 January 2027\n\n"
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))

    print("Bot is running with ALL features... 🚀")
    app.run_polling()
