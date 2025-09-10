# ============================================
# 🔹 handlers/start.py — /start buyrug'i va til tanlash
# ============================================

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboards.language_menu import language_menu
from keyboards.main_menu import main_menu
from data.languages import user_languages
from data.admins import is_admin

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
async def language_selected_handler(call: types.CallbackQuery):
    """
    Yangi tilni tanlaganda
    """
    user_id = call.from_user.id
    data = call.data
    lang = data.split("_")[1]  # ru, uz, en
    
    # Tilni saqlash
    user_languages[user_id] = lang
    
    # Tasdiqlash xabari
    confirm_texts = {
        "ru": "✅ <b>Язык изменен на Русский!</b>\n\nВыберите нужный раздел:",
        "uz": "✅ <b>Til O'zbekchaga o'zgartirildi!</b>\n\nKerakli bo'limni tanlang:",
        "en": "✅ <b>Language changed to English!</b>\n\nChoose a section:"
    }
    
    # Salomlashish matnlari
    greetings = {
        "ru": "👋 <b>Добро пожаловать в Учебный Центр!</b>\n\nВыберите нужный раздел:",
        "uz": "👋 <b>O'quv markazimizga xush kelibsiz!</b>\n\nKerakli bo'limni tanlang:",
        "en": "👋 <b>Welcome to our Learning Center!</b>\n\nChoose a section:"
    }
    
    await call.message.answer(confirm_texts[lang])
    await call.message.answer(greetings[lang], reply_markup=main_menu(lang))
    await call.answer()
    
