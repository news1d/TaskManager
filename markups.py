from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# btnMain = KeyboardButton('🏠 Главное меню')
# Главное меню
btnTask = KeyboardButton('📝 Менеджер задач')
# btnFin = KeyboardButton('📊 Финансовый менеджер')
# mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTask, btnFin)
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTask)


# Менеджер задач (вкл. уведомления)
btnAdd = KeyboardButton('📌 Добавить')
btnList = KeyboardButton('📃 Список')
btnAl = KeyboardButton('✅ Включить уведомления')
taskMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl)
# taskMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl, btnMain)

# Менеджер задач (выкл. уведомления)
btnAdd = KeyboardButton('📌 Добавить')
btnList = KeyboardButton('📃 Список')
btnAl = KeyboardButton('❌ Отключить уведомления')
taskMenu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl)
# taskMenu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdd, btnList, btnAl, btnMain)

# Cписок задач
listMenu = InlineKeyboardMarkup(row_width=1)
btnInList = InlineKeyboardButton(text='🗑 Удалить', callback_data='Delete')
listMenu.insert(btnInList)

# Финансовый менеджер
# btnEar = KeyboardButton('📈 Внести доходы')
# btnSp = KeyboardButton('📉 Внести расходы')
# btnHis = KeyboardButton('🗂 История')
# finMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnEar, btnSp, btnHis, btnMain)


# История расходов/доходов
btnDay = KeyboardButton('1️⃣ День')
btnWeek = KeyboardButton('7️⃣ Неделя')
btnMon = KeyboardButton('🔢 Месяц')
btnBack = KeyboardButton('🔄 Назад')
hisMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnDay, btnWeek, btnMon, btnBack)

# Отмена
btnCancel = KeyboardButton('❌ Отмена')
canMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)