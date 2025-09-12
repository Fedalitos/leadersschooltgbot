import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import web
from storage import storage

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 🔹 Bot token
TOKEN = os.getenv("BOT_TOKEN")

# 🔹 Настройки прокси (если требуется)
PROXY_URL = os.getenv("PROXY_URL")  # Например: http://proxy.example.com:8080

# Создаем сессию с прокси
if PROXY_URL:
    session = AiohttpSession(
        proxy=PROXY_URL,
        timeout=60.0,
        connect_timeout=60.0
    )
    logger.info(f"✅ Используется прокси: {PROXY_URL}")
else:
    session = AiohttpSession(
        timeout=60.0,
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0
    )
    logger.info("✅ Прокси не используется")

# Создаем бота
bot = Bot(
    token=TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
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
    
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    logger.info(f"✅ HTTP server started on port {port}")
    return runner

async def check_telegram_access():
    """Проверка доступности Telegram API"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as test_session:
            async with test_session.get('https://api.telegram.org', timeout=10) as resp:
                if resp.status == 200:
                    logger.info("✅ Telegram API доступен")
                    return True
                else:
                    logger.warning(f"⚠️ Telegram API недоступен, статус: {resp.status}")
                    return False
    except Exception as e:
        logger.warning(f"⚠️ Ошибка проверки Telegram API: {e}")
        return False

async def main():
    # 🔹 Запускаем HTTP сервер
    http_runner = await start_http_server()
    
    # 🔹 Проверяем доступность Telegram API
    telegram_accessible = await check_telegram_access()
    
    if not telegram_accessible:
        logger.warning("⚠️ Telegram API недоступен. Бот будет работать только в режиме HTTP сервера")
    
    try:
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
        from handlers.group_register import router as group_register_router

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
        dp.include_router(group_register_router)

        # 🔹 Инициализация БД
        from data.db import init_db
        init_db()
        
        # 🔹 Инициализация группы БД
        from handlers.group_moderation import init_group_db
        init_group_db()

        logger.info("✅ Bot ishga tushdi...")
        
        # Если Telegram API недоступен, не пытаемся подключиться
        if not telegram_accessible:
            logger.info("🌐 Работаем только в режиме HTTP сервера")
            while True:
                await asyncio.sleep(3600)
            return
        
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Попытка запуска бота #{attempt + 1}")
                
                # Проверяем авторизацию
                try:
                    me = await bot.get_me()
                    logger.info(f"✅ Бот авторизован как: @{me.username}")
                except Exception as auth_error:
                    logger.warning(f"⚠️ Ошибка авторизации: {auth_error}")
                    raise
                
                # Запускаем polling
                await dp.start_polling(
                    bot, 
                    allowed_updates=dp.resolve_used_update_types(),
                    close_bot_session=False
                )
                break
                
            except Exception as e:
                logger.warning(f"⚠️ Ошибка (попытка {attempt + 1}/{max_retries}): {type(e).__name__}: {str(e)[:100]}...")
                
                if attempt < max_retries - 1:
                    current_delay = retry_delay * (attempt + 1)
                    logger.info(f"⏳ Повторная попытка через {current_delay} секунд...")
                    await asyncio.sleep(current_delay)
                else:
                    logger.error("❌ Не удалось подключиться после всех попыток")
                    break
                    
    except Exception as critical_error:
        logger.critical(f"💥 Критическая ошибка: {critical_error}")
    
    finally:
        # Бесконечный цикл для поддержания HTTP сервера
        logger.info("🔄 Переходим в режим поддержки HTTP сервера")
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            logger.info("🚫 Получен сигнал завершения")
        finally:
            await bot.session.close()
            await http_runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.critical(f"💥 Необработанная ошибка: {e}")