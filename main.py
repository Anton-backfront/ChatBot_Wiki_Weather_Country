from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from configs import *
from weather_info import get_weather_any_city
from buttons import four_button
from country_INFO import get_country_info
from wikiped import get_wiki
from Chat_bot import generate_response
from database import get_user_number_by_chat_id, set_first_context, insert_message, get_all_user_id_and_full_name, \
    del_mes_by_user_id

# Контекст для чат бота

# Переменная для проверки включения режима общения для чат бота
chat_activated = False

bot = TeleBot(TOKEN_bot)


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    global chat_activated
    chat_activated = False
    chat_id = message.chat.id
    text = f'''Здравствуйте {message.from_user.full_name}
Для продолжения работы с ботом выберите один из четырех разделов, представленных ниже'''
    bot.send_message(chat_id, text, reply_markup=four_button())


@bot.message_handler(commands=['stop'])
def stop_handler(message):
    global chat_activated
    chat_activated = False

    # Отправляем сообщение с прощанием
    bot.send_message(message.chat.id, """До свидания! Надеюсь, мы скоро увидимся.
Нажмите start запуска бота""")


@bot.message_handler(func=lambda message: message.text == 'AllID')
def message_handler_for_del_message(message):
    user_ids = get_all_user_id_and_full_name()
    bot.send_message(message.chat.id, user_ids)


@bot.message_handler(func=lambda message: 'DeleteID' in message.text)
def message_handler_for_del_message(message):
    _, user_id = message.text.split('_')
    report = del_mes_by_user_id(user_id)

    bot.send_message(message.chat.id, report)


@bot.message_handler(regexp='☂️Weather')
def reaction_to_weather(message: Message):
    global chat_activated
    chat_activated = False
    chat_id = message.chat.id
    # del_wiki_word = message.id
    # bot.delete_message(chat_id, del_wiki_word)

    msg = bot.send_message(chat_id, '''<em><b>Вы зашли в раздел <u>Weather</u></b></em> ☂️ 
Введите город для поиска
(для отмены выберите в меню команду stop)''', reply_markup=ReplyKeyboardRemove(), parse_mode='html')
    bot.register_next_step_handler(msg, weather_result)


def weather_result(message: Message):
    chat_id = message.chat.id  # получаем id пользователя
    text = message.text  # отлавливаем слово отправленное в чат

    result = get_weather_any_city(text)

    dct_of_icons = {
        "Clouds": '☁️',
        "Clear": '☀️',
        "Rain": '🌧'
    }
    try:
        if result[1] >= 25.0:
            bot.send_message(chat_id, result[0] + f"\n🥵{dct_of_icons[result[2]]}", reply_markup=four_button())
        elif 5.0 <= result[1] < 25.0:
            bot.send_message(chat_id, result[0] + f"\n🫠{dct_of_icons[result[2]]}", reply_markup=four_button())
        elif result[1] < 5.0:
            bot.send_message(chat_id, result[0] + f"\n🥶{dct_of_icons[result[2]]}", reply_markup=four_button())
        else:
            bot.send_message(chat_id, result[0], reply_markup=four_button())
    except:
        bot.send_message(chat_id, 'Вы ввели не корректный город, попробуйте снова', reply_markup=four_button())


@bot.message_handler(regexp='🏙 Country Info')
def reaction_to_country_info(message: Message):
    global chat_activated
    chat_activated = False
    chat_id = message.chat.id
    # del_wiki_word = message.id
    # bot.delete_message(chat_id, del_wiki_word)

    msg = bot.send_message(chat_id, '''<b>Вы зашли в раздел <u>Country Info</u></b> 🏙️ 
Введите страну для поиска
(для отмены выберите в меню команду stop)''', reply_markup=ReplyKeyboardRemove(), parse_mode='html')
    bot.register_next_step_handler(msg, country_info_result)


def country_info_result(message: Message):
    chat_id = message.chat.id  # получаем id пользователя
    text = message.text  # отлавливаем слово отправленное в чат

    result = get_country_info(text)
    bot.send_message(chat_id, result, reply_markup=four_button())


@bot.message_handler(regexp='🌎 Wikipedia')
def reaction_to_wikipedia(message: Message):
    global chat_activated
    chat_activated = False
    chat_id = message.chat.id
    # del_wiki_word = message.id
    # bot.delete_message(chat_id, del_wiki_word)

    msg = bot.send_message(chat_id, '''<b>Вы зашли в раздел <u>Wikipedia</u></b> 🌎 
Введите ваш вопрос
(для отмены выберите в меню команду stop)''', reply_markup=ReplyKeyboardRemove(), parse_mode='html')
    bot.register_next_step_handler(msg, wikipedia_result)


def wikipedia_result(message: Message):
    chat_id = message.chat.id  # получаем id пользователя
    text = message.text  # отлавливаем слово отправленное в чат

    result = get_wiki(text)
    bot.send_message(chat_id, result, reply_markup=four_button())


@bot.message_handler(regexp='🎭 ️Chat Bot')
def reaction_to_chat_bot(message: Message):
    global chat_activated
    chat_activated = True

    chat_id = message.chat.id

    bot.send_message(chat_id, '''<b>Вы зашли в раздел <u>Chat Bot</u></b> 🎭
Теперь вы можете начать диалог с чат ботом
(для отмены выберите в меню команду stop)''', reply_markup=ReplyKeyboardRemove(), parse_mode='html')
    # bot.register_next_step_handler(msg, wikipedia_result)


@bot.message_handler(func=lambda message: True)
def message_handler_for_question(message):
    full_name = message.from_user.full_name
    chat_id = message.chat.id

    # Проверка что чат запущен
    if chat_activated:
        # Генерируем ответ на основе вопроса
        user_number = get_user_number_by_chat_id(chat_id, full_name)

        insert_message(user_number, 'user', message.text)
        response = generate_response(message.text)
        # Отправляем ответ
        bot.send_message(message.chat.id, response)


    else:
        bot.send_message(message.chat.id,
                         'Неправильная команда, Выберите один из четырех разделов, представленных ниже',
                         reply_markup=four_button())


bot.infinity_polling(none_stop=True, timeout=80)
