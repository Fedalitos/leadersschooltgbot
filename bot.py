import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from storage import storage

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Bot token
TOKEN = os.getenv("BOT_TOKEN")

# Создаем бота с увеличенными таймаутами
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    timeout=60.0,  # Увеличиваем таймаут до 60 секунд
    connect_timeout=60.0,
    read_timeout=60.0,
    write_timeout=60.0
)

dp = Dispatcher(storage=storage)

# 🔹 HTTP сервер для health checks
async def handle_health_check(request):
    return web.Response(text="✅ Bot is alive and running!")

async def start_http_server():
    """Запуск HTTP сервера для Render"""
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    app.router.add_get('/health', handle_health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Используем порт из переменной окружения или 8080 по умолчанию
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print(f"✅ HTTP server started on port {port}")
    return runner

async def main():
    # 🔹 Запускаем HTTP сервер
    http_runner = await start_http_server()
    
    # 🔹 Импортируем и подключаем роутеры
    from handlers.admin import router as admin_router
    from handlers.start import router as start_router
    from handlers.courses import router as courses_router
    from handlers.schedule import router as schedule_router
    from handlers.register import router as register_router
    from handlers.reviews import router as reviews_router
    from handlers.contacts import router as contacts_router
    from handlers.language import router as language_router
    from handlers.question import router as question_router
    from handlers.group_moderation import router as group_moderation_router
    from handlers.broadcast import router as broadcast_router

    dp.include_router(admin_router)
    dp.include_router(question_router)
    dp.include_router(start_router)
    dp.include_router(courses_router)
    dp.include_router(schedule_router)
    dp.include_router(register_router)
    dp.include_router(reviews_router)
    dp.include_router(contacts_router)
    dp.include_router(language_router)
    dp.include_router(group_moderation_router)
    dp.include_router(broadcast_router)

    # 🔹 Инициализация БД
    from data.db import init_db
    init_db()
    
    # 🔹 Инициализация группы БД
    from handlers.group_moderation import init_group_db
    init_group_db()

    print("✅ Bot ishga tushdi...")
    
    # Добавляем задержку перед запуском бота
    await asyncio.sleep(5)
    
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"🔄 Попытка запуска бота #{attempt + 1}")
            await dp.start_polling(bot)
            break
            
        except Exception as e:
            logger.warning(f"⚠️ Ошибка (попытка {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"⏳ Повторная попытка через {retry_delay} секунд...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Экспоненциальная задержка
            else:
                logger.error("❌ Не удалось подключиться после всех попыток")
                # Не завершаем приложение, продолжаем работать с HTTP сервером
                while True:
                    await asyncio.sleep(3600)  # Спим час и продолжаем
                    
        finally:
        # Корректное завершение
            await http_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())