import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('data_base.db')

# Создаем курсор
cursor = conn.cursor()

# Создаем таблицу с названием "mytable"
cursor.execute('''CREATE TABLE list
                  (id INTEGER PRIMARY KEY,
                   table_name TEXT,
                   user_id INTEGER,
                   words TEXT)''')

# Создаем таблицу с названием "users"
cursor.execute('''CREATE TABLE user
                  (user_id INTEGER PRIMARY KEY,
                   start_date TEXT)''')

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()