from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from dispatcher import dp
import asyncio
import re
from bot import BotDB
from datetime import datetime, timedelta
import markups as nav
import sqlite3
import ast


# создаем форму задачи и указываем поля
class Form(StatesGroup):
    task_name = State()
    description = State()
    deadline = State()
    del_name = State()
    fin_spent = State()
    fin_earned = State()


# стартовый метод
@dp.message_handler(commands="start")
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Привет! Я бот, разработанный группой КС-38 'MUJIKI', " + \
                                   "университета РХТУ им. Д.И.Менделеева. " + \
                                   "\nЯ являюсь менеджером задач.", reply_markup=nav.mainMenu)


@dp.message_handler()
async def main_handler(message: types.Message):
    # -------------------Менеджер задач------------------->
    if message.text == '📝 Менеджер задач':
        notif = str(BotDB.getAlarm(message.from_user.id)).replace(',', '').replace('(', '').replace(')', '').replace("'", '').replace('[', '').replace(']', '')
        if notif == 'on':
            await message.bot.send_message(message.from_user.id, 'Меню менеджера задач', reply_markup=nav.taskMenu1)
        elif notif == 'off':
            await message.bot.send_message(message.from_user.id, 'Меню менеджера задач', reply_markup=nav.taskMenu)
        else:
            await message.bot.send_message(message.from_user.id, 'Меню менеджера задач', reply_markup=nav.taskMenu)

    elif message.text == '📌 Добавить':
        await Form.task_name.set()
        await message.answer("Введите название задачи: ", reply_markup=nav.canMenu)

    elif message.text == '🏠 Главное меню':
        await message.bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=nav.mainMenu)

    elif message.text == '✅ Включить уведомления' or message.text == '❌ Отключить уведомления':

        if message.text == '✅ Включить уведомления':
            notif = "on"
            BotDB.addAlarm(message.from_user.id, notif)
            await message.bot.send_message(message.from_user.id, "✅ Уведомления включены!", reply_markup=nav.taskMenu1)
        elif message.text == '❌ Отключить уведомления':
            notif = "off"
            BotDB.addAlarm(message.from_user.id, notif)
            await message.bot.send_message(message.from_user.id, "❌ Уведомления отключены!", reply_markup=nav.taskMenu)

        while notif == 'on':

            deadline = BotDB.getTime(message.from_user.id)
            taskname = BotDB.getTaskname(message.from_user.id)
            notif = str(BotDB.getAlarm(message.from_user.id)).replace(',', '').replace('(', '').replace(')','').replace("'",'').replace('[', '').replace(']', '')

            i = 0
            while i < len(deadline):
                time_30 = datetime.now() + timedelta(minutes=30)
                time_5 = datetime.now() + timedelta(minutes=5)
                time_deadline = datetime.now()

                name = str(taskname[i])
                name = name.replace(',', '').replace('(', '').replace(')', '').replace("'", '')

                alarm = str(deadline[i])
                alarm = alarm.replace(',', '').replace('(', '').replace(')', '').replace("'", '')
                alarm = datetime.strptime(alarm, '%d-%m %H:%M')

                i += 1

                if time_30.strftime("%d-%m %H:%M") == alarm.strftime('%d-%m %H:%M'):
                    answer = '❌До дедлайна задачи "' + str(name) + '" осталось 30 минут!❌'
                    await message.bot.send_message(message.from_user.id, answer)
                    await asyncio.sleep(60)
                elif time_5.strftime("%d-%m %H:%M") == alarm.strftime('%d-%m %H:%M'):
                    answer = '❌До дедлайна задачи "' + str(name) + '" осталось 5 минут!❌'
                    await message.bot.send_message(message.from_user.id, answer)
                    await asyncio.sleep(60)
                elif time_deadline.strftime("%d-%m %H:%M") == alarm.strftime('%d-%m %H:%M'):
                    answer = '❌Дедлайн задачи "' + str(name) + '"!❌'
                    await message.bot.send_message(message.from_user.id, answer)
                    await asyncio.sleep(60)

            await asyncio.sleep(1)

    elif message.text == '📃 Список':
        tasks = BotDB.getTasks(message.from_user.id)

        if len(tasks):
            count_tasks = len(tasks)
            answer1 = "Количество ваших задач:  " + str(count_tasks) + "\n\nПолный список:"
            await message.answer(answer1)
            i = 0
            for t in tasks:
                i += 1
                answer2 = "❗Задача #" + str(i) + \
                          "\n✏Название: " + str(t[2]) + \
                          "\n📄Описание: " + str(t[3]) + \
                          "\n🕘Дедлайн: " + str(t[4]) + \
                          "\n\nID: " + str(t[0])

                await message.answer(answer2, reply_markup=nav.listMenu)
        else:
            await message.reply("Задач не обнаружено!")

    # -------------------Финансовый менеджер------------------->
    elif message.text == '📊 Финансовый менеджер':
        await message.bot.send_message(message.from_user.id, 'Меню финансового менеджера', reply_markup=nav.finMenu)

    elif message.text == '📉 Внести расходы':
        await Form.fin_spent.set()
        await message.answer("Введите число: ", reply_markup=nav.canMenu)

    elif message.text == '📈 Внести доходы':
        await Form.fin_earned.set()
        await message.answer("Введите число: ", reply_markup=nav.canMenu)

    elif message.text == '🗂 История':
        await message.bot.send_message(message.from_user.id, 'Выберите подходящий период', reply_markup=nav.hisMenu)

    elif message.text == '🔄 Назад':
        await message.bot.send_message(message.from_user.id, 'Вы вернулись в меню финансового менеджера',
                                       reply_markup=nav.finMenu)

    elif message.text == '1️⃣ День' or message.text == '7️⃣ Неделя' or message.text == '🔢 Месяц':

        if message.text == '1️⃣ День':
            within = 'day'
        elif message.text == '7️⃣ Неделя':
            within = 'week'
        elif message.text == '🔢 Месяц':
            within = 'month'

        records = BotDB.get_records(message.from_user.id, within)

        total_earned = 0
        total_spent = 0

        if len(records):
            if within == 'day':
                answer = f"🕘 История операций за день:\n\n"
            elif within == 'week':
                answer = f"🕘 История операций за неделю:\n\n"
            elif within == 'month':
                answer = f"🕘 История операций за месяц:\n\n"

            for r in records:
                answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
                answer += f" - {r[3]}"
                answer += f" <i>({r[4]})</i>\n"
                if r[2]:
                    total_earned += r[3]
                else:
                    total_spent += r[3]

            answer += f'\n📈 <b>Общий доход:</b> {total_earned}\n📉 <b>Общий расход:</b> {total_spent}'

            await message.answer(answer)
        else:
            await message.reply("Записей не обнаружено!")

    else:
        await message.reply("Я не знаю такой команды...")


