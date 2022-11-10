import logging
from aiogram import Bot, Dispatcher

from asuna_bot.handlers.registration import admin_router
# from tgbot.handlers.bind import bind_router
# from tgbot.handlers.raw import raw_router
from asuna_bot.config import CONFIG


def main() -> None:
    logging.basicConfig(
        # filename='log_file.log', 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level='INFO'
    )

    bot = Bot(token=CONFIG.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(admin_router)
    # dp.include_router(bind_router)
    # dp.include_router(raw_router)

    # from tgbot.schedulers.jobs import scheduler

    dp.run_polling(bot)
    

if __name__ == "__main__":
    main()