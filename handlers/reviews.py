# ============================================
# 🔹 handlers/reviews.py — раздел "Отзывы"
# ============================================

from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu
from data.languages import user_languages

# ==============================
# 📌 Роутер для раздела "Отзывы"
# ==============================
router = Router()

# ==============================
# 🔘 Обработка кнопки "Отзывы"
# ==============================
@router.callback_query(lambda c: c.data == "reviews")
async def reviews_handler(call: CallbackQuery):
    """
    Показывает отзывы студентов на выбранном языке
    """
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ru")  # язык по умолчанию

    texts = {
        "ru": "💬 <b>Отзывы студентов:</b>\n\n"
              "1. «Отличные преподаватели и удобное расписание!»\n"
              "2. «Курсы помогли мне освоить Python с нуля.»\n"
              "3. «Очень доволен обучением!»",
        "uz": "💬 <b>Talabalar fikrlari:</b>\n\n"
              "1. «Zo‘r o‘qituvchilar va qulay dars jadvali!»\n"
              "2. «Kurslar menga Pythonni 0 dan o‘rganishga yordam berdi.»\n"
              "3. «O‘qishdan juda mamnunman!»",
        "en": "💬 <b>Student Reviews:</b>\n\n"
              "1. «Great teachers and convenient schedule!»\n"
              "2. «The courses helped me learn Python from scratch.»\n"
              "3. «Very satisfied with the training!»"
    }

    # Отправляем сообщение с текстом и главное меню
    await call.message.answer(texts[lang], reply_markup=main_menu(lang))
    await call.answer()  # убираем "часики"