# добавляем возможность отмены, если пользователь передумал
@dp.message_handler(commands='cancel')
@dp.message_handler(Text(equals='❌ отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Действие отменено!', reply_markup=nav.mainMenu)


@dp.message_handler(state=Form.fin_spent)
async def process_fin_spent(message: types.Message, state: FSMContext):
    operation = '-'
    value = message.text
    if len(value):
        x = re.findall(r"\d+(?:.\d+)?", value)
        if len(x):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value)

            await message.reply("✅ Запись о <u><b>расходе</b></u> успешно внесена!", reply_markup=nav.finMenu)

        else:
            await message.reply("Не удалось определить сумму!", reply_markup=nav.finMenu)
    else:
        await message.reply("Не введена сумма!", reply_markup=nav.finMenu)
    await state.finish()


@dp.message_handler(state=Form.fin_earned)
async def process_fin_earned(message: types.Message, state: FSMContext):
    operation = '+'
    value = message.text
    if len(value):
        x = re.findall(r"\d+(?:.\d+)?", value)
        if len(x):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value)

            await message.reply("✅ Запись о <u><b>доходе</b></u> успешно внесена!", reply_markup=nav.finMenu)
        else:
            await message.reply("Не удалось определить сумму!", reply_markup=nav.finMenu)
    else:
        await message.reply("Не введена сумма!", reply_markup=nav.finMenu)
    await state.finish()


# TASK MANAGER --->
@dp.message_handler(state=Form.task_name)
async def process_taskname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_name'] = message.text

    await Form.next()
    await message.answer("Введите описание задачи:")


@dp.message_handler(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await Form.next()
    await message.answer("Введите дедлайн задачи в формате ДД-ММ ЧЧ:ММ:")


@dp.message_handler(state=Form.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['deadline'] = message.text

        try:
            if datetime.strptime(data['deadline'], '%d-%m %H:%M'):
                task_name = data['task_name']
                description = data['description']
                deadline = data['deadline']

                BotDB.addTask(message.from_user.id, task_name, description, deadline)

                await state.finish()
                await message.answer("✅ Задача под названием '" + task_name + "' успешно внесена!",
                                     reply_markup=nav.taskMenu)
        except Exception:
            await message.answer('Ошибка! Проверьте формат ввода данных')


@dp.callback_query_handler(text='Delete')
async def task_delete(callback_query: types.CallbackQuery):
    temp_id = callback_query.message.text
    id = temp_id.split()[-1]
    BotDB.delTask(callback_query.from_user.id, id)
    await callback_query.message.delete()
    await callback_query.answer('Задача удалена!')