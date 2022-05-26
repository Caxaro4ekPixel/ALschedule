from aiogram import Router, types, html

from keyboards.start_kb import get_start_kb

router = Router()


@router.inline_query()
async def inline_handler(query: types.InlineQuery):
    result = types.InlineQueryResultArticle(
        id=".",
        title=f"Your ID is {query.from_user.id}",
        description="Tap to send your ID to current chat",
        input_message_content=types.InputTextMessageContent(
            message_text=f"My Telegram ID is {html.code(query.from_user.id)}"
        )
    )
    await query.answer(results=[result], cache_time=3600, is_personal=True)
