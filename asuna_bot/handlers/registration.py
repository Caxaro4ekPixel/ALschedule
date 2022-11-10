from aiogram import Router
from aiogram.types import Message
from asuna_bot.filters.admins import AdminFilter

from asuna_bot.filters.chat_type import ChatTypeFilter
from asuna_bot.db.mongo import add_user

admin_router = Router()
admin_router.message.filter(AdminFilter(), ChatTypeFilter("private"))

# Админы дают доступ
@admin_router.message()
async def accept_user(msg: Message):
    if not msg.forward_from:
        name = msg.forward_sender_name
        await msg.answer(f"Не могу добавить {name} из-за настроек приватности 😔")
        return
    
    username = msg.forward_from.username
    user_id = msg.forward_from.id
    full_name = msg.forward_from.full_name        
    add_user(user_id, full_name, username)
    await msg.answer(f"{full_name} / @{username}\nДобавлен в базу! 👍")