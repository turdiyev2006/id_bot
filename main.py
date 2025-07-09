import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

last_used = {}

def log_user(user):
    with open("log.csv", mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), user.id, user.full_name, user.username])

def get_greeting(language_code):
    if language_code == 'uz':
        return "Salom"
    elif language_code == 'ru':
        return "Привет"
    return "Hello"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user = update.effective_user
    user_id = user.id

    if user_id in last_used and time.time() - last_used[user_id] < 60:
        await update.message.reply_text("⏱️ Iltimos, keyinroq yana urinib ko‘ring.")
        return
    last_used[user_id] = time.time()

    greeting = get_greeting(user.language_code)
    text = (
    f"{greeting}, {user.first_name}!\n\n"
    f"🆔 Telegram ID: {user.id}\n"
    f"👤 Username: @{user.username if user.username else 'yo‘q'}\n"
    f"📛 Ism: {user.full_name}\n"
    f"🌐 Til: {user.language_code}"
)


    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 ID ni nusxalash", callback_data="copy_id")]
    ])

    await update.message.reply_text(text, reply_markup=keyboard)

    if user.id != ADMIN_ID:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📥 Yangi foydalanuvchi:{text}")
        log_user(user)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "copy_id":
        user_id = query.from_user.id
        await query.message.reply_text(f"📋 Sizning ID: {user_id}", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
       f"🤖 Bu bot sizning Telegram ID, ism, username va tilingizni ko‘rsatadi.",
        "Foydalanish uchun /start buyrug'ini yuboring."
    )

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
          with open("log.csv", encoding="utf-8") as f:
           lines = f.readlines()[-20:]
          await update.message.reply_text("🗂 Oxirgi foydalanuvchilar:\n" + ''.join(lines))
    except FileNotFoundError:
        await update.message.reply_text("❌ Log fayl topilmadi.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        with open("log.csv", encoding="utf-8") as f:
            count = len(f.readlines())
        await update.message.reply_text(f"📊 Jami foydalanuvchilar soni: {count}")
    except FileNotFoundError:
        await update.message.reply_text("❌ Hech kim botdan foydalanmagan.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()
