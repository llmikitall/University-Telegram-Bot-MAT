import time
import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, types

from AnyMiddleware import AnyMiddleware
from sql.UpdateUserInformation import UpdateAny
from sql.SearchUserInformation import SearchAny
from sql.ScheduleReader import OutputSQL
from StatusFilter import StatusFilter
from MessageLog import MessageInConsole, LogInConsole
from aiogram import Router

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter("2"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Menu1 import Output1
    await Output1(message)


@router.message(F.text, StatusFilter("2"))
async def InputDay(message: Message):
    MessageInConsole(message)
    # Приём даты и возврат ReaderSQL
    WeekDays = ListOfDays(message)
    Keys = [[InlineKeyboardButton(text="Показать всё", callback_data="showAll"),
             InlineKeyboardButton(text="Аббревиатура", callback_data="abbreviation")]]
    InlineKeys = InlineKeyboardMarkup(inline_keyboard=Keys)
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
        try:
            text = OutputSQL(message, strToday, 0)
            await message.answer(text, reply_markup=InlineKeys)
            await Output2(message)
        except TelegramBadRequest:
            print(f"               [<]: Сообщение слишком большое!")
            final = text.split("-------------------------------------\n")
            separator = "-------------------------------------\n"
            output = ""
            for i in range(len(final) - 1):
                print(f"{i} - {len(final)}) {final[i]}")
                if len(output + final[i] + separator) < 4000 and i != len(final) - 2:
                    output = output + final[i] + separator
                    continue
                if i == len(final) - 2:
                    output = output + final[i] + separator
                print(f"{len(output + final[i] + separator)}")
                await message.answer(output)
                output = separator + final[i] + separator
        return
    else:
        try:
            today = datetime.datetime.strptime(message.text, "%d.%m.%Y")
            strToday = today.strftime("%d.%m.%Y")
            await message.answer(OutputSQL(message, strToday, 0), reply_markup=InlineKeys)
        except ValueError:
            await message.answer(f"Не... Я плохо понимаю такой формат, но понимаю такой: [01.09.2024]")
    await Output2(message)


@router.callback_query()
async def callbackHandler(callback: types.CallbackQuery):
    LogInConsole(f"[{callback.message.chat.id}] {callback.data}")
    if callback.data == "showAll":
        Keys = [[InlineKeyboardButton(text="Скрыть вновь", callback_data="hideAgain"),
                 InlineKeyboardButton(text="Аббревиатура", callback_data="abbreviation")]]
        InlineKeys = InlineKeyboardMarkup(inline_keyboard=Keys)
        date = callback.message.text.split("\n", 3)
        text = OutputSQL(callback.message, date[2][14:-1], 1)
        try:
            await callback.message.answer(text, reply_markup=InlineKeys)
        except TelegramBadRequest:
            print(f"               [<]: Сообщение слишком большое!")
            final = text.split("-------------------------------------\n")
            separator = "-------------------------------------\n"
            output = ""

            for i in range(len(final)-1):
                print(f"{i} - {len(final)}) {final[i]}")

                if len(output + final[i] + separator) < 4000 and i != len(final)-2:
                    output = output + final[i] + separator
                    continue
                if i == len(final)-2:
                    output = output + final[i] + separator
                print(f"{len(output + final[i] + separator)}")
                await callback.message.answer(output)
                output = separator + final[i] + separator
    elif callback.data == "abbreviation":
        Keys = [[InlineKeyboardButton(text="Удалить", callback_data="delete")]]
        InlineKeys = InlineKeyboardMarkup(inline_keyboard=Keys)
        text = ("<b>Памятка</b>\n"
                "-------------------------------------\n"
                "Расшифровка номера\n"
                "-------------------------------------\n"
                "<b>(I)</b> - ул. Университетская, 33\n"
                "<b>(II)</b> - ул. Университетская, 31\n"
                "<b>(IV)</b> -	ул. Университетская, 28\n"
                "<b>(V)</b> - ул. Гоголя, 14\n"
                "<b>(VI)</b> - ул. Гоголя, 23\n"
                "<b>(VII)</b> - ул. Курчатова, 7\n"
                "<b>(VIII)</b> - ул. Курчатова, 7\n"
                "<b>(IX)</b> - ул. Курчатова, 7\n"
                "<b>(XII)</b> - ул. Репина, 3\n"
                "-------------------------------------\n"
                "Расшифровка тип пар\n"
                "-------------------------------------\n"
                "<b>[Д]</b> - Дистанционное обучение\n"
                "<b>[ЛЗ]</b> - Лабораторное занятие\n"
                "<b>[ПЗ]</b> - Практическое занятие\n"
                "<b>[Л]</b> - Лекция\n"
                "-------------------------------------\n"
                "Расшифровка чего-то...\n"
                "-------------------------------------\n"
                "<b>(УТЦ)</b> - Учебно-тренировочный центр\n")
        await callback.message.answer(text, reply_markup=InlineKeys)
    elif callback.data == "hideAgain":
        Keys = [[InlineKeyboardButton(text="Показать всё", callback_data="showAll"),
                 InlineKeyboardButton(text="Аббревиатура", callback_data="abbreviation")]]
        InlineKeys = InlineKeyboardMarkup(inline_keyboard=Keys)
        date = callback.message.text.split("\n", 3)
        await callback.message.answer(OutputSQL(callback.message, date[2][14:-1], 0), reply_markup=InlineKeys)
    elif callback.data == "delete":
        await callback.message.delete()
    await callback.answer()


async def Output2(message: Message):
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
    if SearchAny(userID, "historySetting", "status2") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>Выбор дня из расписания</b>]\n   Здесь <i>Вы</i> по-прежнему можете выбрать <b>6-сть "
                "дней из расписания</b>. Однако появилась новая функция! Теперь можно выбрать <b>любой день</b>, "
                "для этого нужно <u>ввести вручную дату</u> интересующего Вас дня: <i>17.09.2024</i>.\n"
                "   По-прежнему, после получения сообщения, к ней будет прикреплено две кнопки: <b>\"Показать всё\"</b>"
                " и <b>\"Аббревиатура\"</b>.\n     <i>1-ая - показывает все скрытые алгоритмом пары</i>. "
                "После можно нажать на <b>\"Скрыть всё\"</b>, чтобы вернуть всё в изначальное состояние.\n"
                "     <i>2-ая - расшифрует сокращённые слова и скрытый смысл римских символов в номерах кабинетов</i>."
                "\n   <b><u>Рекомендуется мной иногда сравнивать с расписанием на сайте "
                "timetable.sevsu.ru, во избежания ошибок!!</u></b>\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ",
                       "CAACAgIAAxkBAAEJq69nJQotLtbMZ0EeLsLGkITvOcjkCwAC1gYAAut-2Uiz43Y2AAEsGQY2BA",
                       "CAACAgIAAxkBAAEIhnhm6Cva-pfDCe4YbqnD_s2qbVl_bgACGAADwDZPE9b6J7-cahj4NgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status2", "1")

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
    UpdateAny(userID, "userOfSetting", "status", "2")


