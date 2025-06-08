import asyncio
import logging
import sqlite3
import sys
from threading import Thread

import aiogram
from aiogram.exceptions import TelegramForbiddenError
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

# Импорт вывод в консоль
from MessageLog import LogInConsole
from ScheduleVerification import ScheduleVerification
from commands import RouterCommands
# Импорт тех. обслуживание
from handler import MaintenanceMessage
from sql.DeleteUser import DeleteUser
from sql.SearchUserInformation import SearchAny
# Импорт структуры проекта
from structures import (StartCommand, EnterGroup0, Menu1, EnterDate2, Setting3, BadMessage, EnterSubgroup4,
                        EnterLesson5, EnterGrouping6, EnterIcons7, EnterEnglishSubgroup8, EnterFormatToday9,
                        EnterFormatDate10, EnterTeacher11, EnterTeacherDate12)


with open("doc/BotToken.txt") as file:
    TOKEN = file.read().strip()
file.close()
# Токен бота:
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    # Диспетчер DP. Все Routers подключены к нему!
    DP = Dispatcher(maintenance_mode=False)
    DP.include_router(MaintenanceMessage.maintenance_router)
    DP.include_router(RouterCommands.router)
    DP.include_router(StartCommand.router)
    DP.include_router(EnterGroup0.router)
    DP.include_router(Menu1.router)
    DP.include_router(EnterDate2.router)
    DP.include_router(Setting3.router)
    DP.include_router(EnterSubgroup4.router)
    DP.include_router(EnterLesson5.router)
    DP.include_router(EnterGrouping6.router)
    DP.include_router(EnterIcons7.router)
    DP.include_router(EnterEnglishSubgroup8.router)
    DP.include_router(EnterFormatToday9.router)
    DP.include_router(EnterFormatDate10.router)
    DP.include_router(EnterTeacher11.router)
    DP.include_router(EnterTeacherDate12.router)

    DP.include_router(BadMessage.router)
    logging.basicConfig(stream=sys.stdout)
    await UpdateBot(False)
    # Запуск верификации Расписания.
    await StartVerification(False)
    LogInConsole("[>] Запуск успешно произведён!")
    await DP.start_polling(bot)

async def StartVerification(boolean):
    if boolean:
        thread1 = Thread(target=ScheduleVerification)
        thread1.start()
    else:
        LogInConsole("[х] Запуск верификации отключен.")


async def UpdateBot(boolean):
    if boolean:
        con = sqlite3.connect("sql/db/users.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM usersList;")
        List = cur.fetchall()
        con.close()
        stickerList = ("CAACAgIAAxkBAAEIhhFm6B8ZeyrSTpvyytOHe3qO9G6i_QACBQADwDZPE_lqX5qCa011NgQ",
                       "CAACAgIAAxkBAAEJq6ZnJQjlBL-JUPpuSfMKSTzdNoRTpgACDQcAAp3m0Eg5RN1dHuLtjTYE",
                       "CAACAgIAAxkBAAEIhhFm6B8ZeyrSTpvyytOHe3qO9G6i_QACBQADwDZPE_lqX5qCa011NgQ")
        text = ("<b>[Обновление v.3.1]</b>\n"
                "—————————————\n"
                "    <i>[Исправлено]</i>\n"
                "    - <b>Иногда не отображался номер пары</b> у факультативов. <i>(Если был выбран "
                "какой-то факультатив)</i>\n"
                "    - <b>Иногда разделители терялись</b> из-за факультативов. <i>Символ \"&\" мог заменить \"——\""
                "</i>\n"
                "    - <b>В воскресенье понедельник не становился \"Завтра\"</b>\n"
                "    - <b>Ошибка связанная с большим размером сообщения</b>. <i>Теперь если оно будет большим, оно"
                " разделится.</i>\n"
                "—————————————\n"
                "    <i>[Добавлено]</i>\n"
                "    - Теперь <u>стиль значков</u> влияет и на <b>стиль стикера</b>. <i>При чёрном минимализме"
                " будет появляться чёрная вишенка.</i>\n"
                "—————————————")
        for i in range(len(List)):
            try:
                emojiID = int(SearchAny(List[i][0], "userOfSetting", "emojiID"))
                await bot.send_message(List[i][0], text)
                await bot.send_sticker(List[i][0],stickerList[emojiID])
                LogInConsole(f"{List[i][0]} -> Получил сообщение.")
            except aiogram.exceptions.TelegramForbiddenError:
                LogInConsole("Error: Пользователь заблокировал бота.")
                DeleteUser(List[i][0])

if __name__ == "__main__":
    LogInConsole("[>] Запуск MAIN...")
    asyncio.run(main())
