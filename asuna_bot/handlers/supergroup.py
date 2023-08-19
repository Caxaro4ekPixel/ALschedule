"""
Хендлер для отлова миграции в супергруппу,
при выдаче прав боту с пунктом "Анонимность"
запустится логика команды /start 
"""
from aiogram import Router, types, Bot
from asuna_bot.config import CONFIG    
from asuna_bot.filters.supergroup import MigrateToSupergroup
from asuna_bot.handlers.start import auto_search_title
from asuna_bot.main.chat_control import ChatControl
from asuna_bot.api.nya.rss_feed import RssFeed


supergroup_router = Router()

@supergroup_router.message(MigrateToSupergroup())
async def supergroup(message: types.Message):
    bot = Bot(token=CONFIG.bot.token)
    new_chat_id = message.migrate_to_chat_id
    await bot.send_message(new_chat_id, f"теперь это супергруппа, id={new_chat_id}")
    chat_obj = ChatControl(new_chat_id)
    
    await auto_search_title(message, new_chat_id)
    del bot