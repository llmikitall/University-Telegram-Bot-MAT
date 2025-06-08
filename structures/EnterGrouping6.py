from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from StatusFilter import StatusFilter
from MessageLog import MessageInConsole
from sql.UpdateUserInformation import UpdateAny
from sql.SearchUserInformation import SearchAny
from aiogram import Router
from AnyMiddleware import AnyMiddleware

import sqlite3

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter("6"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.EnterLesson5 import Output5
    await Output5(message)


@router.message(F.text, StatusFilter("6"))
async def Input6(message: Message):
    MessageInConsole(message)
    group = SearchAny(message.chat.id, "userOfSetting", "class")
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM groupList WHERE class = \"{group}\"")
    List = cur.fetchall()
    if any(message.text[1:-1] in text for text in List):
        groupings = SearchAny(message.chat.id, "userOfSetting", "groupings")
        if not(message.text[1:-1] in groupings):
            if groupings == '?':
                UpdateAny(message.chat.id, "userOfSetting", "groupings", f"{message.text[1:-1]}")
            else:
                UpdateAny(message.chat.id, "userOfSetting", "groupings", f"{groupings}\n{message.text[1:-1]}")
        await message.answer(f"Факультатив {message.text} был успешно добавлен в список.")
        from structures.EnterLesson5 import Output5
        await Output5(message)
        return
    await message.answer("Не-не-не... неправильно")


async def Output6(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])

    group = SearchAny(message.chat.id, "userOfSetting", "class")
    List = groList(group, message.text)
    kb = [[KeyboardButton(text=f"{emojiList[0]}Назад")]]
    for i in range(len(List)):
        kb.append([KeyboardButton(text=f"[{List[i]}]")])

    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    if SearchAny(userID, "historySetting", "status6") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Выбор группы факультатива</b>]\n   Точно-точно этот факультатив..? Просто интересуюсь!"
                " :)\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIiBZm6F4KgdY5ON1SeLH7W63EinTXUwACEgADwDZPEzO8ngEulQc3NgQ",
                       "CAACAgIAAxkBAAEJq7RnJQtJoFDRqGIUNT7jN90MOfJTJQACMwgAAgUr2EqCENrB4G7yLDYE",
                       "CAACAgIAAxkBAAEIiBZm6F4KgdY5ON1SeLH7W63EinTXUwACEgADwDZPEzO8ngEulQc3NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status6", "1")
    await message.answer("Выберите группу своего факультатива:", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "6")


def groList(group, lesson):
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM groupList WHERE class = \"{group}\" and lesson = \"{lesson}\"")
    firstList = cur.fetchall()
    secondList = []
    for i in range(len(firstList)):
        secondList.append(firstList[i][4])
    return secondList
