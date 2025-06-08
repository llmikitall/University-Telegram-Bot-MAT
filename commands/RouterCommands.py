import sqlite3

import aiogram
from aiogram.exceptions import TelegramForbiddenError
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from MessageLog import MessageInConsole, LogInConsole
from AdminMiddleware import AdminMiddleware

from sql.CreateTables import CreateAll
from sql.UpdateUserInformation import UpdateAny
from sql.DeleteUser import DeleteUser
from sql.DeleteTables import DeleteTables, DeleteAll

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command("", prefix="!"))
async def CommandOwner(message: Message):
    MessageInConsole(message)
    text = """Список команд для Администратора:
    1) <b>[!Таблицы]</b> - Обновляет текущие таблицы. (Необходимо для программиста)
    2) <b>[!Заблокировать <i>{ID}</i>]</b> - Блокирует пользователя.
    3) <b>[!Разблокировать <i>{ID}</i>]</b> - Разблокирует пользователя.
    4) <b>[!Удалить <i>{ID}</i>]</b> - Удаляет пользователя из всех таблиц.
    5) <b>[!Пересоздать <i>{Table/всё}</i>]</b> - Удаляет указанную таблицу и тут же её создаёт.
    6) <b>[!Список]</b> - Выводит сообщение со списком всех пользователей и его номером.
    7) <b>[!Найти <i>{ID/номер}</i>]</b> - Выводит всю информацию о пользователе. Нужен лишь ID либо его номер.
    8) <b>[!Сообщение <i>{Текст}</i>]</b> - Отправляет всем пользователям введённый текст. (Понимает HTML теги)
    """
    await message.answer(text)


@router.message(Command("Таблицы", prefix="!"))
async def CreateTables(message: Message):
    MessageInConsole(message)
    CreateAll()
    await message.answer("Таблицы успешно были обновлены")


@router.message(Command("Заблокировать", prefix="!"))
async def Ban(message: Message, command: CommandObject):
    MessageInConsole(message)
    if command.args is None:
        await message.answer("Команда введена неправильно: !Заблокировать {ID}")
        return
    UpdateAny(command.args, "usersList", "blocking", "+")
    await message.answer(f"Пользователь {command.args} был заблокирован.")


@router.message(Command("Разблокировать", prefix="!"))
async def Unban(message: Message, command: CommandObject):
    MessageInConsole(message)
    if command.args is None:
        await message.answer("Команда введена неправильно: !Разблокировать {ID}")
        return
    UpdateAny(command.args, "usersList", "blocking", "-")
    await message.answer(f"Пользователь {command.args} был разблокирован.")


@router.message(Command("Удалить", prefix="!"))
async def DeleteUserOfTable(message: Message, command: CommandObject):
    MessageInConsole(message)
    if command.args is None:
        await message.answer("Команда введена неправильно: !Удалить {ID}")
        return
    DeleteUser(command.args)
    await message.answer(f"Пользователь {command.args} был удалён.")


# Переработать! Сделать уничтожение отдельных таблиц, а не всех!
@router.message(Command("Пересоздать", prefix="!"))
async def DeleteTable(message: Message, command: CommandObject):
    MessageInConsole(message)
    userID = message.chat.id
    if userID != 879866452:
        await message.answer("Команда недоступна для Вас.")
        return
    if command.args is None:
        await message.answer("Команда введена неправильно: !Пересоздать {Table}")
        return
    if command.args == "всё":
        DeleteAll()
        await message.answer("Таблицы были пересозданы.")
        return
    await message.answer(DeleteTables(command.args))


@router.message(Command("Список", prefix="!"))
async def UsersList(message: Message):
    MessageInConsole(message)
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM usersList;")
    List = cur.fetchall()
    con.close()
    text = "<b>Список пользователей:</b>"
    for i in range(len(List)):
        text = text + f"\n<b>{i + 1}.</b> {List[i][0]}"
    await message.answer(text)


@router.message(Command("Найти", prefix="!"))
async def InfoOfUser(message: Message, command: CommandObject):
    MessageInConsole(message)
    if command.args is None:
        await message.answer("Команда введена неправильно: !Найти {ID/Номер}")
        return
    if len(command.args) > 10:
        await message.answer("Команда введена неправильно: !Найти {ID/Номер}")
        return
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    try:
        if len(command.args) > 5:
            cur.execute("SELECT * FROM usersList WHERE userID = (?);", ([command.args]))
            user = cur.fetchall()[0]
        else:
            cur.execute("SELECT * FROM usersList;")
            List = cur.fetchall()
            user = List[int(command.args) - 1]
    except IndexError:
        con.close()
        await message.answer(f"Пользователя такого не существует.")
        return

    text = (f"<b>Пользователь {user[0]}</b>:\n"
            f"-------------------------------\n"
            f"Таблица <b>UsersList</b>:\n"
            f"-------------------------------\n"
            f"<b>Полное имя</b>: {user[1]}\n"
            f"<b>Username</b>: {user[2]}\n"
            f"<b>Блокировка</b>: [{user[3]}]\n"
            f"<b>Последний поиск</b>: {user[4]}\n"
            f"-------------------------------\n"
            f"Таблица <b>UserOfSetting</b>:\n" 
            f"-------------------------------\n")
    cur.execute("SELECT * FROM userOfSetting WHERE userID = (?);", ([user[0]]))
    user = cur.fetchall()[0]
    text = text + (f"<b>Статус</b>: {user[1]}\n"
                   f"<b>Группа</b>: {user[2]}\n"
                   f"<b>Подгруппа</b>: {user[3]}\n"
                   f"<b>Иностранный язык</b>: {user[4]}\n"
                   f"<b>Эллективы</b>: {user[5]}\n"
                   f"<b>Стиль иконок</b>: {user[6]}\n"
                   f"<b>Формат \"Сегодня\"</b>: {user[7]}\n"
                   f"<b>Формат \"Даты\"</b>: {user[8]}\n"
                   f"-------------------------------")
    await message.answer(text)
    cur.execute("SELECT * FROM historySetting WHERE userID = (?);", ([user[0]]))
    user = cur.fetchall()[0]
    con.close()
    text = (f"Таблица <b>HistorySetting</b>:\n"
            f"-------------------------------\n"
            f"<b>Группы</b>: {user[1]}\n"
            f"<b>Преподаватели</b>: {user[2]}\n"
            f"<b>0</b>: [{user[3]}]   <b>1</b>: [{user[4]}]   <b>2</b>: [{user[5]}]\n"
            f"<b>3</b>: [{user[6]}]   <b>4</b>: [{user[7]}]   <b>5</b>: [{user[8]}]\n"
            f"<b>6</b>: [{user[9]}]   <b>7</b>: [{user[10]}]   <b>8</b>: [{user[11]}]\n"
            f"<b>9</b>: [{user[12]}]   <b>10</b>: [{user[13]}]   <b>11</b>: [{user[14]}]\n"
            f"-------------------------------")
    await message.answer(text)


@router.message(Command("Сообщение", prefix="!"))
async def SendMessage(message: Message, command: CommandObject):
    MessageInConsole(message)
    if command.args is None:
        await message.answer("Команда введена неправильно: !Сообщение {Текст}")
    con = sqlite3.connect("sql/db/users.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM usersList;")
    List = cur.fetchall()
    con.close()
    from Main import bot
    for i in range(len(List)):
        try:
            await bot.send_message(List[i][0], command.args)
        except aiogram.exceptions.TelegramForbiddenError:
            LogInConsole("Error: Пользователь заблокировал бота.")
            DeleteUser(List[i][0])

