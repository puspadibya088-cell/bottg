import re
from datetime import datetime
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ================== 🔑 CONFIG ==================
TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"

# Schedule Data from Image (March/April 2026)
SCHEDULE = [
    {"date": "2026-03-26", "subject": "Mathematics", "faculty": "Sachin Jakhar Sir"},
    {"date": "2026-03-28", "subject": "Physical Chemistry", "faculty": "Faisal Razaq Sir"},
    {"date": "2026-03-31", "subject": "Inorganic Chemistry", "faculty": "Om Pandey Sir"},
    {"date": "2026-04-01", "subject": "Organic Chemistry", "faculty": "Pankaj Sijariya Sir"},
    {"date": "2026-04-02", "subject": "Physics", "faculty": "Rahul Yadav Sir"},
]

# ================== 🔥 Blocked Words ==================
blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "bkl", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 📅 BRIDGE COURSE HANDLER (/bridge) ==================
async def bridge_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Delete the user's /bridge command message immediately
    try:
        await update.message.delete()
    except Exception as e:
        print(f"Could not delete command: {e}")

    # 2. Find the most recent/upcoming class
    today_dt = datetime.now()
    target_class = None
    
    for item in SCHEDULE:
        class_dt = datetime.strptime(item["date"], "%Y-%m-%d")
        if class_dt >= today_dt:
            target_class = item
            break
    
    # Fallback to the last class if all dates have passed
    if not target_class:
        target_class = SCHEDULE[-1]

    display_date = datetime.strptime(target_class["date"], "%Y-%m-%d").strftime('%A, %B %d, %Y')
    
    # 3. Send the Beautified Message
    reminder_text = (
        f"🚀 *LAKSHYA JEE BRIDGE COURSE UPDATE* 🚀\n\n"
        f"Hey! A gentle reminder for today's class:\n\n"
        f"📚 *Class:* {target_class['subject']}\n"
        f"👨‍🏫 *Faculty:* {target_class['faculty']}\n"
        f"📅 *Date:* {display_date}\n"
        f"⏰ *Time:* TBD (Announced Soon)\n\n"
        f"✨ _Prepare well and stay focused!_"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=reminder_text, 
        parse_mode=ParseMode.MARKDOWN
    )

    # 4. Send the Standalone Poll
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=f"Will you attend today's {target_class['subject']} class?",
        options=["✅ Yes, I'm ready!", "❌ No, I'll watch later"],
        is_anonymous=False,
        allows_multiple_answers=False
    )

# ================== 🧠 PREVIOUS FEATURES (JOJO) ==================
async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    clean_text_alpha = re.sub(r'[^a-z]', '', text)

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
        if word in clean_text_alpha:
            try:
                await message.delete()
                return 
            except:
                pass

    # ===== 🎯 KEYWORDS: LAKSHYA / ARJUNA / PW =====
    if any(key in text for key in ["lakshya", "jee", "2027"]):
        keyboard = [[InlineKeyboardButton("📚 All Classes", url="https://www.pw.live")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("📌 *Lakshya JEE 2027 @₹5,000/-*\n• LIVE Lectures\n• DPPs\n• Access to Arjuna 2026", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif "arjuna" in text:
        keyboard = [[InlineKeyboardButton("Arjuna JEE 2027", url="https://www.pw.live")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("🔥 *PW Arjuna Batch*\n📚 Duration: 13 April 2026 - 31 January 2027", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    elif "pw" in text:
        keyboard = [[InlineKeyboardButton("🌐 Go to Website", url="https://www.pw.live")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Physics Wallah is an Indian online education platform providing accessible learning.", reply_markup=reply_markup)

# ================== 🚀 MAIN ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("bridge", bridge_schedule_handler))
    
    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))

    print("Bot updated! /bridge command with auto-delete and standalone poll is active. 🚀")
    app.run_polling()
