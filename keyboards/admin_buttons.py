# ============================================
# 🔹 keyboards/admin_buttons.py — administrator tugmalari
# ============================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_approve_buttons(user_id: int, application_id: int):
    """
    Administrator uchun tugmalar: qabul qilish yoki rad etish
    """
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