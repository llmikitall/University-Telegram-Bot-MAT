import sqlite3
import time

import xlrd3 as xlrd

from MessageLog import LogInConsole


def ExcelToSql(filename):
    # Открываем книгу, с которой работаем
    t1 = time.time()
    LogInConsole(f"   [>] [{filename}] Идёт считывание книги.")
    book = xlrd.open_workbook("excel/" + filename)

    # countList - int - количество листов в Excel файле.
    countList = book.nsheets
    # counter - int - является "индексом" каждой строки в книге для базы данных.
    counter = 0
    counter2 = 0

    # dataBase1 - list - лист, где хранится весь текст Excel-файла
    dataBase1 = list()

    dataBase2 = list()

    # Цикл 'a' - int - отвечает за текущую страницу книги. Нужна для переменной sh.
    # Начало со страницы 1, а не 0, потому что 0 - это справочная страница. Там считывать нечего.
    for a in range(1, countList):
        # sh - текущая страница - с помощью неё начинаем взаимодействовать со страницей и считывать её.
        sh = book.sheet_by_index(a)

        # Изначальные значения ячеек в книге.
        GroupRow = 3
        GroupCol = 0

        DateRow = 6
        DateCol = 1

        LessionRow = 6
        LessionCol = 4

        DoubleLessionRow = 6
        DoubleLessionCol = 5

        SubRow = 4
        SubCol = 4

        # Цикл 'b' - int - отвечает за количество групп. С 0 до 12 столбцов считывает.
        # Переменная 'b' Нигде не участвует.
        for b in range(12):
            # Игнорирование ошибки, если вдруг групп в файле меньше, чем 12.
            try:
                Group = sh.cell_value(GroupRow, GroupCol)[9:].casefold()
            except IndexError:
                break
            # SubStep - int - считывает количество подгрупп у группы.
            SubStep = 0
            # Цикл 'f' для вычисления количества подгрупп (всего 4 подгруппы считывается)
            for f in range(4):
                try:
                    sub = sh.cell_value(SubRow, SubCol + f * 3)
                    # Если в ячейке sub будет "подгруппа", то SubStep++. Иначе прекратить.
                    if sub.find("подгруппа") != -1:
                        SubStep = SubStep + 1
                    else:
                        break
                # Не помню, зачем это исключение...
                except IndexError:
                    break

            # Цикл 'c' - int - считывает даты у группы.
            for c in range(6):
                # Цикл 'd' - int - для считывания восьми пар.
                for d in range(8):
                    # week - str - Название листа.
                    week = book.sheet_names()[a]
                    # date - str - Дата дня, который мы считываем в расписании.
                    date = sh.cell_value(DateRow, DateCol)
                    # number - str - Номер текущей пары.
                    number = str(d + 1)
                    # Permission - int - Переменная, которая оповещает, что в текущей паре разделения на подгруппы.
                    Permission = 0

                    # Проверка, разбита ли пара на подгруппы?
                    if SubStep == 2:
                        if (sh.cell_value(DoubleLessionRow, DoubleLessionCol) != ""
                                or sh.cell_value(DoubleLessionRow, DoubleLessionCol + 2) != ""):
                            Permission = 1
                    elif SubStep == 3:
                        if (sh.cell_value(DoubleLessionRow, DoubleLessionCol) != ""
                                or sh.cell_value(DoubleLessionRow, DoubleLessionCol + 2) != ""
                                or sh.cell_value(DoubleLessionRow, DoubleLessionCol + 5) != ""):
                            Permission = 1
                    # Если да, то записываем в таблицу конечный результат
                    if Permission == 1:
                        # Цикл 'e' - int - разбор строки на 'SubStep' раз - количество подгрупп в группе.
                        for e in range(SubStep):
                            # Если ячейка полностью пуста, записываем типа такого: "1) - - - - -"
                            if sh.cell_value(LessionRow, LessionCol + 3 * e) == "":
                                cabinet = "-"
                                lesson = f"{e + 1}) -"
                                group = "-"
                                teacher = ("-", "-", "-")
                                typeL = "-"
                            # Иначе идёт разбор ячейки на части.
                            else:
                                # cell - list - считываем весь текст в ячейке и делим на ", ". ("Пара", "Учитель")
                                cell = sh.cell_value(LessionRow, LessionCol + 3 * e).split(", ")
                                if len(cell) > 2:
                                    for i in range(1, len(cell)):
                                        if i == len(cell) - 1:
                                            cell[1] = cell[i]
                                        cell[0] = f"{cell[0]}, {cell[i]}"
                                # lesson - str - Считываем cell[0] и удаляем первые символы "подг.:1(из2),"
                                # Замена не катит, так как не известно сколько всего подгрупп.
                                lesson = f"{e + 1}) {cell[0][15:]}"
                                # teacher - list - считываем cell[1] и разделяем на " ". ("Фам.", "Имя", "Отч.")
                                teacher = cell[1].replace("\n", "").split(" ")

                                # cabinet - str - считываем номер кабинета.
                                cabinet = f"{sh.cell_value(LessionRow, LessionCol + 2 + 3 * e)[:-1]}"
                                # group - str - обычно группы у подгрупп не бывает. Потому автоматом ставим "-".
                                group = "-"
                                # typeL - str - считывает вид текущей пары. "Л"/"ПЗ"
                                typeL = f"{sh.cell_value(LessionRow, LessionCol + 1 + 3 * e)[:-1]}"
                            try:
                                # Добавляем в базу данных всю полученную информацию. И увеличиваем счётчик-индекс
                                dataBase1.append(
                                    (filename, str(counter), Group, week[6:], date, number, lesson, group,
                                     teacher[0], teacher[1], teacher[2], cabinet, typeL))
                            except IndexError:
                                if len(teacher) == 2:
                                    dataBase1.append(
                                        (filename, str(counter), Group, week[6:], date, number, lesson, group,
                                         teacher[0], teacher[1], "", cabinet, typeL))
                                else:
                                    dataBase1.append(
                                        (filename, str(counter), Group, week[6:], date, number, lesson, group,
                                         teacher[0], "", "", cabinet, typeL))
                                LogInConsole(f"{Group}, {date}, {lesson}, {teacher}: ошибка с преподавателем.")

                            counter = counter + 1
                    else:
                        # Если ячейка полностью пуста, записываем типа такого: - - - - -"
                        if sh.cell_value(LessionRow, LessionCol) == '':
                            cabinet = "-"
                            lesson = "-"
                            teacher = ("-", "-", "-")
                            group = "-"
                            typeL = "-"

                            # Добавляем в базу данных всю полученную информацию. И увеличиваем счётчик-индекс
                            dataBase1.append(
                                (filename, str(counter), Group, week[6:], date, number, lesson, group,
                                 teacher[0], teacher[1], teacher[2], cabinet, typeL))
                            counter = counter + 1

                        # Иначе делим ячейки на части.
                        else:
                            # cell - list - считываем весь текст в ячейке и делим на "\n".
                            # Потому что порою в одной ячейке находятся эллективы. Типа в одной ячейке сразу по 5 пар.
                            cell = sh.cell_value(LessionRow, LessionCol).split("\n")

                            # Исключение из правил... Там была ошибка из-за него. Решить нужно в следующий раз.
                            if 'Обработка изображений и ' in cell:
                                LogInConsole(f"Найдена старая возможная ошибка: \n Книга: {filename};\n Номер: {counter};"
                                             f"\n Изначальный текст в ячейке: {cell};")
                                cell = [f"{cell[0]}{cell[1]}"]
                                LogInConsole(f" Изменённый текст в ячейке: {cell}")
                            # TempCabinet - list - Делит ячейку на "\n". Чтобы получить все кабинеты всех пар по частям.
                            TempCabinet = sh.cell_value(LessionRow, LessionCol + 3 * SubStep - 1).split("\n")
                            # TempTypeL - list - Делит ячейку на "\n". Чтобы получить типы пар всех пар по частям.
                            TempTypeL = sh.cell_value(LessionRow, LessionCol + 3 * SubStep - 2).split("\n")

                            # Цикл 'f' - int - разбираем cell[f], для записи одного из предмета в паре в список.
                            for f in range(len(cell) - 1):
                                # cabinet - str - считываем номер кабинета из TempCabinet[f]
                                cabinet = TempCabinet[f]
                                # typeL - str - считываем вид текущей пары из TempTypeL
                                typeL = TempTypeL[f]
                                # group - str - это просто объявление переменной. Чтобы она была доступна всем в этом
                                # цикле.
                                group = "-"
                                # Порою допускают ошибки, и добавляют в пару предмет с подгруппой, что является ошибкой.
                                cell[f] = cell[f].replace("подгр.:1(из 2),", "1) ").replace("подгр.:2(из 2),", "2) ")
                                # Замена ненужных вещей сразу на ""
                                cell[f] = cell[f].replace("(чп)", "").replace("(нем)", "")
                                # miniCell - list - делим пару на ", ". ("Пара", "Учитель (Группа)")
                                miniCell = cell[f].split(", ")
                                # Исключение, порою в lesson используется лишняя запятая.
                                if len(miniCell) > 2:
                                    miniCell[0] = f"{miniCell[0]}, {miniCell[1]}"
                                    miniCell[1] = miniCell[2]
                                # lesson - str - пара miniCell[0]
                                lesson = miniCell[0]
                                # microCell - list - делим miniCell[1] на '(' для разделения. ("Учитель", "Группа)")
                                microCell = miniCell[1].split("(")
                                # teacher - list - считываем microCell[0] и разделяем на " ". ("Фам.", "Имя", "Отч.")
                                teacher = microCell[0].replace("\n", "").split(" ")
                                # Если вдруг имя будет отсутствовать (Пример пары: "АДАПТАЦИОННАЯ НЕДЕЛЯ"), то
                                # не записываем преподавателя
                                if len(teacher) < 3:
                                    teacher = ("-", "-", "-")
                                # Иначе если имя учителя наоборот... какого-то хрена очень длинное, записываем
                                # последние три ячейки листа. (Пример такого: "2023 бурда Олимп чудо 'Ф И О'"
                                elif len(teacher) > 3:
                                    teacher[0] = teacher[len(teacher) - 4]
                                    teacher[1] = teacher[len(teacher) - 3]
                                    teacher[2] = teacher[len(teacher) - 2]
                                # Если с teacher всё нормально, то продолжаем

                                # Цикл 'test' - int - для поиска слова "Уч.гр." для записи группы пары.
                                for test in range(1, len(microCell)):
                                    if microCell[test].find("Уч.гр.") != -1:
                                        group = microCell[test][7:-1]
                                # Если cabinet и group оказались пусты. То заменяем на "-"
                                if len(cabinet) == 0:
                                    cabinet = "-"
                                if len(group) == 0:
                                    group = "-"
                                # Добавляем в базу данных всю полученную информацию. И увеличиваем счётчик-индекс
                                dataBase1.append(
                                    (filename, str(counter), Group, week[6:], date, number, lesson, group,
                                     teacher[0], teacher[1], teacher[2], cabinet, typeL))
                                counter = counter + 1
                                if not (any(text[2] in Group for text in dataBase2)):
                                    dataBase2.append((filename, str(counter2), Group, "-", "-", "-", "-", "-"))
                                    counter2 = counter2 + 1
                                if group != "-":
                                    if ((((not (any(text[3] == lesson for text in dataBase2))) or
                                        not (any(text[4] == group for text in dataBase2))) or
                                        not (any(text[2] == Group for text in dataBase2))) and
                                            not (") " in lesson)):
                                        dataBase2.append((filename, str(counter2), Group, lesson, group,
                                                          teacher[0], teacher[1], teacher[2]))
                                        counter2 = counter2 + 1
                    # Переходим к следующему, по номеру, уроку
                    LessionRow = LessionRow + 1
                    DoubleLessionRow = DoubleLessionRow + 1
                # Переходим к следующему дню.
                DateRow = DateRow + 8

            # Переходим к следующей группе.
            GroupCol = GroupCol + 3 * SubStep + 4

            # Переходим к самой первой пары следующей группы.
            LessionCol = LessionCol + 3 * SubStep + 4
            LessionRow = 6

            # Переходим к следующей дате новой группы
            DateCol = DateCol + 3 * SubStep + 4
            DateRow = 6

            # Это для считывания разделённых пар на подгруппы.
            DoubleLessionCol = DoubleLessionCol + 3 * SubStep + 4
            DoubleLessionRow = 6

            SubCol = SubCol + 3 * SubStep + 4

    # Открываем базу данных.
    con = sqlite3.connect("sql/db/schedule.db")
    # Создаём эдакий контрольную переменную cur.
    cur = con.cursor()
    # Скачивания всей таблицы в original - list.
    try:
        cur.execute('SELECT * FROM groupList WHERE book = (?)', [filename])
    except sqlite3.OperationalError:
        LogInConsole("   [<] Error: Таблица groupList отсутствовала. Пересоздаю...")
        from sql.CreateTables import CreateTableGroupList
        CreateTableGroupList()
        cur.execute('SELECT * FROM groupList WHERE book = (?)', [filename])
    original = cur.fetchall()
    # Цикл 'i' - Для сравнения dateBase1 с original.
    for i in range(len(dataBase2)):
        # Если строка dataBase1 и original совпадают. То проигнорировать изменения.
        if i < len(original) and dataBase2[i] == original[i]:
            continue
        # Иначе обновить данные.
        elif i < len(original):
            cur.execute("""UPDATE groupList SET class = (?), lesson = (?), grouping = (?), firstName = (?),
            lastName = (?), middleName = (?) WHERE book = """ + dataBase2[i][0] + " AND clue = " + dataBase2[i][1],
                        [dataBase2[i][2], dataBase2[i][3], dataBase2[i][4], dataBase2[i][5], dataBase2[i][6],
                         dataBase2[i][7]])
        else:
            # Если у original закончится размеры листа. Значит время добавлять в базу данных новые данные.
            cur.execute('INSERT INTO groupList VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (dataBase2[i]))
    # Сохранить базу данных.
    con.commit()
    try:
        cur.execute('SELECT * FROM scheduleList WHERE book = (?)', [filename])
    except sqlite3.OperationalError:
        LogInConsole("   [<] Error: Таблица scheduleList отсутствовала. Пересоздаю...")
        from sql.CreateTables import CreateTableScheduleList
        CreateTableScheduleList()
        cur.execute('SELECT * FROM scheduleList WHERE book = (?)', [filename])
    original = cur.fetchall()
    # Цикл 'i' - Для сравнения dateBase1 с original.
    for i in range(len(dataBase1)):
        # Если строка dataBase1 и original совпадают. То проигнорировать изменения.
        if i < len(original) and dataBase1[i] == original[i]:
            continue
        # Иначе обновить данные.
        elif i < len(original):
            cur.execute("""UPDATE scheduleList SET class = (?), week = (?), date = (?), number = (?), lesson = (
            ?), grouping = (?), firstName = (?), lastName = (?), middleName = (?), cabinet = (?), view = (?) 
            WHERE book = """ + dataBase1[i][
                0] + " AND clue = " + dataBase1[i][1],
                        [dataBase1[i][2], dataBase1[i][3], dataBase1[i][4], dataBase1[i][5], dataBase1[i][6],
                         dataBase1[i][7], dataBase1[i][8],
                         dataBase1[i][9], dataBase1[i][10], dataBase1[i][11], dataBase1[i][12]])
        else:
            # Если у original закончится размеры листа. Значит время добавлять в базу данных новые данные.
            cur.execute('INSERT INTO scheduleList VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (dataBase1[i]))
    # Сохранить базу данных.
    con.commit()
    con.close()
    t1 = time.time() - t1
    LogInConsole(f"   [>] [{filename}] Успешно считано за {t1} миллисекунд!")
