from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def courses_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с направлениями курсов и кнопкой "Назад"
    lang: "ru", "uz", "en"
    """
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Языковые Курсы", callback_data="dir_lang")],
            [InlineKeyboardButton(text="💻 IT Курсы", callback_data="dir_it")],
            [InlineKeyboardButton(text="🧮 Математика", callback_data="dir_math")],
            [InlineKeyboardButton(text="🔬 Биология", callback_data="dir_bio")],
            [InlineKeyboardButton(text="🎓 SAT Подготовка", callback_data="dir_sat")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")]
        ])
    elif lang == "uz":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Tillar Kurslari", callback_data="dir_lang")],
            [InlineKeyboardButton(text="💻 IT Kurslari", callback_data="dir_it")],
            [InlineKeyboardButton(text="🧮 Matematika", callback_data="dir_math")],
            [InlineKeyboardButton(text="🔬 Biologiya", callback_data="dir_bio")],
            [InlineKeyboardButton(text="🎓 SAT Tayyorgarlik", callback_data="dir_sat")],
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_main")]
        ])
    else:  # en
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Language Courses", callback_data="dir_lang")],
            [InlineKeyboardButton(text="💻 IT Courses", callback_data="dir_it")],
            [InlineKeyboardButton(text="🧮 Math", callback_data="dir_math")],
            [InlineKeyboardButton(text="🔬 Biology", callback_data="dir_bio")],
            [InlineKeyboardButton(text="🎓 SAT Preparation", callback_data="dir_sat")],
            [InlineKeyboardButton(text="🏠 Main menu", callback_data="back_main")]
        ])