from aiogram.filters import Filter
from aiogram.types import Message

class MigrateToSupergroup(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.migrate_to_chat_id:
            return True
        return False