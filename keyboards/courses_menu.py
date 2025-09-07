# ============================================
# 🔹 keyboards/courses_menu.py — меню выбора направлений курсов
# ============================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def courses_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с направлениями курсов и кнопкой "Назад"
    lang: "ru", "uz", "en"
    """
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💻 IT Курсы", callback_data="dir_it")],
            [InlineKeyboardButton(text="🌍 Языковые Курсы", callback_data="dir_lang")],
            [InlineKeyboardButton(text="🧮 Математика", callback_data="dir_math")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")]
        ])
    elif lang == "uz":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💻 IT Kurslari", callback_data="dir_it")],
            [InlineKeyboardButton(text="🌍 Tillar Kurslari", callback_data="dir_lang")],
            [InlineKeyboardButton(text="🧮 Matematika", callback_data="dir_math")],
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")]
        ])
    else:  # en
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💻 IT Courses", callback_data="dir_it")],
            [InlineKeyboardButton(text="🌍 Language Courses", callback_data="dir_lang")],
            [InlineKeyboardButton(text="🧮 Math", callback_data="dir_math")],
            [InlineKeyboardButton(text="🏠 Main menu", callback_data="back_main")]
        ])
