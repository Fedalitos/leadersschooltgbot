# ============================================
# 🔹 handlers/register.py — "Ro'yxatdan o'tish" bo'limi
# ============================================

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu
from keyboards.admin_buttons import admin_approve_buttons
from data.languages import user_languages
from data.db import save_application
from data.admins import ADMINS
from handlers.admin import notify_admins_new_application

# Administrator guruhining IDsi (o'zgartiring)
ADMIN_GROUP_ID = -4931417098

router = Router()

# Ariza to'ldirish uchun holatlar
class RegistrationStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_course = State()
    waiting_for_phone = State()

# Matnlar turli tillarda
registration_texts = {
    "ru": {
        "start": "📝 <b>Запись на курсы:</b>\n\nПожалуйста, отправьте ваше ФИО:",
        "full_name_example": "Пример: Иван Иванов",
        "course": "🎓 <b>Выберите курс:</b>\n\nАнглийский язык, Русский язык, Математика, IT, Биология, SAT Подготовка",
        "phone": "📱 <b>Отправьте ваш номер телефона:</b>\n\nПример: +998901234567",
        "success": "✅ <b>Ваша заявка отправлена!</b>\n\nАдминистратор свяжется с вами в ближайшее время.\nНомер заявки: #{}\n\n📞 Для связи: {}"
    },
    "uz": {
        "start": "📝 <b>Kurslarga ro'yxatdan o'tish:</b>\n\nIltimos, ismingizni yuboring:",
        "full_name_example": "Namuna: Alisher Navoiy",
        "course": "🎓 <b>Kursni tanlang:</b>\n\nIngliz tili, Rus tili, Matematika, IT, Biologiya, SAT Tayyorgarlik",
        "phone": "📱 <b>Telefon raqamingizni yuboring:</b>\n\nNamuna: +998901234567",
        "success": "✅ <b>Arizangiz yuborildi!</b>\n\nAdministrator tez orada siz bilan bog'lanadi.\nAriza raqami: #{}\n\n📞 Bog'lanish uchun: {}"
    },
    "en": {
        "start": "📝 <b>Register for courses:</b>\n\nPlease send your full name:",
        "full_name_example": "Example: John Smith",
        "course": "🎓 <b>Choose a course:</b>\n\nEnglish Language, Russian Language, Mathematics, IT, Biology, SAT Preparation",
        "phone": "📱 <b>Send your phone number:</b>\n\nExample: +998901234567",
        "success": "✅ <b>Your application has been sent!</b>\n\nAn administrator will contact you shortly.\nApplication number: #{}\n\n📞 For contact: {}"
    }
}

# ==============================
# 🔘 "Ro'yxatdan o'tish" tugmasini bosganda
# ==============================
@router.callback_query(lambda c: c.data == "register")
async def register_start(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    lang = user_languages.get(user_id, "uz")

    text = registration_texts[lang]["start"]
    await call.message.answer(text)
    await state.set_state(RegistrationStates.waiting_for_full_name)
    await call.answer()

# ==============================
# 🔘 Ism-familiyani qabul qilish
# ==============================
@router.message(RegistrationStates.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")
    
    text = registration_texts[lang]["course"]
    await message.answer(text)
    await state.set_state(RegistrationStates.waiting_for_course)

# ==============================
# 🔘 Kursni qabul qilish
# ==============================
@router.message(RegistrationStates.waiting_for_course)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")
    
    text = registration_texts[lang]["phone"]
    await message.answer(text)
    await state.set_state(RegistrationStates.waiting_for_phone)

# ==============================
# 🔘 Telefon raqamini qabul qilish va arizani yuborish
# ==============================
@router.message(RegistrationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")
    
    full_name = user_data['full_name']
    course = user_data['course']
    phone = message.text

    # Arizani bazaga saqlash
    application_id = save_application(user_id, full_name, course, phone, lang)
    
    # Уведомляем администраторов
    user_info = {
        'full_name': full_name,
        'course': course,
        'phone': phone
    }
    await notify_admins_new_application(message.bot, application_id, user_info)

    # Administrator guruhiga yuborish
    admin_text = f"🆕 <b>Yangi kurs arizasi</b>\n\n" \
                 f"👤 <b>Foydalanuvchi:</b> {full_name}\n" \
                 f"📚 <b>Kurs:</b> {course}\n" \
                 f"📱 <b>Telefon:</b> {phone}\n" \
                 f"🆔 <b>Telegram ID:</b> {user_id}\n" \
                 f"👤 <b>Username:</b> @{message.from_user.username if message.from_user.username else 'Yo\'q'}\n" \
                 f"📋 <b>Ariza №:</b> {application_id}"

    try:
        await message.bot.send_message
    except Exception as e:
        print(f"Error sending message to admin group: {e}")