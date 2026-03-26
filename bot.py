import re
from datetime import datetime, time, timedelta
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# ================== 🔑 CONFIG ==================
TOKEN = "8557330337:AAFNiIGDo3TQ69arviN39qrCrqbbbFsFfMI"
GROUP_CHAT_ID = -2800090700 

SCHEDULE = [
    {"date": "2026-03-26", "subject": "Mathematics", "faculty": "Sachin Jakhar Sir"},
    {"date": "2026-03-28", "subject": "Physical Chemistry", "faculty": "Faisal Razaq Sir"},
    {"date": "2026-03-31", "subject": "Inorganic Chemistry", "faculty": "Om Pandey Sir"},
    {"date": "2026-04-01", "subject": "Organic Chemistry", "faculty": "Pankaj Sijariya Sir"},
    {"date": "2026-04-02", "subject": "Physics", "faculty": "Rahul Yadav Sir"},
]

blocked_words = ["gandu", "madarchod", "bhosdi", "spam", "nunu", "santanu", "puspa", "harshita", "vanshika", "shika"]

# ================== 🤖 AUTOMATION HELPERS ==================

async def send_bridge_update(context: ContextTypes.DEFAULT_TYPE, target_chat_id: int, class_data: dict):
    try:
        display_date = datetime.strptime(class_data["date"], "%Y-%m-%d").strftime('%A, %B %d, %Y')
        subj = class_data['subject']
        
        reminder_text = (
            f"🚀 *LAKSHYA JEE BRIDGE COURSE UPDATE* 🚀\n\n"
            f"Hey! A gentle reminder for today's class:\n\n"
            f"📚 *Class:* {subj}\n"
            f"👨‍🏫 *Faculty:* {class_data['faculty']}\n"
            f"📅 *Date:* {display_date}\n"
            f"⏰ *Time:* TBD\n\n"
            f"✨ _Prepare well and stay focused!_"
        )
        
        await context.bot.send_message(chat_id=target_chat_id, text=reminder_text, parse_mode=ParseMode.MARKDOWN)
        await context.bot.send_poll(
            chat_id=target_chat_id,
            question=f"Will you attend today's {subj} class?",
            options=["✅ Yes, I'm ready!", "❌ No, I'll watch later"],
            is_anonymous=False
        )
    except Exception as e:
        print(f"Error sending update: {e}")

async def daily_schedule_checker(context: ContextTypes.DEFAULT_TYPE):
    now_ist = datetime.now() + timedelta(hours=5, minutes=30)
    today_str = now_ist.strftime("%Y-%m-%d")
    
    for item in SCHEDULE:
        if item["date"] == today_str:
            await send_bridge_update(context, GROUP_CHAT_ID, item)
            break

async def test_job_callback(context: ContextTypes.DEFAULT_TYPE):
    test_class = {"date": "2026-03-25", "subject": "BOT TEST", "faculty": "Automation System"}
    await send_bridge_update(context, GROUP_CHAT_ID, test_class)
    print("Test message sent successfully!")

# ================== 🛠️ COMMANDS & MESSAGES ==================

async def get_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Chat ID is: `{update.effective_chat.id}`", parse_mode=ParseMode.MARKDOWN)

async def bridge_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try: await update.message.delete()
    except: pass
    now_ist = datetime.now() + timedelta(hours=5, minutes=30)
    today_str = now_ist.strftime("%Y-%m-%d")
    target_class = next((item for item in SCHEDULE if item["date"] >= today_str), SCHEDULE[-1])
    await send_bridge_update(context, update.effective_chat.id, target_class)

async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text: return
    
    # Non-case sensitive logic
    text = message.text.lower()
    clean = re.sub(r'[^a-z]', '', text)

    # 1. Block Bad Words
    if any(word in clean for word in blocked_words):
        try: await message.delete()
        except: pass
        return

    # 2. Reaction for "baccha"
    if "baccha" in text:
        try: await context.bot.set_message_reaction(chat_id=message.chat_id, message_id=message.message_id, reaction=[{"type": "emoji", "emoji": "🤬"}])
        except: pass

    # 3. Lakshya JEE Trigger (The Update)
    if "lakshya" in text:
        offer_text = (
            "🚀 *Lakshya JEE 2027 @₹5,000/-* (Offers End on 31st March)\n\n"
            "• LIVE Lectures by Top Faculties (2 Faculties Set)\n"
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
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 All Classes", url="https://www.pw.live/study-v2/batches/6779345c20fa0756e4a7fd08/batch-overview?isNewPpjFlow=true&pageName=ALL_CLASSES#Subjects_2")],
            [InlineKeyboardButton("Lecture Planner", url="https://www.pw.live/study-v2/batches/lakshya-jee-2027-181537/subjects/677938c3246e77380db0cb6f/subject-topics/topics/lecture-planner-and-class-schedule-%7C%7C-only-pdf-853346/contents?isNewPpjFlow=true&pageName=ALL_CLASSES&topic=Lecture+Planner+And+Class+Schedule+%7C%7C+Only+PDF&chapterId=67a1f05e0a0df377968f2e66&batchSubjectId=677938c3246e77380db0cb6f&isResources=true&contentOption=Lectures")]
            [InlineKeyboardButton("📚 Lakshya JEE 2.0", url="https://www.pw.live/study-v2/batches/6994351acb3c3eb967dd60ee/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
            [InlineKeyboardButton("📚 Lakshya JEE 3.0", url="https://www.pw.live/study-v2/batches/6994351a00ac8b885c6d88b2/batch-overview?isNewPpjFlow=true&pageName=DESCRIPTION#Description_1")],
            [InlineKeyboardButton("🩺 Lakshya NEET 2027", url="https://www.pw.live/study-v2/batches/6779346f920e596fe7f0e247/batch-overview?came_from=batch_listing#Description_1")],
            
        ])
        
        await message.reply_text(offer_text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)

    # 4. Other Triggers
    elif "arjuna" in text:
        await message.reply_text("🔥 *PW Arjuna Batch*\n📚 April 2026 - Jan 2027", parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Arjuna", url="https://www.pw.live")]]))
    elif "pw" in text:
        await message.reply_text("Physics Wallah online education platform.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Website", url="https://www.pw.live")]]))

# ================== 🚀 RUN ==================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    # 10 AM IST Daily Job
    app.job_queue.run_daily(daily_schedule_checker, time=time(hour=4, minute=30, second=0))

    # Test run after 60 seconds
    app.job_queue.run_once(test_job_callback, when=60) 

    app.add_handler(CommandHandler("bridge", bridge_schedule_handler))
    app.add_handler(CommandHandler("getid", get_id_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler))

    print("Bot is LIVE! 🚀")
    app.run_polling()
