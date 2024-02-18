import asyncio
from aiogram import Dispatcher, Bot

from .constants import token
from .handlers import admin, user, chat


async def main():
    dispatcher = Dispatcher()
    dispatcher.include_routers(admin.router, user.router, chat.router)

    bot = Bot(token)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, newbies=[])


if __name__ == "__main__":
    asyncio.run(main())
