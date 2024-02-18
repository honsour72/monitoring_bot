from typing import Type, Union, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from monitoring_bot.database import Database, User


class IsPrivateChatFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type not in ("group", "supergroup")


class IsUserSubscribed(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user: Type[User] = await Database.select_from_users(user_id=user_id)
        return user and user.status == 'member'


class IsUserNotSubscribedLeftOrBanned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user: Type[User] = await Database.select_from_users(user_id=user_id)
        return user and user.status in ('banned', 'left')


class UserIdOrUsernameFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, dict[str, Any]]:
        cmd, username = message.text.split()
        users = await Database.select_from_users(where={'username': username})
        if users:
            user_id = users[0].user_id
        else:
            user_id = None
        return {'user_id': user_id}
