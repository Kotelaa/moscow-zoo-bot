import asyncio
import logging

from aiogram import Dispatcher, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_list, as_marked_list,  \
    Italic

from TokenData import TOKEN
from utils import ALL_CONTACTS, utils_router
from const import ABOUT_ZOO, ABOUT_CUSTODY, HELP_MESSAGE, PRIVACY_MESSAGE
from quiz import router_quiz
from Keyboards import commands_kb, animal_custody_kb, web_kb


router = Router()

@router.message(CommandStart())
@router.message(Command('commands'))
async def welcome_message(message: Message):
    """ Welcome message using command /start """
    content = as_list(
        Bold(f'Привет, {message.from_user.full_name}!'),
        'Добро пожаловать в Бот Московского зоопарка!\n',
        Bold('Доступные команды: '),
        as_marked_list(
            '/commands',
            '/help',
            '/about',
            '/contact',
            '/survey',
            '/privacy',
            marker='🐾  '
        )
    )
    await message.answer(content.as_html(), reply_markup=commands_kb())


@router.message(Command('help'))
async def help_message(message: Message):
    """ Help message using command /help """
    await message.answer(HELP_MESSAGE.as_html(), reply_markup=commands_kb())


@router.message(Command('about'))
async def about_message(message: Message):
    """ Some information about the ZOO using command /about """
    content = as_list(
        Bold('Московский зоопарк 🐾'),
        Italic('Оазис живой природы с 1864 года'),
        ABOUT_ZOO,
        '',
        Bold('✨ Станьте хранителем!'),
        ABOUT_CUSTODY,
    )

    await message.answer(content.as_html(), reply_markup=animal_custody_kb)


@router.message(Command('contact'))
async def contact_message(message: Message):
    """ Contact message using command /contact """
    content = as_marked_list(
        *ALL_CONTACTS,
        marker='\n🌱 '
    )
    await message.answer(**content.as_kwargs(), reply_markup=web_kb)


@router.message(Command('privacy'))
async def privacy_message(message: Message):
    await message.answer(PRIVACY_MESSAGE.as_html(), reply_markup=commands_kb())


async def start_bot():
    """ Main function to start the bot """
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("bot_errors.log"),
                  logging.StreamHandler()]
    )

    logger = logging.getLogger(__name__)


    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(router_quiz)
    dp.include_router(utils_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print('Bot stopped!')
