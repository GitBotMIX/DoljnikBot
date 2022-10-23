from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, kb_editor, kb_creator, kb_delete
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from data_base import sqlite_db


class FSMAdmin(StatesGroup):
    debtors = State()
    longs = State()



            #DEBTORS
async def info_debtors(message: types.Message):
    infoDebtors = await sqlite_db.sql_read("debtors", message)
    if infoDebtors == False:
        await message.answer(f'Похоже у тебя нету должников')
    else:
        await message.answer(f'Список твоих должников:\n{infoDebtors}', parse_mode="MarkdownV2")

            #/DEBTORS

            #LONGS

async def info_longs(message: types.Message):
    infoDebtors = await sqlite_db.sql_read("longs", message)
    if infoDebtors == False:
        await message.answer(f'Похоже у тебя нету долгов')
    else:
        await message.answer(f'Список твоих долгов:\n{infoDebtors}', parse_mode="MarkdownV2")

            #/LONGS

            #ADD_NOTE
class MakeNote(StatesGroup):
    ADD_DEBTORS_NAME = State()
    ADD_DEBTORS_DEBTOR_SUM = State()
    ADD_DEBTORS_TOTAL = State()

    ADD_LONGS_NAME = State()
    ADD_LONGS_LONGS_SUM = State()
    ADD_LONGS_LONGS_TOTAL = State()
async def make_note_type(message: types.Message):
    await message.answer('Выбери данные о ком будем добавлять', reply_markup=kb_creator)

async def make_note_debtors_name(message: types.Message, state: FSMContext):
    await message.answer('Введи имя должника:')
    await MakeNote.ADD_DEBTORS_NAME.set()
    await MakeNote.next()
async def make_note_debtors_sum(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'debtors'):
        await message.answer('Данные о должнике уже есть в списке❌')
        await state.finish()
        return
    await message.answer('Сколько он тебе должен?:')
    async with state.proxy() as data:
        data['name'] = message.text
    await MakeNote.next()
