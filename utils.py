# import re
from aiogram.utils.formatting import as_line, TextLink, Bold
from aiogram import Router, F
from aiogram.types import Message

utils_router = Router()


def add_number(name: str, phone : str =None, mail : str =None):
    """ Add a number to the /contact command """
    parts = []
    parts.append(Bold(f'{name}: '))

    if phone:
        # clean_phone = re.sub(r'[^\d+]', '', phone)
        parts.append(f'{phone}')
        parts.append('  ')
    if mail:
        parts.append(TextLink(mail, url=f'mailto:{mail}'))
    return as_line(*parts)


ALL_CONTACTS = [
    add_number('Телефон для справок по льготам, покупке билетов '
               'и другим вопросам посетителей', phone='+7 (495) 775-33-70'),
        add_number('Администрация', mail='zoopark@culture.mos.ru'),
        add_number('Дежурно-диспетчерская служба(по вопросам оповещения)',
                   mail='pcn@culture.mos.ru'),
        add_number('Детский лагерь «ЗооМастерские»',
                   phone='+7 (499) 255-57-63'),
        add_number('Центр воспроизводства', phone='+7 (903) 004-94-25',
                   mail='info@moscowzoo.center'),
        add_number('Волонтерам', mail='VolonterZoo@culture.mos.ru'),
        add_number('Отдел гуманитарных и творческих программ',
                   phone='+7 (499) 255-57-63'),
        add_number('Арт-Зебра', phone='+7 (906) 084-48-41',
                   mail='ArtzebraZoo@culture.mos.ru'),
        add_number('Заказ экскурсий', phone='+7 (499) 255-53-75',
                   mail='education@moscowzoo.ru'),
        add_number('Пресс-служба', mail='SaralievBS@culture.mos.ru'),
        add_number('Клуб Друзей Московского зоопарка (Опекунство)',
                   phone='+7 (962) 971-38-75', mail='zoofriends@moscowzoo.ru'),
        add_number('Сотрудничество, реализация спонсорских '
                   'и благотворительных программ',
                   mail='partnershipzoo@culture.mos.ru')]



@utils_router.message(F.photo)
async def get_photo_id(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f"ID твоей картинки:\n<code>{photo_id}</code>",
                         parse_mode="HTML")
    print(f"File ID: {photo_id}")