def ListOfDays(message: Message):
    # Today - текущее время. Day - сколько времени в одном дне. Week - текущий день недели.
    today = time.time()
    day = 86400
    week = datetime.datetime.fromtimestamp(time.time()).weekday()
    # Сегодняшний день недели, как константа
    todayWeek = datetime.date.today().weekday()
    # Создание списка дней.
    formatDate = int(SearchAny(message.chat.id, "userOfSetting", "formatDate"))
    formatToday = SearchAny(message.chat.id, "userOfSetting", "formatToday")
    WeekDays = list()
    for i in range(7):
        # Проверка на воскресенье. (Мы исключаем воскресенье)
        if week >= 6:
            # + День * ((Воскресенье || Воскресенье + 1) - 5), добавить столько дней, сколько превысило воскресенье.
            today = today + day * (week - 5)
            week = 0
        # День и месяц дня, до которого дошла очередь.
        TimeToday = datetime.datetime.fromtimestamp(today).strftime("%d.%m")
        # Создаётся массив. (0 - тип оформления №1, 1 - тип оформления №2)
        if (week != 6) and (week == todayWeek) and formatToday == '1':
            WeekDays.append("Сегодня")
        elif week == todayWeek + 1 and formatToday == '1' or todayWeek == 6 and week == 0:
            WeekDays.append("Завтра")
        elif week == 0:
            WeekDays.append(('Понедельник', f'ПН. {TimeToday}')[formatDate])  # [todayList]
        elif week == 1:
            WeekDays.append(('Вторник', f'ВТ. {TimeToday}')[formatDate])
        elif week == 2:
            WeekDays.append(('Среда', f'СР. {TimeToday}')[formatDate])
        elif week == 3:
            WeekDays.append(('Четверг', f'ЧТ. {TimeToday}')[formatDate])
        elif week == 4:
            WeekDays.append(('Пятница', f'ПТ. {TimeToday}')[formatDate])
        elif week == 5:
            WeekDays.append(('Суббота', f'СБ. {TimeToday}')[formatDate])
        # Обработка массива.

        week = week + 1
        today = today + day
    return WeekDays
