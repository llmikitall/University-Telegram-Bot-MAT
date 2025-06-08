from aiogram.filters import BaseFilter
from aiogram.types import Message
from sql.SearchUserInformation import SearchAny
from MessageLog import MessageInConsole

# StatusFilter - фильтр статуса для router.message(...). В init передаётся (статус №1), с которым допускается
# пользователь. В call сравнение (статуса №1) с текущим статусом пользователя. Если статусы равны - пользователю
# дозволяется выполнить метод. Иначе - пропускает этот метод.


class StatusFilter(BaseFilter):
    def __init__(self, status):
        self.status = status

    async def __call__(self, message: Message) -> bool:
        if self.status == SearchAny(message.chat.id, "userOfSetting", "status"):
            return True
        else:
            return False
