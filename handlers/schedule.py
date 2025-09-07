# ============================================
# 🔹 handlers/schedule.py — раздел "Расписание"
# ============================================

from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu
from data.languages import user_languages

# ==============================
# 📌 Роутер для раздела "Расписание"
# ==============================
router = Router()

# ==============================
# 🔘 Обработка кнопки "Расписание"
# ==============================
@router.callback_query(lambda c: c.data == "schedule")
async def schedule_handler(call: CallbackQuery):
    """
    Показывает расписание занятий на выбранном языке
    """
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ru")  # язык по умолчанию

    texts = {
        "ru": "🕒 <b>Расписание занятий:</b>\n\n"
              "Понедельник — IT: 10:00-12:00\n"
              "Вторник — Математика: 14:00-16:00\n"
              "Среда — Языковые курсы: 12:00-14:00",
        "uz": "🕒 <b>Dars jadvali:</b>\n\n"
              "Dushanba — IT: 10:00-12:00\n"
              "Seshanba — Matematika: 14:00-16:00\n"
              "Chorshanba — Tillar kurslari: 12:00-14:00",
        "en": "🕒 <b>Schedule:</b>\n\n"
              "Monday — IT: 10:00-12:00\n"
              "Tuesday — Math: 14:00-16:00\n"
              "Wednesday — Language Courses: 12:00-14:00"
    }

    # Отправляем сообщение с текстом и главное меню
    await call.message.answer(texts[lang], reply_markup=main_menu(lang))
    await call.answer()  # убираем "часики"