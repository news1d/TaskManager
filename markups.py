from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Главное меню
btnTask = KeyboardButton('📝 Менеджер задач')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTask)

# Менеджер задач (вкл. уведомления)
btnAdd = KeyboardButton('📌 Добавить')
btnList = KeyboardButton('📃 Список')
btnAl = KeyboardButton('✅ Включить уведомления')
taskMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl)

# Менеджер задач (выкл. уведомления)
btnAdd = KeyboardButton('📌 Добавить')
btnList = KeyboardButton('📃 Список')
btnAl = KeyboardButton('❌ Отключить уведомления')
taskMenu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl)

# Cписок задач
listMenu = InlineKeyboardMarkup(row_width=1)
btnInList = InlineKeyboardButton(text='🗑 Удалить', callback_data='Delete')
listMenu.insert(btnInList)

# Отмена
btnCancel = KeyboardButton('❌ Отмена')
canMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)