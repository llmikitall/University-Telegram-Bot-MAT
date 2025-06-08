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


@router.message(F.text.contains("Назад"), StatusFilter("5"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Menu1 import Output1
    await Output1(message)


@router.message(F.text.contains("Обнулить все факультативы"), StatusFilter("5"))
async def InputBack(message: Message):
    MessageInConsole(message)
    UpdateAny(message.chat.id, "userOfSetting", "groupings", "?")
    await message.answer("Ваши факультативы были обнулены.")
    await Output5(message)


@router.message(F.text, StatusFilter("5"))
async def Input5(message: Message):
    MessageInConsole(message)
    group = SearchAny(message.chat.id, "userOfSetting", "class")
    List = elcList(group)
    if message.text in List:
        from structures.EnterGrouping6 import Output6
        await Output6(message)
        return
    await message.answer("Не-не-не... неправильно")


async def Output5(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    emojiList.append(('', '✖️', '✖️')[emojiID])

    group = SearchAny(message.chat.id, "userOfSetting", "class")
    List = elcList(group)
    kb = [[KeyboardButton(text=f"{emojiList[0]}Назад")]]
    for i in range(len(List)):
        kb.append([KeyboardButton(text=f"{List[i]}")])
    kb.append([KeyboardButton(text=f"{emojiList[1]}Обнулить все факультативы{emojiList[1]}")])
    groupings = SearchAny(message.chat.id, "userOfSetting", "groupings")


    if SearchAny(userID, "historySetting", "status5") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Выбор факультатива</b>]\n   Здесь отображается <u>все</u> факультативы <i>Вашей</i>"
                " <u>группы</u>. Выбираете <i>Ваши</i> факультативы, которые <i>Вы</i> <b>выбирали на "
                "сайте: iot.sevsu.ru/electives</b>. После этого выбираете номер <i>Вашей</i> группы <i>Вашего</i> "
                "факультатива. Алгоритм будет отображать только <i>Ваши</i> факультативы, <b>скрывая все остальные</b>."
                "\n   <b>Будьте внимательны!</b>\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status5", "1")
    text = "<i>Ваш текущий список факультативов:</i>"
    if groupings == '?':
        text = "<b>На данный момент Вы не выбрали ни одного факультатива.</b>"
    else:
        groupings = groupings.split("\n")
        for i in range(len(groupings)):
            text = f"{text}\n   - <b>[{groupings[i]}]</b>"

    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer(f"Выберите название своего факультатива.\n{text}", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "5")


def elcList(group) -> list:
    con = sqlite3.connect("sql/db/schedule.db")
    cur = con.cursor()
    cur.execute(f'SELECT * FROM groupList WHERE class = "{group}"')
    firstList = cur.fetchall()
    secondList = []
    for i in range(len(firstList)):
        if not (firstList[i][3] in secondList) and firstList[i][3] != '-':
            secondList.append(firstList[i][3])
    secondList.sort()
    return secondList

