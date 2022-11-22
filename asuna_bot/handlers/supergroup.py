"""
Хендлер для отлова миграции в супергруппу,
при выдаче прав боту с пунктом "Анонимность"
запустится логика команды /start 
"""
from aiogram import Router, types, Bot
from asuna_bot.config import CONFIG    
from asuna_bot.filters.supergroup import MigrateToSupergroup

supergroup_router = Router()

@supergroup_router.message(MigrateToSupergroup())
async def supergroup(message: types.Message):
    bot = Bot(token=CONFIG.bot.token)
    new_chat_id = message.migrate_to_chat_id
    # TODO допилить логику команды /start 
    await bot.send_message(new_chat_id, f"теперь это супергруппа, id={new_chat_id}")
    del bot