from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db import get_user_count, set_user_data, get_user_data
import logging

logger = logging.getLogger(__name__)


class CallbackStates(StatesGroup):
    waiting_for_feedback = State()


async def cb_stats(callback_query: types.CallbackQuery):
    """Обработчик кнопки статистики"""
    user_count = await get_user_count()
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"📊 **Статистика бота:**\n\n"
        f"👥 Всего пользователей: {user_count}",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("◀️ Назад", callback_data="back")
        )
    )


async def cb_write_msg(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки написания сообщения"""
    await callback_query.answer()
    await callback_query.message.edit_text("📝 Напиши свое сообщение:")
    await state.set_state(CallbackStates.waiting_for_feedback)


async def process_feedback(message: types.Message, state: FSMContext):
    """Обработка отзыва пользователя"""
    user_id = message.from_user.id
    
    await set_user_data(user_id, "last_feedback", message.text)
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="back"))
    
    await message.reply(
        "✅ Спасибо за обратную связь! Твое сообщение сохранено.",
        reply_markup=keyboard
    )
    await state.finish()


async def cb_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки возврата в главное меню"""
    await state.finish()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    keyboard.add(types.InlineKeyboardButton("💬 Написать сообщение", callback_data="write_msg"))
    
    await callback_query.answer()
    await callback_query.message.edit_text(
        "🏠 Главное меню\n\nВыбери действие:",
        reply_markup=keyboard
    )


def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков callbacks"""
    dp.register_callback_query_handler(cb_stats, lambda c: c.data == "stats")
    dp.register_callback_query_handler(cb_write_msg, lambda c: c.data == "write_msg")
    dp.register_callback_query_handler(cb_back, lambda c: c.data == "back")
    
    dp.register_message_handler(
        process_feedback,
        state=CallbackStates.waiting_for_feedback
    )