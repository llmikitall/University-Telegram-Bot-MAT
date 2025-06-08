from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from StatusFilter import StatusFilter
from MessageLog import MessageInConsole
from sql.SearchUserInformation import SearchAny
from sql.UpdateUserInformation import UpdateAny
from aiogram import Router
from AnyMiddleware import AnyMiddleware

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Стандартное оформление"), StatusFilter("9"))
async def Input1(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "formatToday", "0")
    await message.answer("Изменения успешно применены.")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Сегодня/Завтра"), StatusFilter("9"))
async def Input2(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "formatToday", "1")
    await message.answer("Изменения успешно применены.")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Назад"), StatusFilter("9"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Setting3 import Output3
    await Output3(message)


async def Output9(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    if SearchAny(userID, "historySetting", "status9") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Формат текущего дня</b>]\n   Это визуальная настройка. Когда <i>Вы</i> "
                "выбрали <b>\"Расписание\"</b>, сегодняшний день отображается как <b>\"Сегодня\"</b>, "
                "завтрашний - <b>\"Завтра\"</b>. <i>(Настройка \"[Сегодня/Завтра]\")</i>\n"
                "   <b>Стандартное оформление</b> - это вместо надписей выше будут даты.\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status9", "1")
    kb = [
        [KeyboardButton(text="[Стандартное оформление]")],
        [KeyboardButton(text="[Сегодня/Завтра]")],
        [KeyboardButton(text=f"{emojiList[0]}Назад")],
    ]
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer(f"Выберите формат текущего дня: ", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "9")
