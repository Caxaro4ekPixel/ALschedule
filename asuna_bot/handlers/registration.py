"""
Ботом могут пользоваться только зарегистрированные пользователи.
Регистрация происходит путем пересылки админом любого сообщения пользователя,
если настройки приватности не позволяют добавить пользователя, 
просим на время изменить настройки приватности.
"""

from aiogram import Router
from aiogram.types import Message
from asuna_bot.filters.admins import AdminFilter

from asuna_bot.filters.chat_type import ChatTypeFilter
from asuna_bot.db.mongo import mongo

admin_router = Router()
admin_router.message.filter(AdminFilter(), ChatTypeFilter("private"))


@admin_router.message()
async def accept_user(msg: Message):
    if msg.forward_from:
        username = msg.forward_from.username
        user_id = msg.forward_from.id
        full_name = msg.forward_from.full_name        
        mongo.add_user(user_id, full_name, username)
        await msg.answer(f"{full_name} / @{username}\nДобавлен в базу! 👍")
        return
    
    if msg.forward_sender_name:
        name = msg.forward_sender_name
        await msg.answer(f"Не могу добавить {name} из-за настроек приватности 😔")