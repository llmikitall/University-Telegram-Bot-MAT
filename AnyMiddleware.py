from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from MessageLog import LogInConsole

from sql.SearchUserInformation import SearchAny


# Милдварь блокировки. Будет проверять, а является ли пользователь злоумышленником?
class AnyMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if SearchAny(event.chat.id, "usersList", "blocking") == "+":
            LogInConsole(f"[{event.chat.id} -> blocked] {event.text}")
            await event.answer("Вы, злоумышленник!")
            emojiID = int(SearchAny(event.chat.id, "userOfSetting", "emojiID"))
            stickerList = ("CAACAgIAAxkBAAEGgLtmftZhuQaquiJ_MeOmF2hqqp-cJQACGgADwDZPE4LbsLU8BkFXNQQ",
                           "CAACAgIAAxkBAAEJq9tnJQ17rsXsLvWBSWYRdm3Mn2I1UwAC_AgAAkxT0UgbO0Wq3lR40zYE",
                           "CAACAgIAAxkBAAEGgLtmftZhuQaquiJ_MeOmF2hqqp-cJQACGgADwDZPE4LbsLU8BkFXNQQ")
            await event.answer_sticker(stickerList[emojiID])
            return
        result = await handler(event, data)
        return result
