import os.path

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from AnyMiddleware import AnyMiddleware
from MessageLog import MessageInConsole


router = Router()
router.message.middleware(AnyMiddleware())


@router.message(F.text.contains("Разоблачение"))
async def HappyYear(message: Message):
    MessageInConsole(message)
    all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos')
    photo = FSInputFile(os.path.join(all_media_dir,'photo.jpg'))
    await message.answer_photo(photo=photo)


@router.message()
async def BadMessage(message: Message):
    MessageInConsole(message)
    await message.answer(f"Не пойму... что ты вводишь...")
    from sql.SearchUserInformation import SearchAny
    emojiID = int(SearchAny(message.chat.id, "userOfSetting", "emojiID"))
    stickerList = ("CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ",
                   "CAACAgIAAxkBAAEJq5FnJQaTjxkeDffS6Ye1ygynAAEb2tsAAiAJAAKm2dBISzXq3TBjArA2BA",
                   "CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ")
    await message.answer_sticker(stickerList[emojiID])