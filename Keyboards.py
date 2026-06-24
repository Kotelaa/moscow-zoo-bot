import urllib.parse

from aiogram.utils.keyboard import KeyboardButton, \
    ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardMarkup


def commands_kb():
    """ Telegram commands keyboard """
    keyboard = ReplyKeyboardBuilder()
    commands = ['/commands',
            '/help',
            '/about',
            '/contact',
            '/survey',
            '/privacy']

    for command in commands:
        keyboard.add(KeyboardButton(text=command))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


animal_custody_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Узнать больше о опеке',
                          url='https://moscowzoo.ru/about/guardianship/')]])


# phone_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
#     text="📞 Позвонить в зоопарк", url="tel:+74957753370")]])


web_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton
                      (text='🤗  Посетите наш сайт',
                       url='https://moscowzoo.ru/')]])


def survey_options_kb(options):
    keyboard = ReplyKeyboardBuilder()
    for option in options:
        keyboard.add(KeyboardButton(text=option))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def share_keyboard(animal_name):
    share_text = (f"Я прошел тест от Московского зоопарка и моё тотемное "
                  f"животное – {animal_name}! 🐾 Узнай своё здесь:")
    bot_link = 'https://t.me/Moskva_Zoo_bot'

    encoded_text = urllib.parse.quote(share_text)

    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(
        text="✈️ Поделиться в Telegram",
        url=f"https://t.me/share/url?url={bot_link}&text={encoded_text}"))
    keyboard.row(InlineKeyboardButton(
        text="💙 Поделиться в VK",
        url=f"https://vk.com/share.php?url={bot_link}&title={encoded_text}"))
    keyboard.row(InlineKeyboardButton(
        text='🐱  Узнать больше о опеке',
        url='https://moscowzoo.ru/about/guardianship/'))
    keyboard.row(InlineKeyboardButton(
        text="📞 Связаться с сотрудником",
        callback_data="contact_staff")
    )
    return keyboard.as_markup(resize_keyboard=True)






