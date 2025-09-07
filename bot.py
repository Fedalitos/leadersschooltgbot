import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# ==============================
# 🔑 Bot tokeni BotFatherdan
# ✅ ИЗМЕНЕНИЕ: Безопасное получение токена из переменных окружения
# ==============================
TOKEN = os.getenv("BOT_TOKEN")  # Токен теперь берется из настроек Render

# ==============================
# ✅ Botni ishga tushirish
# ==============================
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# ==============================
# 🔹 Foydalanuvchi tillari saqlash joyi
# ==============================
from data.languages import user_languages # Импорт можно оставить здесь

async def main():
    # ==============================
    # 🔹 Routerlarni import qilish (ИМПОРТИРУЕМ ЗДЕСЬ, чтобы избежать циклов)
    # ==============================
    from handlers.start import router as start_router
    from handlers.courses import router as courses_router
    from handlers.schedule import router as schedule_router
    from handlers.register import router as register_router
    from handlers.reviews import router as reviews_router
    from handlers.contacts import router as contacts_router
    from handlers.admin import router as admin_router
    from handlers.language import router as language_router

    # ==============================
    # 🔹 Routerlarni ulash
    # ==============================
    dp.include_router(start_router)
    dp.include_router(courses_router)
    dp.include_router(schedule_router)
    dp.include_router(register_router)
    dp.include_router(reviews_router)
    dp.include_router(contacts_router)
    dp.include_router(admin_router)
    dp.include_router(language_router)

    # Инициализация БД (если нужно)
    from data.db import init_db
    init_db()

    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())