async def make_note_debtors_total(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['long'] = message.text
    if await sqlite_db.sql_add_command(state, 'debtors', message):
        await message.answer('Данные о должнике успешно сохранены')
    else:
        await message.answer('В тексте найдены запрещенные символы❌')
    await state.finish()



async def make_note_longs_name(message: types.Message):
    await message.answer('Введи имя человека которому ты должен:')
    await MakeNote.ADD_LONGS_NAME.set()
    await MakeNote.next()
async def make_note_longs_sum(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'longs'):
        await message.answer('Данные о должнике уже есть в списке❌')
        await state.finish()
        return
    await message.answer('Сколько ты ему должен?:')
    async with state.proxy() as data:
        data['name'] = message.text
    await MakeNote.next()
async def make_note_longs_total(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['long'] = message.text
    if await sqlite_db.sql_add_command(state, 'longs', message):
        await message.answer('Данные о должнике успешно сохранены')
    else:
        await message.answer('В тексте найдены запрещенные символы❌')
    await state.finish()

            #/ADD_NOTE

            #DELETE


class DeleteNoteDebtorsStates(StatesGroup):
    INPUT_NAME_DEBTORS = State()
    PERFORM_REMOVE_DEBTORS = State()

async def delete_note(message: types.Message):
    await message.answer('Выбери какого типа запись удалить', reply_markup=kb_delete)

async def delete_note_debtors(message: types.Message):
    if await sqlite_db.sql_read("debtors", message) != False:
        await message.answer('Введи имя должника:')
        await message.answer(f'{await sqlite_db.sql_read("debtors", message)}', parse_mode="MarkdownV2")
        await DeleteNoteDebtorsStates.INPUT_NAME_DEBTORS.set()
        await DeleteNoteDebtorsStates.next()
    else:
        await message.answer('Похоже у тебя нету должников❌')


async def delete_note_debtors_execute(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'debtors'):
        await sqlite_db.sql_delete(message, 'debtors')
        await message.answer(f'Успешно удалил запись о должнике "{message.text}"', reply_markup=kb_client)
    else:
        await message.answer(f'Такого должника нет в списке ')
    await state.finish()

class DeleteNoteLongsStates(StatesGroup):
    INPUT_NAME_LONGS = State()
    PERFORM_REMOVE_LONGS = State()

async def delete_note_longs(message: types.Message):
    if await sqlite_db.sql_read("longs", message) != False:
        await message.answer(f'Введи имя человека которому ты должен:{await sqlite_db.sql_read("longs", message)}', parse_mode="MarkdownV2")
        await DeleteNoteLongsStates.INPUT_NAME_LONGS.set()
        await DeleteNoteLongsStates.next()
    else:
        await message.answer('Похоже у тебя нету долгов❌')

async def delete_note_longs_execute(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'longs'):
        await sqlite_db.sql_delete(message, 'longs')
        await message.answer(f'Успешно удалил запись о "{message.text}"', reply_markup=kb_client)
    else:
        await message.answer(f'Такого имени нету в списке ')
    await state.finish()

            #/DELETE



            #EDITOR
class EditorStates(StatesGroup):
    INPUT_DEBTOR = State()
    NEW_DEBTOR = State()
    NEW_DEBTOR_APPLY = State()

    INPUT_LONGS = State()
    NEW_LONGS = State()
    NEW_LONGS_APPLY = State()


async def editor(message: types.Message):
    await message.answer('Выбери данные какой категории будем изменять', reply_markup=kb_editor)

async def editor_debtors(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_read("debtors", message) != False:
        await message.answer(f'Введи имя должника чью запись будем редактировать:\n{await sqlite_db.sql_read("debtors", message)}', parse_mode="MarkdownV2")
        await EditorStates.INPUT_DEBTOR.set()
        await EditorStates.next()
    else:
        await message.answer('Похоже у тебя нету должников❌')
        await state.finish()
async def editor_debtors_set_new(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'debtors'):
        await message.answer('Введи новую сумму долга:')
        async with state.proxy() as data:
            data['nameDebtor'] = message.text
        await EditorStates.next()
    else:
        await message.answer('Такого должника нет в списке!❌')
        await state.finish()

async def editor_debtors_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['newDebt'] = message.text
    async with state.proxy() as data:
        await sqlite_db.sql_update(state, 'debtors')
        await message.answer(f'Успешно отредактировал запись о должнике *{tuple(data.values())[0]}*',
                             reply_markup=kb_client, parse_mode='MarkdownV2')
    await state.finish()



async def editor_longs(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_read("longs", message) != False:
        await message.answer(f'Введи имя человека которому ты должен:\n{await sqlite_db.sql_read("longs", message)}', parse_mode="MarkdownV2")
        await EditorStates.INPUT_LONGS.set()
        await EditorStates.next()
    else:
        await message.answer('Похоже у тебя нету долгов❌')
        await state.finish()

async def editor_longs_set_new(message: types.Message, state: FSMContext):
    if await sqlite_db.sql_name_check_message(message, 'longs'):
        await message.answer('Введи новую сумму твоего долга:')
        async with state.proxy() as data:
            data['nameLong'] = message.text
        await EditorStates.next()
    else:
        await message.answer('Такого должника нет в списке!❌')
        await state.finish()

async def editor_longs_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['newLong'] = message.text
    async with state.proxy() as data:
        await sqlite_db.sql_update(state, 'longs')
        await message.answer(f'Успешно отредактировал запись о долге *{tuple(data.values())[0]}*',
                             reply_markup=kb_client, parse_mode='MarkdownV2')
    await state.finish()
            #/EDITOR


async def user_id(message: types.Message):
    await message.answer(f'Твой ID: {message.from_user.id}')

async def help(message: types.Message):
    await message.answer(f'Приветствую, я бот который поможет тебе контролировать информацию о твоих должниках и долгах.\n'
                         f'Для начала воспользуйся любой командой из предложенных, в твоем меню, что-бы его открыть, '
                         f'нажми на квадрат с 4 точками по центру, который возле эмодзи.'
                         f'\nСписок "быстрых" команд:\n'
                         f'/Должники\n'
                         f'/Долги\n'
                         f'/Добавить данные о должниках\n'
                         f'/Добавить данные о долгах\n'
                         f'/Редактировать данные о должниках\n'
                         f'/Редактировать данные о долгах\n'
                         f'/Удалить запись о должнике\n'
                         f'/Удалить запись о долгах',
                         reply_markup=kb_client, parse_mode="Markdown")

#Если возникли какие-либо вопросы по работе бота писать сюда - https://vk.com/nikitamixxxx
async def get_client_keyboard(message: types.Message):
    await message.answer('*Главное меню*', reply_markup=kb_client, parse_mode="MarkdownV2")


def register_handlers_client(dp : Dispatcher):
            #DEBTORS
    dp.register_message_handler(info_debtors, commands=['Должники'])
            #/DEBTORS

    dp.register_message_handler(info_longs, commands=['Долги'])

            #EDITOR
    dp.register_message_handler(editor, commands=['Редактор'])
    dp.register_message_handler(editor_debtors, text_contains=['Редактировать данные о должниках'])
    dp.register_message_handler(editor_longs, text_contains=['Редактировать данные о долгах'])
    dp.register_message_handler(editor_debtors_set_new, state=EditorStates.NEW_DEBTOR)
    dp.register_message_handler(editor_debtors_finish, state=EditorStates.NEW_DEBTOR_APPLY)

    dp.register_message_handler(editor_longs_set_new, state=EditorStates.NEW_LONGS)
    dp.register_message_handler(editor_longs_finish, state=EditorStates.NEW_LONGS_APPLY)
            #/EDITOR


            #DELETE
    dp.register_message_handler(delete_note, text_contains=['Удалить запиcь'])
    dp.register_message_handler(delete_note_debtors, text_contains=['Удалить запись о должнике'])
    dp.register_message_handler(delete_note_debtors_execute,state=DeleteNoteDebtorsStates.PERFORM_REMOVE_DEBTORS)
    dp.register_message_handler(delete_note_longs, text_contains=['Удалить запись о долгах'])
    dp.register_message_handler(delete_note_longs_execute, state=DeleteNoteLongsStates.PERFORM_REMOVE_LONGS)


            #/DELETE
            #ADD_NOTE
    dp.register_message_handler(make_note_type, text_contains=['Добавить запись'])
    dp.register_message_handler(make_note_debtors_name, text_contains=['Добавить данные о должниках'])
    dp.register_message_handler(make_note_debtors_sum, state=MakeNote.ADD_DEBTORS_DEBTOR_SUM)
    dp.register_message_handler(make_note_debtors_total, state=MakeNote.ADD_DEBTORS_TOTAL)
    dp.register_message_handler(make_note_longs_name, text_contains=['Добавить данные о долгах'])
    dp.register_message_handler(make_note_longs_sum, state=MakeNote.ADD_LONGS_LONGS_SUM)
    dp.register_message_handler(make_note_longs_total, state=MakeNote.ADD_LONGS_LONGS_TOTAL)
            #/ADD_NOTE

    dp.register_message_handler(get_client_keyboard, commands=['<--Назад'])
    dp.register_message_handler(help, commands=['start'])
    dp.register_message_handler(user_id, commands=['id'])
