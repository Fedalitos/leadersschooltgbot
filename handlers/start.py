# ============================================
# 🔹 handlers/start.py — /start buyrug'i va til tanlash
# ============================================

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboards.language_menu import language_menu
from keyboards.main_menu import main_menu
from data.languages import user_languages
from data.admins import is_admin  # Добавляем импорт

# ==============================
# 📌 Router for start logic
# ==============================
router = Router()

# ==============================
# 🌍 /start buyrug'i — til tanlash
# ==============================
@router.message(CommandStart())
async def start_command(message: types.Message):
    """
    Birinchi marta /start bosilganda til menyusini ko'rsatadi
    """
    text = "🌍 <b>Tilni tanlang / Выберите язык / Choose language:</b>"
    await message.answer(text, reply_markup=language_menu())

# ==============================
# 🌍 /language buyrug'i — tilni o'zgartirish
# ==============================
@router.message(Command("language"))
async def language_command(message: types.Message):
    """
    /language buyrug'i orqali tilni o'zgartirish
    """
    text = "🌍 <b>Tilni tanlang / Выберите язык / Choose language:</b>"
    await message.answer(text, reply_markup=language_menu())

# ==============================
# 🔘 Til tanlash tugmalarini qayta ishlash
# ==============================
@router.callback_query(lambda c: c.data.startswith("lang_"))
async def language_callback(call: types.CallbackQuery):
    """
    Til tugmalarini bosilganda asosiy menyuni tanlangan tilda ko'rsatadi
    """
    user_id = call.from_user.id
    data = call.data
    lang = data.split("_")[1]  # ru, uz, en
    
    # Tilni saqlash
    user_languages[user_id] = lang

    # Salomlashish matnlari
    greetings = {
        "ru": "👋 <b>Добро пожаловать в Учебный Центр!</b>\n\nВыберите нужный раздел:",
        "uz": "👋 <b>O'quv markazimizga xush kelibsiz!</b>\n\nKerakli bo'limni tanlang:",
        "en": "👋 <b>Welcome to our Learning Center!</b>\n\nChoose a section:"
    }

    # Asosiy menyuni tanlangan tilda ko'rsatish
    await call.message.answer(greetings[lang], reply_markup=main_menu(lang))
    await call.answer()
    
# 🔘 Команда /stats (только для админов)
# ==============================
@router.message(Command("stats"))
async def stats_command(message: types.Message):
    """Показать статистику бота (только для админов)"""
    if not is_admin(message.from_user.id):
        lang = user_languages.get(message.from_user.id, "uz")
        await message.answer("⛔ <b>Sizda administrator huquqlari yo'q!</b>" if lang == "uz" else 
                            "⛔ <b>У вас нет прав администратора!</b>" if lang == "ru" else 
                            "⛔ <b>You don't have administrator rights!</b>")
        return
    
    # Перенаправляем на обработчик в admin.py
    from handlers.admin import stats_command as admin_stats
    await admin_stats(message)