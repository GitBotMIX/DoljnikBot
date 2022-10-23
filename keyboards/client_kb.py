from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Должники')
b2 = KeyboardButton('/Долги')
b3 = KeyboardButton('/Добавить запись')
b4 = KeyboardButton('/Удалить запиcь')
b5 = KeyboardButton('/Редактор')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2).add(b3).add(b4).add(b5)