import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN, DATABASE_URL
from handlers import commands, callbacks
from database.db import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
commands.register_handlers(dp)
callbacks.register_handlers(dp)


async def on_startup(dp):
    """Срабатывает при запуске бота"""
    logger.info("Бот запущен")
    await init_db()
    await bot.send_message(
        chat_id=123456789,  # Замени на свой ID (если нужно)
        text="✅ Бот успешно запущен!"
    )


async def on_shutdown(dp):
    """Срабатывает при остановке бота"""
    logger.info("Бот остановлен")
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )