from datetime import datetime

from aiogram import Router, Bot
from aiogram.types import Message, Document, File, ReactionTypeEmoji
from aiogram.filters import CommandStart, Command

from monitoring_bot.database import Database
from monitoring_bot.constants import (admin_id,
                                      log,
                                      first_bot_user_private_chat_message,
                                      greetings_message,
                                      banned_or_left_user_message)
from monitoring_bot.handlers.filters import IsPrivateChatFilter, IsUserSubscribed, IsUserNotSubscribedLeftOrBanned
from monitoring_bot.utils import create_admin_new_message_keyboard


async def react_on_unban(message: Message, bot: Bot) -> None:
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def hello(message: Message) -> None:
    log.info(f"User {message.from_user.username} start dialog with a bot")
    update_status = await Database.update_user(user_id=message.from_user.id, has_chat_with_bot=True)
    if update_status is False:
        text = first_bot_user_private_chat_message
        await Database.insert_into_users(user_id=message.from_user.id,
                                         username=message.from_user.username,
                                         enter_date=datetime.now(),
                                         status='not_a_member',
                                         has_chat_with_bot=True)
    else:
        text = greetings_message
    await message.answer(text)


async def resend_to_admin(data: Message | Document | File, bot: Bot) -> None:
    # TODO: add documents and other stuff
    await Database.update_user(user_id=data.from_user.id, has_chat_with_bot=True)
    await bot.set_message_reaction(chat_id=data.from_user.id,
                                   message_id=data.message_id,
                                   reaction=[ReactionTypeEmoji(emoji="👌")]
                                   )
    user = "👤: @" + data.from_user.username
    if data.photo:
        text = f"{data.caption}\n\n{user}" if data.caption else user

        await bot.send_photo(chat_id=admin_id,
                             photo=data.photo[0].file_id,
                             caption=text,
                             reply_markup=create_admin_new_message_keyboard(data.from_user.id),
                             disable_notification=True
                             )
    else:
        text = f"{data.text}\n\n{user}"
        await bot.send_message(chat_id=admin_id,
                               text=text,
                               reply_markup=create_admin_new_message_keyboard(data.from_user.id),
                               disable_notification=True
                               )


async def send_message_to_subscribe(message: Message) -> None:
    await message.answer(text=banned_or_left_user_message)


router = Router()
router.message.register(react_on_unban, Command('unban'))
router.message.register(send_message_to_subscribe, IsUserNotSubscribedLeftOrBanned())
router.message.register(hello, CommandStart())
router.message.register(resend_to_admin,
                        IsPrivateChatFilter(),
                        IsUserSubscribed(),
                        lambda msg: msg.from_user.id != admin_id)

