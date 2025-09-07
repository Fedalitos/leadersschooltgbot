# ============================================
# 🔹 handlers/contacts.py — раздел "Контакты"
# ============================================

from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.main_menu import main_menu
from data.languages import user_languages

# ==============================
# 📌 Роутер для раздела "Контакты"
# ==============================
router = Router()

# ==============================
# 🔘 Обработка кнопки "Контакты"
# ==============================
@router.callback_query(lambda c: c.data == "contacts")
async def contacts_handler(call: CallbackQuery):
    """
    Показывает контактную информацию учебного центра на выбранном языке
    """
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "ru")  # язык по умолчанию

    texts = {
        "ru": "📞 <b>Контакты Учебного Центра:</b>\n\n"
              "📧 Email: info@school.com\n"
              "📱 Телефон: +998 90 123 45 67\n"
              "🌐 Сайт: www.school.com\n"
              "📍 Адрес: г. Ташкент, ул. Университетская, 10",
        "uz": "📞 <b>O‘quv Markazi Kontaktlari:</b>\n\n"
              "📧 Email: info@school.com\n"
              "📱 Telefon: +998 90 123 45 67\n"
              "🌐 Sayt: www.school.com\n"
              "📍 Manzil: Toshkent sh., Universitet ko‘chasi, 10",
        "en": "📞 <b>Learning Center Contacts:</b>\n\n"
              "📧 Email: info@school.com\n"
              "📱 Phone: +998 90 123 45 67\n"
              "🌐 Website: www.school.com\n"
              "📍 Address: Tashkent, Universitetskaya St., 10"
    }

    # Отправляем сообщение с текстом и главное меню
    await call.message.answer(texts[lang], reply_markup=main_menu(lang))
    await call.answer()  # убираем "часики"