from random import choices, shuffle, choice

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from monitoring_bot.constants import (
    check_new_member_buttons_texts,
    correct_new_member_answer,
    wrong_new_member_answer,
    admin_id,
    admin_thumbs_up,
    admin_read,
    admin_thumbs_down,
    write_an_answer,
    move_to_trash,
    i_want_to_ban_user
)


def create_check_new_member_keyboard() -> InlineKeyboardMarkup:
    texts_copy = check_new_member_buttons_texts.copy()
    texts = []

    for _ in range(4):
        text = choice(texts_copy)
        texts.append(text)
        texts_copy.remove(text)

    buttons_data = [{"text": f"Я {t}", "callback_data": wrong_new_member_answer} for t in texts]
    buttons_data.append({"text": "Я человек", "callback_data": correct_new_member_answer})
    shuffle(buttons_data)
    builder = InlineKeyboardBuilder()

    for button_data in buttons_data:
        builder.button(**button_data)

    builder.adjust(3, 2)
    return builder.as_markup()


def create_admin_new_message_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        {"text": "👍", "callback_data": admin_thumbs_up},
        {"text": "👀", "callback_data": admin_read},
        {"text": "💬", "callback_data": write_an_answer.format(user_id)},
        {"text": "🗑", "callback_data": move_to_trash},
        {"text": "🚫", "callback_data": i_want_to_ban_user.format(user_id)},
        {"text": "👎", "callback_data": admin_thumbs_down},
    ]
    for button in buttons:
        builder.button(**button)

    return builder.as_markup()


async def send_note_to_admin(bot: Bot, text: str, mute: bool = True) -> None:
    await bot.send_message(chat_id=admin_id, text=text, disable_notification=mute)
