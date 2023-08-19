import asyncio
from aiogram import Bot, Dispatcher
from asuna_bot.handlers.registration import admin_router
from asuna_bot.handlers.start import start_router
from asuna_bot.handlers.supergroup import supergroup_router
from asuna_bot.handlers.ass_to_srt import convert_router
from asuna_bot.config import CONFIG


from motor.motor_asyncio import AsyncIOMotorClient
from asuna_bot.db.odm import __beanie_models__
from beanie import init_beanie


async def main() -> None:
    client = AsyncIOMotorClient(CONFIG.db.connection_string)
    await init_beanie(database=client.al_schedule, document_models=__beanie_models__)
    
    from migration import create_chat_list, create_release_list, create_user_list
    from asuna_bot.db.odm import Chat, Release, User
    # await User.insert_many(create_user_list())
    await Release.insert_many(create_release_list())
    # await Chat.insert_many(create_chat_list())

    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(supergroup_router)
    dp.include_router(convert_router)

    bot = Bot(token=CONFIG.bot.token, parse_mode='HTML')
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    from asuna_bot.utils import logging
    
    logging.setup()
    asyncio.run(main())