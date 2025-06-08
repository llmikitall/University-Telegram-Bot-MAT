import sqlite3
from aiogram.types import Message

from sql.SearchUserInformation import SearchAny


def OutputSQL(message: Message, date, showAll):
    # Открываем базу данных.
    conn = sqlite3.connect('sql/db/schedule.db')
    # Создаём эдакую контрольную переменную.
    cur = conn.cursor()
    group = SearchAny(message.chat.id, "userOfSetting", "class")
    # Конкретная дата для выдачи списка уроков.
    num = (f'{group}', date)
    # Получаем список уроков в конкретную дату.
    cur.execute('SELECT * FROM scheduleList WHERE class = (?) AND date = (?);', num)
    # Присваиваем resul таблицу. Теперь он двухмерный массив.
    resul = cur.fetchall()
    userID = message.chat.id
    if len(resul) == 0:
        return (f"<b>{group}</b>\nУчебная неделя: <u>?</u>\nРасписание на <u>{date}</u>:\n"
                f"-------------------------------------\n"
                f"<i>Расписание на данный день отсутствует.</i>\n")
    text = (f"<b>{group}</b>\n"
            f"Учебная неделя: <u>{resul[0][3]}</u>\n"
            f"Расписание на <u>{date}</u>:\n"
            f"-------------------------------------\n")
    time = ['(8.30-10.00)', '(10.10-11.40)', '(11.50-13.20)', '(14.00-15.30)', '(15.40-17.10)', '(17.20-18.50)',
            '(19.00-20.30)', '(20.40-22.10)']
    for i in range(len(resul)):
        number = resul[i][5]
        lesson = resul[i][6]
        grouping = "" if len(resul[i][7]) <= 1 else f"<b>[{resul[i][7]}]</b>"
        teacher = f"{resul[i][8]} {resul[i][9]} {resul[i][10]}"
        cabinet = resul[i][11]
        view = resul[i][12]
        endLine = False
        if lesson == "-":
            if showAll == 1:
                text = text + (f"<b>{number}.</b> -\n"
                               "-------------------------------------\n")
        else:
            if showAll == 0 and ") " in lesson and grouping == "":
                if "язык" in lesson and SearchAny(userID, "userOfSetting", "englishSubgroup") != "?":
                    if not (SearchAny(userID, "userOfSetting", "englishSubgroup") in lesson):
                        continue
                    else:
                        endLine = True
                elif SearchAny(userID, "userOfSetting", "subgroup") != "?":
                    if not (SearchAny(userID, "userOfSetting", "subgroup") in lesson):
                        continue
                    else:
                        endLine = True
            elif showAll == 0 and grouping != "":
                groupings = SearchAny(userID, "userOfSetting", "groupings")
                if groupings != '?':
                    if not (grouping[4:-5] in groupings):
                        continue
                    else:
                        endLine = True

            if i == 0 or resul[i - 1][5] != number or endLine:
                text = text + f"<b>{number}.</b> <i>{time[int(number) - 1]}</i>\n"


            if ") " in lesson and grouping == "":
                if ") -" in lesson:
                    text = text + f"   {lesson}\n"
                else:
                    memory = lesson.split(" ", 1)
                    text = text + (f"   {memory[0]} <b><i>[{cabinet}]</i></b> <i>[{view}]</i> {memory[1]}  - "
                                   f"{teacher} {grouping}\n")
            else:
                text = text + f"   <b><i>[{cabinet}]</i></b> <i>[{view}]</i> {lesson} - {teacher} {grouping}\n"
            if i != len(resul) - 1 and resul[i + 1][5] != number or endLine:
                text = text + "-------------------------------------\n"
            else:
                text = text + "                   <i>&</i>\n"
    if len(text.split("\n")) < 6:
        text = text + ("<i>Данный день можно считать выходным!</i>\n"
                       "-------------------------------------\n")
    if showAll == 0:
        text = text + "<i>Кнопка \"Показать всё\" покажет все скрытые пары.</i>"
    return text


def OutputSQLTeacher(date, teacher):
    conn = sqlite3.connect('sql/db/schedule.db')
    cur = conn.cursor()

    num = (f'{teacher}', date)
    # Получаем список уроков в конкретную дату.
    cur.execute('SELECT * FROM scheduleList WHERE firstName = (?) AND date = (?);', num)
    # Присваиваем resul таблицу. Теперь он двухмерный массив.
    resul = cur.fetchall()
    resul.sort(key=lambda x: x[5])
    if len(resul) == 0:
        return (f"<b>{teacher}</b>\nУчебная неделя: <u>?</u>\nРасписание на <u>{date}</u>:\n"
                f"-------------------------------------\n"
                f"<i>Расписание на данный день отсутствует.</i>\n")
    text = (f"<b>{teacher}</b>\n"
            f"Учебная неделя: <u>{resul[0][3]}</u>\n"
            f"Расписание на <u>{date}</u>:\n"
            f"-------------------------------------\n")
    time = ['(8.30-10.00)', '(10.10-11.40)', '(11.50-13.20)', '(14.00-15.30)', '(15.40-17.10)', '(17.20-18.50)',
            '(19.00-20.30)', '(20.40-22.10)']
    for i in range(len(resul)):

        number = resul[i][5]
        lesson = resul[i][6]
        grouping = "" if len(resul[i][7]) <= 1 else f"<b>[{resul[i][7]}]</b>"
        group = f"<b>[{resul[i][2]}]</b>" if len(resul[i][7]) <= 1 else ""
        teacher = f"{resul[i][8]} {resul[i][9]} {resul[i][10]}"
        cabinet = resul[i][11]
        view = resul[i][12]
        if lesson == "-":
            text = text + (f"<b>{number}.</b> -\n"
                           "-------------------------------------\n")
        else:
            if i == 0 or resul[i - 1][5] != number:
                text = text + f"<b>{number}.</b> <i>{time[int(number) - 1]}</i>\n"

            if ") " in lesson:  # and grouping == ""
                if ") -" in lesson:
                    text = text + f"   {lesson}\n"
                else:
                    memory = lesson.split(" ", 1)
                    text = text + (f"   {memory[0]} <b><i>[{cabinet}]</i></b> <i>[{view}]</i> {memory[1]}  - "
                                   f"{teacher} {grouping} {group}")
            else:
                if i == 0 or (number != resul[i - 1][5]):
                    text = text + f"   <b><i>[{cabinet}]</i></b> <i>[{view}]</i> {lesson} - {teacher} {grouping}{group}"
                else:
                    memory = text.split("-------------------------------------\n")
                    if not(f"{grouping}{group}" in memory[len(memory)-1]):
                        text = text + f"-{grouping}{group}"

                #memory = f"   <b><i>[{cabinet}]</i></b> <i>[{view}]</i> {lesson} - {teacher} {grouping} {group}\n"
                #if not(memory in text) or number != resul[i - 1][5]:
                #    text = text + memory
            if i == len(resul) - 1 or resul[i + 1][5] != number:
                text = text + "\n-------------------------------------\n"
    return text
