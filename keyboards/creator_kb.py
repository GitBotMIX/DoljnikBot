from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Добавить данные о должниках')
b2 = KeyboardButton('/Добавить данные о долгах')
b3 = KeyboardButton('/<--Назад')

kb_creator= ReplyKeyboardMarkup(resize_keyboard=True)

kb_creator.add(b1).add(b2).add(b3)