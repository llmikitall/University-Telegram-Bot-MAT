import time
import datetime

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, types

from AnyMiddleware import AnyMiddleware
from sql.UpdateUserInformation import UpdateAny
from sql.SearchUserInformation import SearchAny
from sql.ScheduleReader import OutputSQLTeacher
from StatusFilter import StatusFilter
from MessageLog import MessageInConsole, LogInConsole
from aiogram import Router

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter("12"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Menu1 import Output1
    await Output1(message)


@router.message(F.text, StatusFilter("12"))
async def InputDay(message: Message):
    userID = message.chat.id
    teacher = SearchAny(userID, "usersList", "search")
    from structures.EnterDate2 import ListOfDays
    MessageInConsole(message)
    # Приём даты и возврат ReaderSQL
    WeekDays = ListOfDays(message)
    if any(text in message.text for text in WeekDays):
        day = 86400
        today = time.time()
        factor = 0
        if WeekDays[1] in message.text:
            factor = 1
        elif WeekDays[2] in message.text:
            factor = 2
        elif WeekDays[3] in message.text:
            factor = 3
        elif WeekDays[4] in message.text:
            factor = 4
        elif WeekDays[5] in message.text:
            factor = 5
        if datetime.date.today().weekday() + factor > 5:
            factor = factor + 1
        today = today + day * factor
        strToday = datetime.datetime.fromtimestamp(today).strftime('%d.%m.%Y')
        await message.answer(OutputSQLTeacher(strToday, teacher))
        await Output12(message)
        return
    else:
        try:
            today = datetime.datetime.strptime(message.text, "%d.%m.%Y")
            strToday = today.strftime("%d.%m.%Y")
            await message.answer(OutputSQLTeacher(strToday, teacher))
        except ValueError:
            await message.answer(f"Не... Я плохо понимаю такой формат, но понимаю такой: [01.09.2024]")
    await Output12(message)


async def Output12(message: Message):
    from structures.EnterDate2 import ListOfDays
    ListOfDays(message)
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList = list()
    emojiList.append(('', '➖', '🔹')[emojiID])
    emojiList.append(('', '', '🔹')[emojiID])
    emojiList.append(('', '✖️', '⭕')[emojiID])
    emojiList.append(('', '➕', '🔘')[emojiID])
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    WeekDays = ListOfDays(message)

    kb = [
        [KeyboardButton(text=f"{emojiList[2]} {WeekDays[0]} {emojiList[2]}"),
         KeyboardButton(text=f"{emojiList[3]} {WeekDays[1]} {emojiList[3]}")],
        [KeyboardButton(text=f"{emojiList[0]}{WeekDays[2]}{emojiList[1]}"),
         KeyboardButton(text=f"{emojiList[0]}{WeekDays[3]}{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[0]}{WeekDays[4]}{emojiList[1]}"),
         KeyboardButton(text=f"{emojiList[0]}{WeekDays[5]}{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[4]}Назад")]
    ]
    placeholder = "Выберите день:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Расписание на неделю:", reply_markup=Keys)
    UpdateAny(userID, "userOfSetting", "status", "12")
