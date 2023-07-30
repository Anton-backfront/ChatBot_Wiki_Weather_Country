from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def four_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_wik = KeyboardButton(text='🌎 Wikipedia')
    btn_country = KeyboardButton(text='🏙 Country Info')
    btn_weather = KeyboardButton(text='☂️Weather')
    btn_chat = KeyboardButton(text='🎭 ️Chat Bot')

    # markup.add(btn, btn1, btn2)
    markup.row(btn_chat)
    markup.row(btn_wik, btn_weather, btn_country)
    return markup