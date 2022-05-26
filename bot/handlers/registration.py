from aiogram import Router, html, F, Bot
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.reg_kb import register_user, Registration, register_admin
from config import ADMIN_CHAT
from filters.chat_type import ChatTypeFilter
from db.mongo import add_new_user, get_user, add_user_to_whitelist

router = Router()


# Юзер запускает бота
@router.message(ChatTypeFilter(chat_type=["private"]), Command(commands=["start"]))
async def bot_start(message: Message):
    resp = add_new_user(
        user_id=message.from_user.id,
        user_name=message.from_user.username,
        full_name=message.from_user.full_name
    ) # Добавляем всех юзеров в бд
    
    if resp:
        await message.answer(
            "Привет! Для регистрации в боте нажми кнопку", 
            reply_markup=register_user(message.from_user.id)
        )

    else:
        await message.answer(
            f"Привет! {html.code(message.from_user.full_name)}, ты уже зарегистрирован."
        )


# Данные юзера прилетают в админский чат
@router.callback_query(Registration.filter(F.type == "user")) # Через колбек прокидываем id юзера
async def send_to_admin_chat(query: CallbackQuery, bot: Bot, callback_data: Registration):
    user = get_user(callback_data.chat_id) # Берем данные этого юзера из БД по его id (в колбеке может не влезть вся инфа поэтому так)
    if user:
        text = [
            "Пользователь",
            f"{user['full_name']} \ @{user['user_name']}",
            "Хочет зарегистрироваться, Принять?"
        ]
        await bot.send_message(ADMIN_CHAT, '\n'.join(text), reply_markup=register_admin(user["_id"]))
        await query.answer("Ожидайте подтверждения!")


# Админы дают доступ
@router.callback_query(Registration.filter(F.type == "accept"))
async def accept_user(query: CallbackQuery, bot: Bot, callback_data: Registration):
    user = get_user(callback_data.chat_id)
    add_user_to_whitelist(user["_id"], user["user_name"], user["full_name"])
    
    text = [
        "Пользователь",
        f"{user['full_name']} \ {user['user_name']}",
        "Добавлен в базу!"
    ]
    await bot.send_message(user["_id"], "Успешно!\nТеперь вы можете пользоваться ботом.")
    await query.answer("\n".join(text))


# Админы откланяют доступ
@router.callback_query(Registration.filter(F.type == "decline"))
async def decline_user(query: CallbackQuery, bot: Bot, callback_data: Registration):
    user = get_user(callback_data.chat_id)
    """ТУТ ДОБАВЛЯЕМ ЮЗЕРА В ЧС"""
    
    text = [
        "Пользователь",
        f"{user['full_name']} \ {user['user_name']}",
        "Добавлен в ЧС!"
    ]
    await bot.send_message(user["_id"], "Отказано!\nВы не можете пользоваться ботом.")
    await query.answer("\n".join(text))