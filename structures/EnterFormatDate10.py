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


@router.message(F.text.contains("Понедельник/Вторник"), StatusFilter("10"))
async def Input1(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "formatDate", "0")
    await message.answer("Изменения успешно применены.")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("ПН. 11.03/ВТ. 12.03"), StatusFilter("10"))
async def Input2(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "formatDate", "1")
    await message.answer("Изменения успешно применены.")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Назад"), StatusFilter("10"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Setting3 import Output3
    await Output3(message)


async def Output10(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])

    kb = [
        [KeyboardButton(text="[Понедельник/Вторник]")],
        [KeyboardButton(text="[ПН. 11.03/ВТ. 12.03]")],
        [KeyboardButton(text=f"{emojiList[0]}Назад")],
    ]
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    if SearchAny(userID, "historySetting", "status10") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Формат даты</b>]\n   Это визуальная настройка. Когда <i>Вы</i> "
                "выбрали <b>\"Расписание\"</b>, каждый день отображается по стилю: <i>[ДН. ДД.ММ]</i>, где "
                " <b>ДН</b> - <i>день недели</i>, <b>ДД</b> - <i>день (число)</i>, <b>ММ</b> - <i>месяц (число)</i>. "
                "<i>(Настройка: [ПН. 11.03/ВТ. 12.03])</i>\n"
                "   <b>[Понедельник/Вторник]</b> - это каждый день будет отображаться названиями дней недели.\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status10", "1")
    await message.answer(f"Выберите формат текущего дня: ", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "10")
