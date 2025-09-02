from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from MessageLog import LogInConsole
from aiogram.types import TelegramObject, Message

with open("doc/AdminID.txt") as file:
    ADMIN = int(file.read().strip())
file.close()


class AdminMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:

        if event.chat.id != ADMIN:
            LogInConsole(f"[X][{event.chat.id}]{event.text}")
            await event.answer("У Вас нет прав администратора.")
            return
        result = await handler(event, data)
        return result
