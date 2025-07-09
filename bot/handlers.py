import os
from telegram import Update
from telegram.ext import ContextTypes
from .utils import format_user_info, is_new_user, get_user_greeting

ADMIN_ID = os.getenv("ADMIN_ID")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    info_text = format_user_info(user)
    greeting = get_user_greeting(user)

    # Foydalanuvchiga yuborish
    await context.bot.send_message(
        chat_id=chat.id,
        text=f"{greeting}\n{info_text}",
        parse_mode="HTML"
    )

    # Adminga yuborish
    if str(user.id) != ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👤 <b>Yangi foydalanuvchi</b> ishlatdi:\n{info_text}",
            parse_mode="HTML"
        )
