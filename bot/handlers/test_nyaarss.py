from loguru import logger
from aiogram import types

from aiogram.utils.markdown import hcode, hbold, hlink
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, nyaa_rss


@dp.message_handler(commands="nyaa")
async def cmd_nyaa(message: types.Message):
    query = message.get_args()
    torrents = await nyaa_rss.search_torrent(query, limit=2)
    logger.debug(torrents[-1])
    if torrents:
        torr = [f"{hcode(torrent.name)} - {hlink('magnet', torrent.magnet)}" for torrent in torrents]
        await message.answer(hbold("Найдено:\n") + "\n".join(torr))
    else:
        await message.answer('🧐Ничего не найдено🧐')
    