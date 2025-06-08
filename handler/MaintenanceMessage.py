from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import MagicData



# Обработчик для тех. обслуживания. Во время тех. обслуживания бот будет иметь автоответчик на все сообщения
# пользователя. Нужно изменить параметр на True, чтобы начать тех. обслуживание. Иначе будет нормальная работа.


MaintenanceMode = True

maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(MaintenanceMode)))


@maintenance_router.message()
async def any_message(message: Message):
    await message.answer("Бот на обслуживании... Пожалуйста, разбудите его попозже...")
    from sql.SearchUserInformation import SearchAny
    emojiID = int(SearchAny(message.chat.id, "userOfSetting", "emojiID"))
    stickerList = ("CAACAgIAAxkBAAEGeq5mfYn1Qt-iIjDH-fNN4iCgOAlGpQACCwADwDZPEwj4r9hZOMkzNQQ",
                   "CAACAgIAAxkBAAEJq9FnJQ0bc8lCnkbfPyMs5jrL_kW2egACEggAAhwGIUrmaGiuavJ_KTYE",
                   "CAACAgIAAxkBAAEGeq5mfYn1Qt-iIjDH-fNN4iCgOAlGpQACCwADwDZPEwj4r9hZOMkzNQQ")
    await message.answer_sticker(stickerList[emojiID])
