import sqlite3

# Функция для создания таблицы пользователей
def create_users_table():
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT NOT NULL UNIQUE,
        user_number INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT
    );
    ''')
    database.commit()
    database.close()


# create_users_table()

def create_messages_table():
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages(
        user_number INTEGER REFERENCES users(user_number),
        role TEXT,
        content TEXT
    );
    ''')
    database.commit()
    database.close()


# create_messages_table()

def set_user_info(user_id, full_name):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute('''
        INSERT INTO users(user_id, full_name) VALUES
        (?, ?)
        ''', (user_id, full_name))
    database.commit()
    database.close()


def set_first_context(user_id):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute('''
       INSERT INTO messages(user_number, role, content) VALUES
       ((SELECT user_number FROM users WHERE user_id = ?), "system", "You are a professional in all areas and can answer any questions."),
       ((SELECT user_number FROM users WHERE user_id = ?), "user", "I'm interested in everything"),
       ((SELECT user_number FROM users WHERE user_id = ?), "assistant", "What questions do you have")
       ''', (user_id, user_id, user_id))
    database.commit()
    database.close()

# set_first_context(1)

def get_user_number_by_chat_id(user_id, full_name):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute(f'''
            SELECT user_number FROM users WHERE user_id={user_id}
            ''')
    result = cursor.fetchone()
    database.close()

    if result is not None:

        return result[0]
    else:

        set_user_info(user_id, full_name)
        set_first_context(user_id)
        get_user_number_by_chat_id(user_id, full_name)



# get_user_number_by_chat_id(23232, 'Ulugbek')
# get_user_number_by_chat_id(34567, 'Anton H')




# set_user_info(34567, "Anton H")
# set_user_info(22222, "Anatol")



# def get_user_number(user_id):
#     database = sqlite3.connect('Chat_bot_history.db')
#     cursor = database.cursor()
#     cursor.execute(f'''
#                 SELECT user_number FROM users WHERE user_id={user_id}
#                 ''')
#     result = cursor.fetchall()
#     database.close()

#     return result






def insert_message(user_number, role, content):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO messages(user_number, role, content) VALUES
    (?, ?, ?)
    ''', (user_number, role, content))
    database.commit()
    database.close()


# insert_message(1, 'user', 'Hello, how is it going?')

def get_all_messages_by_user_id(user_number):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute(f'''
        SELECT * FROM messages WHERE user_number = {user_number}
        ''')
    result = cursor.fetchall()
    database.close()
    result_str_finally = "\n".join([f"{x[1]}: {x[2]}" for x in result])
    # print(result_str_finally)
    # # print(", "join(result))
    return result_str_finally


# get_all_messages_by_user_id(1)

def get_all_user_id_and_full_name():

    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute(f'''
            SELECT DISTINCT user_id, full_name FROM users;
            ''')
    result = cursor.fetchall()
    database.close()
    result_str = "\n".join([f"{x[0]}, {x[1]}" for x in result])
    return result_str

# print(get_all_user_id_and_full_name())

def del_mes_by_user_id(user_id):
    database = sqlite3.connect('Chat_bot_history.db')
    cursor = database.cursor()
    cursor.execute(f'''
                DELETE FROM messages WHERE user_number = (SELECT user_number FROM users WHERE user_id = {user_id});
                ''')
    cursor.execute(f'''
                DELETE FROM users WHERE user_id = {user_id};
                ''')
    database.commit()
    database.close()
    return f"История переводов {user_id} успешно очищена 🔥"



# del_mes_by_user_id(34567)