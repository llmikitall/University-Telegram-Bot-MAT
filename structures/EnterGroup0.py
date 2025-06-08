from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F
from asyncio import sleep

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


@router.message(F.text, StatusFilter("0"))
async def Input0(message: Message):
    MessageInConsole(message)
    userID = message.chat.id
    text = message.text.casefold()
    if any(group[2] == text for group in OutputTable("groupList")):
        UpdateAny(userID, "userOfSetting", "class", text)
        await message.answer(f"Ваша группа: {text}")
        con = sqlite3.connect("sql/db/users.db")
        cur = con.cursor()
        cur.execute("SELECT class FROM historySetting WHERE userID = (?);", ([userID]))
        List = cur.fetchall()[0][0]
        if List == '?':
            UpdateAny(userID, "historySetting", "class", f"{text}")
        else:
            if not(message.text in List):
                UpdateAny(userID, "historySetting", "class", f"{List}\n{text}")
        UpdateAny(userID, "userOfSetting", "status", "1")

        from structures.Menu1 import Output1

        await Output1(message)
        return
    await message.answer("Введите нормальную группу!")


async def Output0(message: Message):
    userID = message.chat.id
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("SELECT class FROM historySetting WHERE userID = (?);", ([userID]))
    List = cur.fetchall()[0][0].split('\n')
    con.close()

    if SearchAny(userID, "historySetting", "status0") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Ввод Вашей группы</b>]\n   Привет, я - <i>Ваш</i> <b>проводник данного лабиринта</b>. "
                "Я буду рассказывать <i>Вам</i> <b>про нововведения</b> или <b>как пользоваться текущими кнопками</b>."
                " После этого я буду редко появляться, чтобы <i>Вы</i> потом скучали по мне. :)\n"
                "Здесь нужно ввести <u>вручную <i>Вашу</i> группу</u>. Пример: <i>ит/б-23-2-о</i>. После этого я "
                "запомню <i>Ваш</i> выбор, и, если <i>Вы</i> захотите сменить группу, <b>автоматически подставлю"
                " <i>Ваши</i> введённые до этого группы</b>.\n")
        await message.answer(sep + text + sep)
        emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
        stickerList = ("CAACAgIAAxkBAAEIhhFm6B8ZeyrSTpvyytOHe3qO9G6i_QACBQADwDZPE_lqX5qCa011NgQ",
                       "CAACAgIAAxkBAAEJq6ZnJQjlBL-JUPpuSfMKSTzdNoRTpgACDQcAAp3m0Eg5RN1dHuLtjTYE",
                       "CAACAgIAAxkBAAEIhhFm6B8ZeyrSTpvyytOHe3qO9G6i_QACBQADwDZPE_lqX5qCa011NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status0", "1")

    kb = []
    for i in range(len(List)):
        kb.append([KeyboardButton(text=f"{List[i]}")])
    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Введите вашу группу:", reply_markup=Keys)
    UpdateAny(message.chat.id, "userOfSetting", "status", "0")

