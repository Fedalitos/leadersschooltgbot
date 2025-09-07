# ============================================
# 🔹 keyboards/admin_buttons.py — administrator tugmalari
# ============================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_approve_buttons(user_id: int, application_id: int):
    """Кнопки для заявок"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"approve_{user_id}_{application_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{user_id}_{application_id}")
        ],
        [
            InlineKeyboardButton(text="📞 Bog'lanish", callback_data=f"contact_{user_id}"),
            InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"delete_{application_id}")
        ]
    ])

def admin_question_buttons(user_id: int, question_id: int):
    """Кнопки для вопросов"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💬 Ответить", callback_data=f"answer_question_{user_id}_{question_id}"),
            InlineKeyboardButton(text="✅ Отвечено", callback_data=f"question_done_{question_id}")
        ],
        [
            InlineKeyboardButton(text="📞 Связаться", callback_data=f"contact_{user_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_question_{question_id}")
        ]
    ])