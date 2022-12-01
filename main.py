import telebot
from telebot import types
import time


# API_KEY = '5924672396:AAEsfX7vyFgA3uy7GrugRR5w8_rXfhW54U8'

API_KEY = '5855326170:AAE5CJw2wI1kVe19nhMgB-YsKySaR5M7Qag'

CHAT_ID = -1001818313548

# CHAT_ID = 640348124

# USER_ID = 640348124

USER_ID = 748736705

PASSWORD = '1234'

П1 = 100

П2 = 20

bot = telebot.TeleBot(API_KEY)

USER_DICT = {}

RAS_DICT = {}

class User:
    def __init__(self, name):
        self.name = name
        self.birthday = None
        self.tel = None



@bot.message_handler(commands=['edit'])
def edit(message):
    try:
        if message.from_user.id == USER_ID:
            send = bot.reply_to(message, 'Пароль:')
            bot.register_next_step_handler(send, edit_2)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, повторите операцию. /edit')


def edit_2(message):
    try:
        if message.text == PASSWORD:
            send = bot.reply_to(message, 'Введите новый ID:')
            bot.register_next_step_handler(send, edit_3)
        else:
            bot.send_message(message.chat.id, 'Ошибка!')
            bot.send_message(message.chat.id, 'Для повторной попытки нажмите на /edit!')
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, повторите операцию. /edit')


def edit_3(message):
    try:
        global CHAT_ID
        CHAT_ID = message.text
        bot.send_message(message.chat.id, 'ID сменен успешно!')
        bot.send_message(message.chat.id, 'Для активации бота нажмите на /start')
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, повторите операцию. /edit')


@bot.message_handler(commands=['start'])
def start_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    credit = types.KeyboardButton('Расчитать сумму')
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы расчитать сумму нажмите на кнопку "Расчитать сумму"', reply_markup=markup)
    bot.register_next_step_handler(message, start_2)


def start_2(message):
    if message.text != 'Расчитать сумму' and message.text != 'Пересчитать сумму':
        start_1(message=bot.reply_to(message, 'Пожалуйста, нажмите на кнопку для расчетв'))
    else:
        send = bot.reply_to(message, 'Укажите цену товара')
        bot.register_next_step_handler(send, review_1)
    

def review_1(message):
    try:
        if int(message.text) // int(message.text) == 1:
            sum = message.text
            RAS_DICT['sum'] = int(sum)
            send = bot.reply_to(message, 'Укажите первоначальный взнос:')
            bot.register_next_step_handler(send, review_2)
    except:
            send = bot.reply_to(message, 'Укажите цифрами')
            bot.register_next_step_handler(send, review_1)


def review_2(message):
    try:
        if int(message.text) // int(message.text) == 1:
            per_vznos = message.text
            RAS_DICT['per_vznos'] = int(per_vznos)
            send = bot.reply_to(message, 'Укажите срок расрочки:')
            bot.register_next_step_handler(send, review_3)
    except:
        send = bot.reply_to(message, 'Укажите цифрами')
        bot.register_next_step_handler(send, review_2)


