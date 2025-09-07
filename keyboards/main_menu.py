# ============================================
# 🔹 keyboards/main_menu.py — asosiy menyu
# ============================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 📚 Asosiy menyu tarjima bilan
def main_menu(lang: str = "uz") -> InlineKeyboardMarkup:
    """
    InlineKeyboardMarkup ni tanlangan tilga qarab qaytaradi.
    lang: "ru", "uz" yoki "en"
    """
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Курсы", callback_data="courses")],
            [InlineKeyboardButton(text="🕒 Расписание", callback_data="schedule")],
            [InlineKeyboardButton(text="📝 Записаться", callback_data="register")],
            [InlineKeyboardButton(text="💬 Отзывы", callback_data="reviews")],
            [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_language")]
        ])
    elif lang == "uz":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Kurslar", callback_data="courses")],
            [InlineKeyboardButton(text="🕒 Dars jadvali", callback_data="schedule")],
            [InlineKeyboardButton(text="📝 Ro'yxatdan o'tish", callback_data="register")],
            [InlineKeyboardButton(text="💬 Fikrlar", callback_data="reviews")],
            [InlineKeyboardButton(text="📞 Kontaktlar", callback_data="contacts")],
            [InlineKeyboardButton(text="🌍 Tilni o'zgartirish", callback_data="change_language")]
        ])
    else:  # en
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Courses", callback_data="courses")],
            [InlineKeyboardButton(text="🕒 Schedule", callback_data="schedule")],
            [InlineKeyboardButton(text="📝 Register", callback_data="register")],
            [InlineKeyboardButton(text="💬 Reviews", callback_data="reviews")],
            [InlineKeyboardButton(text="📞 Contacts", callback_data="contacts")],
            [InlineKeyboardButton(text="🌍 Change language", callback_data="change_language")]
        ])