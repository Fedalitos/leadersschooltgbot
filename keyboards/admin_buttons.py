# admin_buttons.py - улучшенная версия
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_approve_buttons(user_id: int, application_id: int, username: str = ""):
    """Красивые кнопки для заявок с ссылкой на профиль"""
    profile_link = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_{user_id}_{application_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}_{application_id}")
        ],
        [
            InlineKeyboardButton(text="👤 Профиль пользователя", url=profile_link),
            InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{user_id}")
        ],
        [
            InlineKeyboardButton(text="💬 Ответить быстро", callback_data=f"quick_answer_{user_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_{application_id}")
        ]
    ])

def admin_question_buttons(user_id: int, question_id: int, username: str = ""):
    """Красивые кнопки для вопросов с ссылкой на профиль"""
    profile_link = f"https://t.me/{username}" if username else f"tg://user?id={user_id}"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Ответить", callback_data=f"answer_question_{user_id}_{question_id}"),
            InlineKeyboardButton(text="✅ Отвечено", callback_data=f"question_done_{question_id}")
        ],
        [
            InlineKeyboardButton(text="👤 Профиль пользователя", url=profile_link),
            InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{user_id}")
        ],
        [
            InlineKeyboardButton(text="⚡ Быстрый ответ", callback_data=f"quick_reply_{user_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_question_{question_id}")
        ]
    ])

def admin_panel_buttons():
    """Красивые кнопки админ-панели"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="📝 Заявки", callback_data="admin_pending_apps")
        ],
        [
            InlineKeyboardButton(text="❓ Вопросы", callback_data="admin_pending_questions"),
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_refresh"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")
        ],
        [
            InlineKeyboardButton(text="✖️ Закрыть", callback_data="admin_close")
        ]
    ])