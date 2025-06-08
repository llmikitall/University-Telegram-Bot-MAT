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


@router.message(F.text.contains("Без значков"), StatusFilter("7"))
async def Input1(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "emojiID", "0")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Чёрный минимализм"), StatusFilter("7"))
async def Input2(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "emojiID", "1")
    await message.answer("Ваша подгруппа: 2")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Яркая жизнь"), StatusFilter("7"))
async def Input3(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "emojiID", "2")
    await message.answer("Ваша подгруппа: 3")
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Назад"), StatusFilter("7"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Setting3 import Output3
    await Output3(message)


async def Output7(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    if SearchAny(userID, "historySetting", "status7") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Выбор стиля значков!</b>]\n   О! Здесь можно <b>выбрать стиль значков на кнопках</b>. "
                "В данный момент стоит стиль \"[🔹<u>Яркая жизнь</u>🔹]\". Так что если <i>Вам</i> надоел стиль, "
                "всегда можно его поменять на другой.\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEGelJmfYH03dS23KkecTYXL-XjqPkxAwACDQADwDZPE6T54fTUeI1TNQQ",
                       "CAACAgIAAxkBAAEJq7xnJQuAzVeyWcF-B4wt2ZcpAvpO8gACHQcAAg8wCEqnw4xYP4fWQDYE",
                       "CAACAgIAAxkBAAEGelJmfYH03dS23KkecTYXL-XjqPkxAwACDQADwDZPE6T54fTUeI1TNQQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status7", "1")
    kb = [
        [KeyboardButton(text="[Без значков]")],
        [KeyboardButton(text="[✖️Чёрный минимализм✖️]")],
        [KeyboardButton(text="[🔹Яркая жизнь🔹]")],
        [KeyboardButton(text=f"{emojiList[0]}Назад")]
    ]
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Выберите свой стиль:", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "7")
