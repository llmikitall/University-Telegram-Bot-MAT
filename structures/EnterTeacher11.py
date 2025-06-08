from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from StatusFilter import StatusFilter
from MessageLog import MessageInConsole
from sql.SearchUserInformation import SearchAny
from sql.UpdateUserInformation import UpdateAny
from sql.OutputTable import OutputTable
from aiogram import Router
from AnyMiddleware import AnyMiddleware

import sqlite3


router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter("11"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Menu1 import Output1
    await Output1(message)


@router.message(F.text, StatusFilter("11"))
async def Input11(message: Message, firstName=None, middleName=None, boolean=False):
    MessageInConsole(message)
    userID = message.chat.id
    secondName = message.text.casefold()
    table = OutputTable("scheduleList")
    for teacher in table:
        if teacher[8].casefold() == secondName:
            secondName = teacher[8]
            firstName = teacher[9]
            middleName = teacher[10]
            boolean = True
            break
    if boolean:
        await message.answer(f"Преподаватель {secondName} {firstName} {middleName}.")
        con = sqlite3.connect("sql/db/users.db")
        cur = con.cursor()
        cur.execute("SELECT teacher FROM historySetting WHERE userID = (?);", ([userID]))
        List = cur.fetchall()[0][0]
        if List == '?':
            UpdateAny(userID, "historySetting", "teacher", f"{secondName}")
        else:
            if not(message.text in List):
                UpdateAny(userID, "historySetting", "teacher", f"{List}\n{secondName}")

        UpdateAny(userID, "usersList", "search", secondName)
        UpdateAny(userID, "userOfSetting", "status", "1")

        from structures.EnterTeacherDate12 import Output12

        await Output12(message)
        return
    await message.answer("Введите нормального преподавателя!!")


async def Output11(message: Message):
    emojiList = list()
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])

    userID = message.chat.id
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("SELECT teacher FROM historySetting WHERE userID = (?);", ([userID]))
    List = cur.fetchall()[0][0].split('\n')
    con.close()

    if SearchAny(userID, "historySetting", "status11") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("<b>Поиск преподавателя</b>\n   Здесь нужно вручную ввести <b>фамилию</b> преподавателя, "
                "а после выбрать день недели или ввести дату расписания: <i>04.09.2024</i>, и мы получим расписание"
                " преподавателя в этот день!\n"
                "   Все введённые преподаватели до этого я выведу в виде кнопок!\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status11", "1")

    kb = []
    for i in range(len(List)):
        kb.append([KeyboardButton(text=f"{List[i]}")])
    kb.append([KeyboardButton(text=f"{emojiList[0]}Назад")])
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Введите фамилию преподавателя:", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "11")