def review_3(message):
    try:
        int(message.text) // int(message.text) == 1
    except ValueError:
        send = bot.reply_to(message, 'Укажите цифрами')
        bot.register_next_step_handler(send, review_3)
    else:
        if int(message.text) < 2 or int(message.text) > 12:
            send = bot.reply_to(message, 'Максимальное кол-во месяцев 12, а минимальное 2')
            bot.register_next_step_handler(send, review_3)
        else:
            srok = message.text
            RAS_DICT['srok'] = int(srok)
            A = RAS_DICT['sum']
            B = RAS_DICT['per_vznos']
            C = RAS_DICT['srok']
            if C >= 2 and C <= 11:
                if C == 2:
                    K1 = 0.09
                    K2 = 0.17
                elif C == 3:
                    K1 = 0.08
                    K2 = 0.16
                elif C == 4:
                    K1 = 0.065
                    K2 = 0.138
                elif C == 5:
                    K1 = 0.053
                    K2 = 0.12
                elif C >= 6 and C <= 8:
                    K1 = 0.05
                    K2 = 0.115
                elif C == 9:
                    K1 = 0.045
                    K2 = 0.11
                elif C >= 10 and C <= 11:
                    K1 = 0.04
                    K2 = 0.105
                try:
                    (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)
                except ZeroDivisionError:
                    send = bot.reply_to(message, 'Вы ввели так, что поделилось на 0')
                    bot.register_next_step_handler(send, review_3)
                else:
                    res_1 = (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)
                    bot.send_message(message.chat.id, round(res_1))
            else:
                K1 = 0.04
                K2 = 0.105
                try:
                    (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1
                except ZeroDivisionError:
                    send = bot.reply_to(message, 'Вы ввели так, что поделилось на 0')
                    bot.register_next_step_handler(send, review_3)
                else:
                    res_2 = (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1
                    bot.send_message(message.chat.id, round(res_2))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
            credit = types.KeyboardButton('Сформировать онлайн заявку')
            raschet = types.KeyboardButton('Пересчитать сумму')
            markup.add(credit, raschet)
            send = bot.send_message(
            message.chat.id,
            'Если вас устраивает цена нажмите на "Сформировать онлайн заявку", если нет на "Пересчитать сумму"',
            reply_markup=markup
            )
            bot.register_next_step_handler(send, func)


def func(message):
    if message.text == 'Сформировать онлайн заявку':
        review_5(message=message)
    elif message.text == 'Пересчитать сумму':
        start_2(message=message)


def review_4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    credit = types.KeyboardButton('Сформировать онлайн заявку')
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы оформить рассрочку нажмите на кнопку "Сформировать онлайн заявку"', reply_markup=markup)
    bot.register_next_step_handler(message, review_5)


def review_5(message):
    if message.text != 'Сформировать онлайн заявку':
        review_4(message=bot.reply_to(message, 'Пожалуйста, нажмите на кнопку для получения рассрочки'))
    else:
        send = bot.reply_to(message, 'Внесите ваши Фамилию Имя Отчество полностью, например\n Иванов Иван Иванович')
        bot.register_next_step_handler(send, review_6)
    

def review_6(message):
    if any(map(str.isdigit, message.text)):
        send = bot.reply_to(message, 'Без цифр')
        bot.register_next_step_handler(send, review_6)
    else:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        USER_DICT[chat_id] = user
        send = bot.reply_to(message, 'Укажите дату рождения в формате 01.01.2000:')
        bot.register_next_step_handler(send, review_7)


def review_7(message):
    chat_id = message.chat.id
    birthday = message.text
    user = USER_DICT[chat_id]
    user.birthday = birthday
    send = bot.reply_to(message, 'Укажите телефон:')
    bot.register_next_step_handler(send, review_8)


def review_8(message):
    chat_id = message.chat.id
    tel = message.text
    user = USER_DICT[chat_id]
    user.tel = tel
    bot.send_message(message.chat.id, 'Ваша заявка принята, в ближайшее время наш менеджер свяжется с вами.')
    message_to_save = f'{user.name} \n {user.birthday} \n {user.tel}'
    try:
        bot.send_message(CHAT_ID, message_to_save)
    except:
        bot.send_message(message.chat.id, 'Сервер перезагрузился, пожалуйста, укажите ID чата через /edit')
    time.sleep(3)
    bot.send_message(message.chat.id, 'Если вы хотите оставить еще одну заявку запустите бота снова /start')


@bot.message_handler(content_types=['text'])
def not_found(message):
    if message.text != '/edit' and message.text != '/start' and message.text != 'Сформировать онлайн заявку' and message.text != 'Пересчитать сумму' and message.text != 'Расчитать сумму':
        bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')


bot.polling(non_stop=True)
bot.infinity_polling()