# ==============================
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
    
    # Получаем статистику напрямую
    from data.db import get_statistics, get_user_count
    
    stats = get_statistics()
    users_stats = get_user_count()
    lang = user_languages.get(message.from_user.id, "ru")
    
    # Форматируем популярные курсы
    popular_courses = ""
    for course, count in stats['popular_courses']:
        popular_courses += f"• {course}: {count}\n"
    
    # Считаем заявки и вопросы за 7 дней
    app_last_7_days = sum(count for _, count in stats['applications_last_7_days'])
    quest_last_7_days = sum(count for _, count in stats['questions_last_7_days'])
    
    # Тексты для статистики
    stats_texts = {
        "ru": {
            "title": "📊 <b>СТАТИСТИКА БОТА</b>\n\n",
            "users": "👥 <b>Пользователи:</b>\n"
                    "• Всего пользователей: {total_users}\n"
                    "• Подали заявки: {applications_users}\n"
                    "• Задали вопросы: {questions_users}\n\n",
            "applications": "📝 <b>Заявки:</b>\n"
                           "• Всего заявок: {total_applications}\n"
                           "• Ожидают: {pending_applications}\n"
                           "• Одобрены: {approved_applications}\n"
                           "• Отклонены: {rejected_applications}\n\n",
            "questions": "❓ <b>Вопросы:</b>\n"
                        "• Всего вопросов: {total_questions}\n"
                        "• Ожидают ответа: {pending_questions}\n"
                        "• Ответили: {answered_questions}\n\n",
            "recent": "📈 <b>Активность за 7 дней:</b>\n"
                     "• Заявок: {app_last_7_days}\n"
                     "• Вопросов: {quest_last_7_days}\n\n",
            "popular": "🎯 <b>Популярные курсы:</b>\n{popular_courses}"
        },
        "uz": {
            "title": "📊 <b>BOT STATISTIKASI</b>\n\n",
            "users": "👥 <b>Foydalanuvchilar:</b>\n"
                    "• Jami foydalanuvchilar: {total_users}\n"
                    "• Ariza yuborganlar: {applications_users}\n"
                    "• Savol berganlar: {questions_users}\n\n",
            "applications": "📝 <b>Arizalar:</b>\n"
                           "• Jami arizalar: {total_applications}\n"
                           "• Kutayotgan: {pending_applications}\n"
                           "• Qabul qilingan: {approved_applications}\n"
                           "• Rad etilgan: {rejected_applications}\n\n",
            "questions": "❓ <b>Savollar:</b>\n"
                        "• Jami savollar: {total_questions}\n"
                        "• Javob kutayotgan: {pending_questions}\n"
                        "• Javob berilgan: {answered_questions}\n\n",
            "recent": "📈 <b>7 kunlik faollik:</b>\n"
                     "• Arizalar: {app_last_7_days}\n"
                     "• Savollar: {quest_last_7_days}\n\n",
            "popular": "🎯 <b>Mashhur kurslar:</b>\n{popular_courses}"
        },
        "en": {
            "title": "📊 <b>BOT STATISTICS</b>\n\n",
            "users": "👥 <b>Users:</b>\n"
                    "• Total users: {total_users}\n"
                    "• Applied: {applications_users}\n"
                    "• Asked questions: {questions_users}\n\n",
            "applications": "📝 <b>Applications:</b>\n"
                           "• Total applications: {total_applications}\n"
                           "• Pending: {pending_applications}\n"
                           "• Approved: {approved_applications}\n"
                           "• Rejected: {rejected_applications}\n\n",
            "questions": "❓ <b>Questions:</b>\n"
                        "• Total questions: {total_questions}\n"
                        "• Waiting: {pending_questions}\n"
                        "• Answered: {answered_questions}\n\n",
            "recent": "📈 <b>Activity last 7 days:</b>\n"
                     "• Applications: {app_last_7_days}\n"
                     "• Questions: {quest_last_7_days}\n\n",
            "popular": "🎯 <b>Popular courses:</b>\n{popular_courses}"
        }
    }
    
    # Формируем текст статистики
    text = (
        stats_texts[lang]["title"] +
        stats_texts[lang]["users"].format(
            total_users=users_stats['total_users'],
            applications_users=users_stats['applications_users'],
            questions_users=users_stats['questions_users']
        ) +
        stats_texts[lang]["applications"].format(
            total_applications=stats['total_applications'],
            pending_applications=stats['pending_applications'],
            approved_applications=stats['approved_applications'],
            rejected_applications=stats['rejected_applications']
        ) +
        stats_texts[lang]["questions"].format(
            total_questions=stats['total_questions'],
            pending_questions=stats['pending_questions'],
            answered_questions=stats['answered_questions']
        ) +
        stats_texts[lang]["recent"].format(
            app_last_7_days=app_last_7_days,
            quest_last_7_days=quest_last_7_days
        ) +
        stats_texts[lang]["popular"].format(popular_courses=popular_courses)
    )
    
    await message.answer(text)

# ==============================
# 🔘 Команда /panel (только для админов)
# ==============================
@router.message(Command("panel"))
async def panel_command(message: types.Message):
    """Админ-панель (только для админов)"""
    if not is_admin(message.from_user.id):
        lang = user_languages.get(message.from_user.id, "uz")
        await message.answer("⛔ <b>Sizda administrator huquqlari yo'q!</b>" if lang == "uz" else 
                            "⛔ <b>У вас нет прав администратора!</b>" if lang == "ru" else 
                            "⛔ <b>You don't have administrator rights!</b>")
        return
    
    # Создаем админ-панель напрямую
    from data.db import get_pending_applications_count, get_pending_questions_count
    from keyboards.admin_buttons import admin_panel_buttons
    
    pending_apps = get_pending_applications_count()
    pending_questions = get_pending_questions_count()
    
    text = f"👑 <b>Admin Panel</b>\n\n" \
           f"📊 <b>Statistika:</b>\n" \
           f"• 📝 Kutayotgan arizalar: {pending_apps}\n" \
           f"• ❓ Kutayotgan savollar: {pending_questions}\n\n" \
           f"🛠 <b>Boshqaruv:</b>\n" \
           f"Quyidagi tugmalar orqali boshqaring"
    
    await message.answer(text, reply_markup=admin_panel_buttons())