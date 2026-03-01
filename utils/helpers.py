"""
Вспомогательные функции для бота
"""

def format_user_info(user: dict) -> str:
    """Форматирование информации о пользователе"""
    return f"👤 {user.get('first_name', 'Неизвестный')} (@{user.get('username', 'N/A')})"

def escape_markdown(text: str) -> str:
    """Экранирование символов Markdown"""
    markdown_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in markdown_chars:
        text = text.replace(char, f'\{char}')
    return text