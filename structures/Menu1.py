from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from AnyMiddleware import AnyMiddleware
from sql.UpdateUserInformation import UpdateAny
from sql.SearchUserInformation import SearchAny
from StatusFilter import StatusFilter
from MessageLog import MessageInConsole
from aiogram import Router

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Расписание"), StatusFilter("1"))
async def InputSchedule(message: Message):
    MessageInConsole(message)
    from structures.EnterDate2 import Output2
    await Output2(message)


@router.message(F.text.contains("Настройки"), StatusFilter("1"))
async def InputSetting(message: Message):
    MessageInConsole(message)
    from structures.Setting3 import Output3
    await Output3(message)


@router.message(F.text.contains("Поменять группу:"), StatusFilter("1"))
async def InputChangeGroup(message: Message):
    MessageInConsole(message)
    from structures.EnterGroup0 import Output0
    await Output0(message)


@router.message(F.text.contains("Факультатив"), StatusFilter("1"))
async def InputAboutBot(message: Message):
    MessageInConsole(message)
    from structures.EnterLesson5 import Output5
    await Output5(message)


@router.message(F.text.contains("Поиск"), StatusFilter("1"))
async def InputAboutBot(message: Message):
    MessageInConsole(message)
    from structures.EnterTeacher11 import Output11
    await Output11(message)


async def Output1(message: Message):
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    userGroup = SearchAny(userID, "userOfSetting", "class")
    emojiList = list()
    emojiList.append(('', '✖️', '🕣 ')[emojiID])
    emojiList.append(('', '✖️', ' 🕓')[emojiID])
    emojiList.append(('', '➖', '⚙️ ')[emojiID])
    emojiList.append(('', '➖', '⭕ ')[emojiID])
    emojiList.append(('', '🔘', '👥 ')[emojiID])

    if SearchAny(userID, "historySetting", "status1") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Добро пожаловать в главное меню!</b>]\n   Здесь <i>Вы</i> по-прежнему можете перейти в "
                "расписание. Из нового, представляю <i>Вам</i> кнопки <u><b>\"Факультатив\"</b></u> и "
                "<u><b>\"Поиск\"</b></u>. "
                "Советую посетить каждую из этих кнопок. И особенно <u><i>рекомендую</i></u> зайти в "
                "<u><b>\"Настройки\"</b></u>! "
                "Там крайне много интересных вещей!\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhj1m6CVwvKZ0K1-DMbLzXOmjRt04BAACGwADwDZPE329ioPLRE1qNgQ",
                      "CAACAgIAAxkBAAEJq6xnJQkRh9MUriO6ZRJvJxkOTZ07SgACPAgAAkgVAUtpJ4GNIiLZSTYE",
                      "CAACAgIAAxkBAAEIhj1m6CVwvKZ0K1-DMbLzXOmjRt04BAACGwADwDZPE329ioPLRE1qNgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status1", "1")

    kb = [
        [KeyboardButton(text=f"{emojiList[0]}Расписание{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[3]}Факультатив"), KeyboardButton(text=f"{emojiList[3]}Поиск")],
        [KeyboardButton(text=f"{emojiList[2]}Настройки")],
        [KeyboardButton(text=f"{emojiList[4]}Поменять группу: {userGroup}")]
    ]
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Главное меню:", reply_markup=Keys)
    UpdateAny(userID, "userOfSetting", "status", "1")



