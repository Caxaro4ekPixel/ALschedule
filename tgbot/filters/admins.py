from aiogram.filters import Filter
from aiogram.types import Message
from tgbot.db.mongo import mongo
from tgbot.config import CONFIG


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in CONFIG.bot.admin_ids:
            return True
        return False


class AllowedUserFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in mongo.get_all_user_ids():
            return True
        return False