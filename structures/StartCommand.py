from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router
from asyncio import sleep

from MessageLog import MessageInConsole, LogInConsole
from sql.SearchUserInformation import SearchAny
from sql.UpdateUserInformation import UpdateAny
from AnyMiddleware import AnyMiddleware

import sqlite3
import random

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(CommandStart())
async def CommandStart(message: Message):
    MessageInConsole(message)
    userID = message.chat.id
    con = sqlite3.connect('sql/db/users.db')
    cur = con.cursor()
    cur.execute("""SELECT * FROM usersList WHERE userID = (?)""", ([f'{userID}']))
    user = cur.fetchall()
    if len(user) == 0:
        fullName = message.chat.full_name
        userName = message.chat.username
        cur.execute('INSERT INTO usersList VALUES(?, ?, ?, ?, ?);', (f'{userID}', fullName, userName, "-", "-"))
        cur.execute('INSERT INTO userOfSetting VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);', (f'{userID}', "0",
                                                                                     "?", "?", "?", "?", "2", "1", "1"))
        cur.execute('INSERT INTO historySetting VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                    (f'{userID}', "?", "?", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"))
        con.commit()
        LogInConsole(f"Запись нового пользователя: {userID}|{userName}|{fullName}.")
        con.close()
        from structures.EnterGroup0 import Output0

        await Output0(message)
        return
    con.close()
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    if SearchAny(userID, "userOfSetting", "status") == "0":
        await message.answer("Не-не-не... Введите сначала свою группу!")
        stickerList = ("CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ",
                       "CAACAgIAAxkBAAEJq5FnJQaTjxkeDffS6Ye1ygynAAEb2tsAAiAJAAKm2dBISzXq3TBjArA2BA",
                       "CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ")
        await message.answer_sticker(stickerList[emojiID])
        from structures.EnterGroup0 import Output0
        await Output0(message)
        return
    else:
        stickersList = (("CAACAgIAAxkBAAEHoXVmucVYCKn-iuXEkgr_ME1IQbv3nAACHAADwDZPE8GCGtMs_g7hNQQ",
                         "CAACAgIAAxkBAAEJq4hnJQYNvV3agG14Nkfb7QFy23Xv3wACyAoAAu4D0EigtVR0eA-44TYE",
                         "CAACAgIAAxkBAAEHoXVmucVYCKn-iuXEkgr_ME1IQbv3nAACHAADwDZPE8GCGtMs_g7hNQQ"),
                        ("CAACAgIAAxkBAAEHoXdmucVhMvICm4N-Nx9hCrsX4W0R8AACHgADwDZPE6FgWy2rAAHeBDUE",
                         "CAACAgIAAxkBAAEJq4tnJQYs6yhlzFFkKip9poCp-lBpkwACrwgAAmYwYUqfVf7YJTfGPTYE",
                         "CAACAgIAAxkBAAEHoXdmucVhMvICm4N-Nx9hCrsX4W0R8AACHgADwDZPE6FgWy2rAAHeBDUE"),
                        ("CAACAgIAAxkBAAEHoXlmucVqOs1F-BiHakz4bIAcELGFDAACEQADwDZPEw2qsw_cHj7lNQQ",
                         "CAACAgIAAxkBAAEJq6ZnJQjlBL-JUPpuSfMKSTzdNoRTpgACDQcAAp3m0Eg5RN1dHuLtjTYE",
                         "CAACAgIAAxkBAAEHoXlmucVqOs1F-BiHakz4bIAcELGFDAACEQADwDZPEw2qsw_cHj7lNQQ"),
                        ("CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ",
                         "CAACAgIAAxkBAAEJq5FnJQaTjxkeDffS6Ye1ygynAAEb2tsAAiAJAAKm2dBISzXq3TBjArA2BA",
                         "CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ"))
        await message.answer_sticker(random.choice(stickersList)[emojiID])

        from structures.Menu1 import Output1

        await Output1(message)
