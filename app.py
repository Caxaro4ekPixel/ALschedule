from aiogram import executor
from loguru import logger

from loader import dp, bot
import handlers

        
async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    b = await dp.bot.get_me()
    logger.debug(f'Bot: {b.full_name} [@{b.username}]')
    logger.info("Start polling")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
