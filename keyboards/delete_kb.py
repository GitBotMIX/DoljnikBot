from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Удалить запись о должнике')
b2 = KeyboardButton('/Удалить запись о долгах')
b3 = KeyboardButton('/<--Назад')

kb_delete= ReplyKeyboardMarkup(resize_keyboard=True)

kb_delete.add(b1).add(b2).add(b3)