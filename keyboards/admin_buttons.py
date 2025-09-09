# ============================================
# 🔹 keyboards/admin_buttons.py — administrator tugmalari
# ============================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_approve_buttons(user_id: int, application_id: int, username: str = ""):
    """Кнопки для заявок с ссылкой на профиль"""
    profile_link = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"approve_{user_id}_{application_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{user_id}_{application_id}")
        ],
        [
            InlineKeyboardButton(text="👤 Profilga o'tish", url=profile_link),
            InlineKeyboardButton(text="📞 Bog'lanish", callback_data=f"contact_{user_id}")
        ],
        [
            InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_{application_id}")
        ]
    ])

def admin_question_buttons(user_id: int, question_id: int, username: str = ""):
    """Кнопки для вопросов с ссылкой на профиль"""
    profile_link = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Javob yozish", callback_data=f"answer_question_{user_id}_{question_id}"),
            InlineKeyboardButton(text="✅ Javob berildi", callback_data=f"question_done_{question_id}")
        ],
        [
            InlineKeyboardButton(text="👤 Profilga o'tish", url=profile_link),
            InlineKeyboardButton(text="📞 Bog'lanish", callback_data=f"contact_{user_id}")
        ],
        [
            InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_question_{question_id}")
        ]
    ])

def admin_panel_buttons():
    """Кнопки админ-панели"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton(text="📝 Yangi arizalar", callback_data="admin_pending_apps")
        ],
        [
            InlineKeyboardButton(text="❓ Yangi savollar", callback_data="admin_pending_questions"),
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="🔄 Yangilash", callback_data="admin_refresh"),
            InlineKeyboardButton(text="✖️ Yopish", callback_data="admin_close")
        ]
    ])