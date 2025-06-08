from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from AnyMiddleware import AnyMiddleware
from sql.UpdateUserInformation import UpdateAny
from sql.SearchUserInformation import SearchAny
from StatusFilter import StatusFilter
from MessageLog import MessageInConsole
from aiogram import Router

router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Выбрать подгруппу Иностр. яз."), StatusFilter("3"))
async def InputEnglishSubgroup(message: Message):
    MessageInConsole(message)
    from structures.EnterEnglishSubgroup8 import Output8
    await Output8(message)


@router.message(F.text.contains("Выбрать подгруппу"), StatusFilter("3"))
async def InputSubgroup(message: Message):
    MessageInConsole(message)
    from structures.EnterSubgroup4 import Output4
    await Output4(message)


@router.message(F.text.contains("Значки"), StatusFilter("3"))
async def InputIcons(message: Message):
    MessageInConsole(message)
    from structures.EnterIcons7 import Output7
    await Output7(message)


@router.message(F.text.contains("Формат текущего дня"), StatusFilter("3"))
async def InputIcons(message: Message):
    MessageInConsole(message)
    from structures.EnterFormatToday9 import Output9
    await Output9(message)


@router.message(F.text.contains("Формат даты"), StatusFilter("3"))
async def InputIcons(message: Message):
    MessageInConsole(message)
    from structures.EnterFormatDate10 import Output10
    await Output10(message)


@router.message(F.text.contains("О боте"), StatusFilter("3"))
async def InputAboutBot(message: Message):
    MessageInConsole(message)
    out = ("Бот <b>\"СевГУ\"</b>:\n- Версия: <i>3.1</i>\n- Разработчики: \n   - <i>Mik&&Ton</i>\n   - "
           "<i>welltrueforever19</i>\n- Связь с разработчиком: <i>@Miandon</i> ^-^")
    await message.answer(out)


@router.message(F.text.contains("Назад"), StatusFilter("3"))
async def InputBack(message: Message):
    MessageInConsole(message)
    from structures.Menu1 import Output1
    await Output1(message)


async def Output3(message: Message):
    userID = message.chat.id
    emojiID = int(SearchAny(userID, "userOfSetting", "emojiID"))
    emojiList = list()
    emojiList.append(('', '🔙 ', '↪️ ')[emojiID])
    emojiList.append(('', '▪️', '🔹')[emojiID])
    emojiList.append(('', '🖤 ', '🗺 ')[emojiID])
    emojiList.append(('', '▪️', '🤖 ')[emojiID])
    emojiList.append(('', '▪️', '')[emojiID])

    if SearchAny(userID, "historySetting", "status3") == '0':
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>НАСТРОЙКИ бота!</b>]\n   Надо же! <i>Сюда</i> кто-то да заглядывает! По моим исследованиям, "
                "этой опцией пользовались только... Я. <i>А ведь я старался</i>!\n   Здесь можно найти уйму "
                "<b>настроек</b>: можно <b>выбрать подгруппу</b>, <b>подгруппу иностранного языка</b>, разные "
                "<b>форматы расписаний</b> и стили <b><u>ЗНАЧКОВ</u></b>!\n"
                "   И в самом внизу можно найти <i>информацию о разработчиках</i>. Жду Вас в каждой кнопке! :)\n")
        await message.answer(sep + text + sep)
        stickerList = ("CAACAgIAAxkBAAEIhoBm6CyT7VdVjwcKpctANUt-1uyl_AACHAADwDZPE8GCGtMs_g7hNgQ",
                       "CAACAgIAAxkBAAEJq4hnJQYNvV3agG14Nkfb7QFy23Xv3wACyAoAAu4D0EigtVR0eA-44TYE",
                       "CAACAgIAAxkBAAEIhoBm6CyT7VdVjwcKpctANUt-1uyl_AACHAADwDZPE8GCGtMs_g7hNgQ")
        await message.answer_sticker(stickerList[emojiID])
        UpdateAny(userID, "historySetting", "status3", "1")

    kb = [
        [KeyboardButton(text=f"{emojiList[0]}Назад")],
        [KeyboardButton(text=f"{emojiList[1]}Выбрать подгруппу{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[1]}Выбрать подгруппу Иностр. яз.{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[1]}Формат текущего дня{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[1]}Формат даты{emojiList[1]}")],
        [KeyboardButton(text=f"{emojiList[2]}Значки")],
        [KeyboardButton(text=f"{emojiList[3]}О боте{emojiList[4]}")]
    ]

    placeholder = "Выберите вариант:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("Настройки:", reply_markup=Keys)
    UpdateAny(userID, "userOfSetting", "status", "3")



