import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operation`, `value`) VALUES (?, ?, ?)",
                            (self.get_user_id(user_id),
                             operation == "+",
                             value))
        return self.conn.commit()

    def get_records(self, user_id, within="all"):
        """Получаем историю о доходах/расходах"""

        if (within == "day"):
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif (within == "week"):
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        elif (within == "month"):
            result = self.cursor.execute(
                "SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
                (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? ORDER BY `date`",
                                         (self.get_user_id(user_id),))

        return result.fetchall()

    def addTask(self, user_id, taskname, description, deadline):
        """Создаем запись о задаче"""
        self.cursor.execute(
            "INSERT INTO `tasks` (`users_id`, `taskname`, `description`, `deadline`) VALUES (?, ?, ?, ?)",
            (self.get_user_id(user_id),
             taskname,
             description,
             deadline))
        return self.conn.commit()

    def delTask(self, users_id, task_id):
        """Удаляем запись о задаче"""
        self.cursor.execute("DELETE FROM `tasks` WHERE `users_id` = (?) AND `id` = (?)",
                            (self.get_user_id(users_id), task_id))
        return self.conn.commit()

    def getTasks(self, users_id):
        """Получаем все записи с задачами СОРТИРОВАНЫ ПО ДЕДЛАЙНУ"""

        self.cursor.execute("SELECT * FROM `tasks` WHERE `users_id` = (?) "
                            "ORDER BY `deadline`", (self.get_user_id(users_id), ))
        tasks = self.cursor.fetchall()

        return tasks

    def getTime(self, users_id):
        """Получаем время ДЕДЛАЙНА"""
        self.cursor.execute("SELECT deadline FROM tasks WHERE users_id = (?) ",
                            (self.get_user_id(users_id), ))
        deadline = self.cursor.fetchall()

        return deadline

    def getTaskname(self, users_id):
        """Получаем названия задач"""
        self.cursor.execute("SELECT taskname FROM tasks WHERE users_id = (?) ",
                            (self.get_user_id(users_id), ))
        taskname = self.cursor.fetchall()

        return taskname


    def addAlarm(self, user_id, notif):
        """Создаем запись о вкл/выкл уведомлений"""
        self.cursor.execute("INSERT INTO `alarm` (`users_id`, `notif`) VALUES (?, ?)",
                            (self.get_user_id(user_id), notif))
        return self.conn.commit()


    def getAlarm(self, users_id):
        """Получаем значение состояния уведомлений"""
        self.cursor.execute("SELECT notif FROM alarm WHERE users_id = (?) ORDER BY id DESC LIMIT 1",
                            (self.get_user_id(users_id), ))
        alarm = self.cursor.fetchall()

        return alarm

    def AlarmOff(self):
        """Выключаем все уведомления (используется при перезапуске бота)"""
        self.cursor.execute("DELETE FROM `alarm`")
        return self.conn.commit()


def close(self):
    """Закрываем соединение с БД"""
    self.connection.close()
