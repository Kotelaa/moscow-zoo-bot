from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.utils.formatting import Bold, as_list, as_line
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards import survey_options_kb, share_keyboard
from quiz_questions import QUIZ_QUESTIONS, RESULTS
from const import SURVEY_MESSAGE, START_SURVEY_MESSAGE
from TokenData import ADMIN_ID


DEFAULT_QUIZ_DATA = {
    'current_step': 0,
    'scores': {'mammals': 0, 'birds': 0, 'reptiles': 0, 'amphibians': 0}
}

router_quiz = Router()


class Quiz(StatesGroup):
    asking = State()
    finished = State()


@router_quiz.message(Command('survey'))
async def start_survey(message: Message):
    """ Asks user if he/she wants start survey """
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='🚀 Начать викторину',
                                callback_data='run_quiz'))
    kb.row(InlineKeyboardButton(text='⏰ Приступлю позже',
                                callback_data='cancel_quiz'))

    await message.answer(START_SURVEY_MESSAGE.as_html(),
                         reply_markup=kb.as_markup(),
                         parse_mode='HTML')


@router_quiz.callback_query(F.data == 'run_quiz')
async def run_quiz(callback: CallbackQuery, state: FSMContext):
    """ Function starts the survey"""
    await callback.answer()
    await state.set_state(Quiz.asking)
    await state.update_data(**DEFAULT_QUIZ_DATA)

    await callback.message.delete()
    await handle_survey(callback.message, state)


@router_quiz.callback_query(F.data == 'cancel_quiz')
async def cancel_quiz(callback: CallbackQuery, state: FSMContext):
    """ When the user has decided to postpone the test  """
    await callback.answer('Жаль, будем ждать вас позже!')
    await callback.message.edit_text(
        'Ничего страшного! Вы можете запустить викторину в любое время '
        'командой /survey. Хорошего дня! ✨'
    )
    await state.clear()


@router_quiz.message(Quiz.asking)
async def handle_survey(message: Message, state: FSMContext):
    """ Asks questions about the user's compatibility with different animals """
    data = await state.get_data()
    current_step = data.get('current_step', 0)
    scores = data.get('scores', {'mammals': 0, 'birds': 0, 'reptiles': 0,
                                 'amphibians': 0})

    if current_step > 0:
        prev_question = QUIZ_QUESTIONS[current_step-1]
        user_answer = message.text

        answer_result = prev_question.get('options').get(user_answer)
        if answer_result:
            scores[answer_result] += 1

    if current_step < len(QUIZ_QUESTIONS):
        question_data = QUIZ_QUESTIONS[current_step]
        question = question_data.get('question')
        answers = list(question_data.get('options').keys())
        kb = survey_options_kb(answers)
        await message.answer(question, reply_markup=kb)
        await state.update_data(current_step=current_step+1, scores=scores)

    else:
        winner = max(scores, key=scores.get)
        await show_result(message, state, winner)


async def show_result(message: Message, state: FSMContext, winner: str):
    await message.answer(text='Загружаю результат...',
                         reply_markup=ReplyKeyboardRemove())

    survey_result = RESULTS.get(winner)
    content = as_list(
        f'Тест завершен!',
        f"{survey_result.get('message')}",
        '\n',
        SURVEY_MESSAGE
    )

    await message.answer_photo(photo=survey_result.get('image'),
                               caption=content.as_html(),
                               reply_markup=share_keyboard(survey_result.get('animal'))
    )

    winner_animal = survey_result.get('animal')
    await state.update_data(quiz_result=winner_animal)


@router_quiz.callback_query(F.data == 'contact_staff')
async def contact_staff(callback: CallbackQuery, state: FSMContext):
    """ Processes the request to contact an employee of the ZOO """
    user_data = await state.get_data()
    result = user_data.get('quiz_result', 'Неизвестно')

    user = callback.from_user

    admin_message = as_list(
        Bold('🚀 Новая заявка на консультацию! \n\n'),
        as_line(Bold('Пользователь: '), f'{user.username or 'нет юзернейма'}\n'),
        as_line(Bold('Имя: '), f'{user.full_name}'),
        as_line(Bold('ID: '), f'{user.id}'),
        as_line(Bold('Результат теста: '), f'{result}')
    )
    callback_answer = ("Заявка отправлена! Сотрудник свяжется с вами "
                       "в ближайшее время.")

    try:
        await callback.bot.send_message(chat_id=ADMIN_ID,
                                        text=admin_message.as_html())
        await callback.answer(callback_answer, show_alert=True)

        await state.clear()

    except Exception as e:
        await callback.answer("Ошибка при отправке заявки.")
        print(f'Ошибка: {e}')
