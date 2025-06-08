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


@router.message(F.text.contains("Без подгруппы"), StatusFilter("4"))
async def Input1(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "subgroup", "?")
    await message.answer("Вы выбрали: \"Без подгруппы\"")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("1"), StatusFilter("4"))
async def Input1(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "subgroup", "1")
    await message.answer("Ваша подгруппа: 1")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("2"), StatusFilter("4"))
async def Input2(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "subgroup", "2")
    await message.answer("Ваша подгруппа: 2")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("3"), StatusFilter("4"))
async def Input3(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "subgroup", "3")
    await message.answer("Ваша подгруппа: 3")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Назад"), StatusFilter("4"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Setting3 import Output3
    await Output3(message)


async def Output4(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    emojiList.append(('', '✖️', '✖️')[emojiID])
    if SearchAny(userID, "historySetting", "status4") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Выбор подгруппы</b>]\n   Здесь всё просто, нужно <b>выбрать</b> <i>Вашу</i> <b>текущую "
                "подгруппу</b>. Выбранная подгруппа будет учитываться алгоритмом и станет отображать только пары с "
                "<i>Вашей</i> подгруппой. <u>Важно, что, для пары по иностранному языку, подгруппы отличаются</u>.\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status4", "1")
    kb = [
        [KeyboardButton(text="[1]")],
        [KeyboardButton(text="[2]")],
        [KeyboardButton(text="[3]")],
        [KeyboardButton(text=f"{emojiList[0]}Назад")],
        [KeyboardButton(text=f"{emojiList[1]}Без подгруппы{emojiList[1]}")]
    ]
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Выберите свою подгруппу:", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "4")
