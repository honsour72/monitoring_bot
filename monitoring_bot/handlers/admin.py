import re
from typing import Sequence

from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from monitoring_bot.constants import (log,
                                      ban_user_query,
                                      cancel_ban_user,
                                      want_to_ban_user_regexp,
                                      ban_user_regexp,
                                      write_an_answer_regexp,
                                      admin_id,
                                      chat_id,
                                      channel_id,
                                      admin_appreciates_it,
                                      admin_disrespects_it,
                                      admin_saw_it)
from monitoring_bot.database import Database, User
from monitoring_bot.handlers.filters import IsPrivateChatFilter, UserIdOrUsernameFilter
from monitoring_bot.utils import admin_thumbs_up, admin_thumbs_down, admin_read, move_to_trash

user_ids_to_answer = []


async def start(message: Message) -> None:
    text = "Что будем делать?"
    await message.answer(text)


async def reacts(query: CallbackQuery, bot: Bot) -> None:
    await query.answer('reacted!')
    if query.data.endswith('down'):
        text = admin_disrespects_it
    elif query.data.endswith('up'):
        text = admin_appreciates_it
    else:
        text = admin_saw_it

    if query.message.caption:
        message_text = query.message.caption
    else:
        message_text = query.message.text
    username = message_text.split('@')[-1]
    writers: Sequence[User] = await Database.select_from_users(where={'username': username})
    await bot.send_message(chat_id=writers[0].user_id, text=text)


async def write_a_message_to_user(query: CallbackQuery) -> None:
    await query.answer('Write a message to user...')
    user_id = int(query.data.split('_')[-1])
    user_ids_to_answer.append(user_id)
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data=cancel_ban_user)
    await query.message.answer(text="Напишите сообщение юзеру", reply_markup=builder.as_markup())


async def remove_user_message(query: CallbackQuery, bot: Bot) -> None:
    await query.answer('remove message...')
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)


async def want_to_ban_user(query: CallbackQuery) -> None:
    await query.answer('Do you really want to ban this user?')
    user_id = query.data.split('_')[-1]
    text = "Вы уверены что хотите ограничить челу доступ на канал/чат?"
    builder = InlineKeyboardBuilder()
    builder.button(text="✅", callback_data=ban_user_query.format(user_id))
    builder.button(text="❌", callback_data=cancel_ban_user)
    await query.message.answer(text=text, reply_markup=builder.as_markup())


async def ban_user(query: CallbackQuery, bot: Bot) -> None:
    user_id = int(query.data.split('_')[-1])
    await query.answer(f'Banning user with ID: {user_id}')
    # TODO: understand how to get chat_id or channel_id
    await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
    await bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
    await Database.update_user(user_id, status='banned')
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    log.success(f"User with ID: {user_id} has been banned in channel ({channel_id}) and chat ({chat_id})")


async def cancel_banning(query: CallbackQuery, bot: Bot) -> None:
    await bot.delete_message(query.message.chat.id, query.message.message_id)


async def resend_to_user(message: Message) -> None:
    user_id = user_ids_to_answer.pop()
    await message.send_copy(chat_id=user_id)


async def unban_user(message: Message, user_id: int | None, bot: Bot) -> None:
    if user_id is None:
        log.debug(f"Admin try to unban user with id={user_id}, but there is no user with such id -> aborting")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(text=f'Юзера с таким {user_id} не существует')
        return

    await Database.update_user(user_id=user_id, status='not_a_member')
    await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)  # for the chat
    await bot.unban_chat_member(chat_id=channel_id, user_id=user_id)  # for the channel
    log.success(f"User with ID={user_id} unbanned from chat AND channel")


async def show_banned(message: Message) -> None:
    users = await Database.select_from_users(where={'status': 'banned'}) or []
    text = "\n".join([f"@{user.username}" for user in users])
    await message.answer(text=text)


router = Router()

router.message.register(start, CommandStart(), lambda msg: msg.from_user.id == admin_id)
router.message.register(unban_user,
                        Command('unban'),
                        UserIdOrUsernameFilter(),
                        lambda msg: msg.from_user.id == admin_id)
router.message.register(show_banned, Command('show_banned'), lambda msg: msg.from_user.id == admin_id)
router.callback_query.register(reacts, lambda q: q.data in (admin_thumbs_up, admin_thumbs_down, admin_read))
router.callback_query.register(write_a_message_to_user, lambda q: re.match(write_an_answer_regexp, q.data))
router.callback_query.register(remove_user_message, lambda q: q.data == move_to_trash)
router.callback_query.register(want_to_ban_user, lambda q: re.match(want_to_ban_user_regexp, q.data))
router.callback_query.register(ban_user, lambda q: re.match(ban_user_regexp, q.data))
router.callback_query.register(cancel_banning, lambda q: q.data == cancel_ban_user)
router.message.register(resend_to_user, IsPrivateChatFilter(), lambda msg: msg.from_user.id == admin_id)
