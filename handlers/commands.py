from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db import add_user, get_user_count
import logging

logger = logging.getLogger(__name__)


class UserStates(StatesGroup):
    waiting_for_message = State()


async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    await add_user(user_id, username, first_name)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    keyboard.add(types.InlineKeyboardButton("💬 Написать сообщение", callback_data="write_msg"))
    
    await message.reply(
        f"👋 Привет, {first_name}!\n\n"
        f"Я Telegram бот, готовый к работе.\n\n"
        f"Выбери действие:",
        reply_markup=keyboard
    )


async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
🤖 **Доступные команды:**

/start - Начать работу с ботом
/help - Справка
/stats - Показать статистику
/feedback - Отправить отзыв

Нажимай на кнопки ниже для взаимодействия! 👇
    """
    await message.reply(help_text, parse_mode="Markdown")


async def cmd_stats(message: types.Message):
    """Обработчик команды /stats"""
    user_count = await get_user_count()
    await message.reply(
        f"📊 **Статистика бота:**\n\n"
        f"👥 Всего пользователей: {user_count}",
        parse_mode="Markdown"
    )


def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков команд"""
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_stats, commands=['stats'])