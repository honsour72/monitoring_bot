from datetime import datetime
from typing import Any

from aiogram import Bot, Router, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER

from monitoring_bot.constants import (log,
                                      these_buttons_not_for_you,
                                      congratulations,
                                      correct_new_member_answer,
                                      new_member_answer,
                                      new_user_approve_message,
                                      user_passes_chat_verification_message)
from monitoring_bot.database import Database
from monitoring_bot.utils import create_check_new_member_keyboard, send_note_to_admin, get_text_about_leaver


async def notify_admin_about_leaver(chat_leaver: types.ChatMemberUpdated, bot: Bot) -> Any:
    text = await get_text_about_leaver(chat_leaver)
    log.info(text)

    await bot.ban_chat_member(chat_id=chat_leaver.chat.id, user_id=chat_leaver.from_user.id)

    update_status = await Database.update_user(chat_leaver.from_user.id, status='left', leave_date=datetime.now())
    if not update_status:
        await Database.insert_into_users(user_id=chat_leaver.from_user.id,
                                         username=chat_leaver.from_user.username,
                                         enter_date=datetime.now(),
                                         leave_date=datetime.now(),
                                         status='banned')
    await send_note_to_admin(bot, text)


async def handle_new_member(new_chat_member: types.ChatMemberUpdated, bot: Bot, newbies: list) -> None:
    if not new_chat_member.chat.username:
        newbies.append(new_chat_member.from_user.id)
        message = new_user_approve_message.format(new_chat_member.from_user.username)
        log.info(f"User @{new_chat_member.from_user.username} enter the chat")
        await new_chat_member.answer(text=message,
                                     reply_markup=create_check_new_member_keyboard(),
                                     disable_notification=True)
    else:
        log.info(f"User @{new_chat_member.from_user.username} enter the channel @{new_chat_member.chat.username}")
        await send_note_to_admin(bot, text=f"На канале новый подписчек @{new_chat_member.from_user.username}")
        success_insertion = await Database.insert_into_users(user_id=new_chat_member.from_user.id,
                                                             username=new_chat_member.from_user.username,
                                                             enter_date=datetime.now(),
                                                             status='member')
        # User can write bot at first, so we just need to update it status
        if not success_insertion:
            await Database.update_user(user_id=new_chat_member.from_user.id, status='member', leave_date=None)


async def check_new_member_is_human(query: types.CallbackQuery, bot: Bot, newbies: list) -> None:
    if query.from_user.id in newbies:
        await query.answer(congratulations)
        del newbies[0]
        if query.data == correct_new_member_answer:
            log.success(user_passes_chat_verification_message.format(query.from_user.username))
            await query.message.delete()
            await send_note_to_admin(bot, user_passes_chat_verification_message.format(query.from_user.username))
            success_insertion = await Database.insert_into_users(user_id=query.from_user.id,
                                                                 username=query.from_user.username,
                                                                 enter_date=datetime.now(),
                                                                 status='member')
            if success_insertion:
                log.exception(f"Strange: @{query.from_user.username} subscribe to chat at first, but not to channel")
            else:
                await Database.update_user(user_id=query.from_user.id, status='member')

        else:
            log.info(f"Ban @{query.from_user.username} in chat forever")
            await query.message.delete()
            await bot.ban_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
            await Database.update_user(query.from_user.id, status='banned')
    else:
        await query.answer(these_buttons_not_for_you)


router = Router()
router.chat_member.register(notify_admin_about_leaver, ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
router.chat_member.register(handle_new_member, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.callback_query.register(check_new_member_is_human, lambda answer: answer.data in new_member_answer)
