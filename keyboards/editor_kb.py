from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Редактировать данные о должниках')
b2 = KeyboardButton('/Редактировать данные о долгах')
b3 = KeyboardButton('/<--Назад')

kb_editor= ReplyKeyboardMarkup(resize_keyboard=True)

kb_editor.add(b1).add(b2).add(b3)