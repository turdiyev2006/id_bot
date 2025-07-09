from telegram import User

def format_user_info(user: User) -> str:
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "—"
    language = user.language_code or "—"

    return (
        f"🆔 <b>Sizning Telegram ID:</b> <code>{user.id}</code>\n"
        f"👤 <b>Username:</b> {username}\n"
        f"🧑‍💼 <b>Ism:</b> {full_name}\n"
        f"🌐 <b>Til:</b> {language}"
    )

def get_user_greeting(user: User) -> str:
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    return f"📩 <b>Yangi foydalanuvchi:</b>\nПривет, <b>{full_name.upper()}!</b>"
