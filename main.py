import telebot
from telebot import types


# API_KEY = '5924672396:AAEsfX7vyFgA3uy7GrugRR5w8_rXfhW54U8'

API_KEY = '5855326170:AAE5CJw2wI1kVe19nhMgB-YsKySaR5M7Qag'

CHAT_ID = -1001818313548

# CHAT_ID = 640348124

# USER_ID = 640348124

USER_ID = 748736705

PASSWORD = '1234'

П1 = 100

PAR_DICT = {}

П2 = 20

bot = telebot.TeleBot(API_KEY)

USER_DICT = {}

RAS_DICT = {}


@bot.message_handler(commands=['editid'])
def edit(message):
    if message.from_user.id == USER_ID:
        send = bot.send_message(message.chat.id, 'Пароль')
        bot.register_next_step_handler(send, edit_2)
    else:
        bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')


def edit_2(message):
    if message.text == PASSWORD:
        send = bot.send_message(message.chat.id, 'Введите новый ID:')
        bot.register_next_step_handler(send, edit_3)
    else:
        bot.send_message(message.chat.id, 'Ошибка!')
        bot.send_message(message.chat.id, 'Для повторной попытки нажмите на /editid!')


def edit_3(message):
    global CHAT_ID
    CHAT_ID = message.text
    bot.send_message(message.chat.id, 'ID сменен успешно!')
    bot.send_message(message.chat.id, 'Для активации бота нажмите на /start')


@bot.message_handler(commands=['editpar'])
def edit_id(message):
    try:
        if message.from_user.id == USER_ID:
            send = bot.send_message(message.chat.id, 'Пароль')
            bot.register_next_step_handler(send, edit_id_2)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, повторите операцию. /edit')


def edit_id_2(message):
    if message.text == PASSWORD:
        send = bot.send_message(message.chat.id, 'Введите 1-й параметр:')
        bot.register_next_step_handler(send, edit_id_3)
    else:
        bot.send_message(message.chat.id, 'Ошибка!')
        bot.send_message(message.chat.id, 'Для повторной попытки нажмите на /editpar!')


def edit_id_3(message):
    PAR_DICT['1par'] = message.text
    send = bot.send_message(message.chat.id, 'Введите 2-й параметр:')
    bot.register_next_step_handler(send, edit_id_4)


def edit_id_4(message):
    PAR_DICT['2par'] = message.text
    global П1, П2
    П1 = PAR_DICT['1par']
    П2 = PAR_DICT['2par']
    bot.send_message(message.chat.id, 'Параметры сменены успешно!')
    bot.send_message(message.chat.id, f'{П1} \n {П2}')
    bot.send_message(message.chat.id, 'Для активации бота нажмите на /start')


@bot.message_handler(commands=['start'])
def start_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    credit = types.KeyboardButton('Расчитать сумму')
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы расчитать сумму нажмите на кнопку "Расчитать сумму"', reply_markup=markup)
    bot.register_next_step_handler(message, start_2)


def start_2(message):
    if message.text != 'Расчитать сумму' and message.text != 'Пересчитать сумму' and message.text != 'Начать расчет заново':
        start_1(message=bot.reply_to(message, 'Пожалуйста, нажмите на кнопку для расчета'))
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        credit = types.KeyboardButton('Назад')
        markup.add(credit)
        send = bot.send_message(message.chat.id, 'Укажите цену товара', reply_markup=markup)
        bot.register_next_step_handler(send, review_1)
    

def review_1(message):
        if message.text == 'Назад':
            start_1(message=message)
        else:
            try:
                int(message.text) // int(message.text) == 1
            except:
                send = bot.reply_to(message, 'Укажите цифрами')
                bot.register_next_step_handler(send, review_1)
            else:
                sum = message.text
                RAS_DICT['sum'] = int(sum)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                credit = types.KeyboardButton('Начать расчет заново')
                markup.add(credit)
                send = bot.send_message(message.chat.id, 'Укажите первоначальный взнос:', reply_markup=markup)
                bot.register_next_step_handler(send, review_2)


def review_2(message):
    if message.text == 'Начать расчет заново':
        start_2(message=message)
    else:
        try:
            int(message.text) // int(message.text) == 1
            per_vznos = message.text
            RAS_DICT['per_vznos'] = int(per_vznos)
            send = bot.send_message(message.chat.id, 'Укажите срок расрочки:')
            bot.register_next_step_handler(send, review_3)
        except:
            send = bot.reply_to(message, 'Укажите цифрами')
            bot.register_next_step_handler(send, review_2)


def review_3(message):
    err = 0
    if message.text == 'Начать расчет заново':
        start_2(message=message)
    else:
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
                        round((A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)) * (C-1) - B
                    except:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
                        raschet = types.KeyboardButton('Пересчитать сумму')
                        markup.add(raschet)
                        send = bot.send_message(message.chat.id, 'Вы неверно ввели данные, пожалуйста, нажмите на кнопку "Пересчитать сумму"', reply_markup=markup)
                        bot.register_next_step_handler(send, func)
                        err = 500
                    else:
                        res_1 = (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)
                        bot.send_message(
                        message.chat.id,
                        f'Сумма товара: {A} руб. \n Срок договора: {C} мес. \n Первоначальный взнос: {B} руб. \n Ежемесячный платеж: {round(res_1)} руб. \n Сумма задолженности: {round(res_1) * (C-1) - B} руб. '
                        )
                else:
                    K1 = 0.04
                    K2 = 0.105
                    try:
                        (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)
                        round((A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)) * (C-1) - B
                    except:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
                        raschet = types.KeyboardButton('Пересчитать сумму')
                        markup.add(raschet)
                        send = bot.send_message(message.chat.id, 'Вы неверно ввели данные, пожалуйста, нажмите на кнопку "Пересчитать сумму"', reply_markup=markup)
                        bot.register_next_step_handler(send, func)
                        err = 500
                    else:
                        res_1 = (A - B) *  C * 18 / (C * 0.01) ** 0.5 / (A - B)**K1 * K2 / П1 / (12 / C) ** (П2 / 100)
                        bot.send_message(
                        message.chat.id,
                        f'Сумма товара: {A} руб. \n Срок договора: {C} мес. \n Первоначальный взнос: {B} руб. \n Ежемесячный платеж: {round(res_1)} руб. \n Сумма задолженности: {round(res_1) * (C-1) - B} руб. '
                        )
                if err != 500:
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
    if message.text == 'Сформировать онлайн заявку' or message.text == 'Заполнить анкету заново':
        review_5(message=message)
    elif message.text == 'Пересчитать сумму':
        start_2(message=message)
    else:
        send = bot.send_message(message.chat.id, 'Пожалуйста нажмите на кнопку')
        bot.register_next_step_handler(send, func)
    

def review_4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    credit = types.KeyboardButton('Сформировать онлайн заявку', one_time_keyboard=True)
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы оформить рассрочку нажмите на кнопку "Сформировать онлайн заявку"', reply_markup=markup)
    bot.register_next_step_handler(message, review_5)


def review_5(message):
    if message.text != 'Сформировать онлайн заявку' and message.text != 'Заполнить анкету заново':
        review_4(message=bot.reply_to(message, 'Пожалуйста, нажмите на кнопку для получения рассрочки'))
    else:
        send = bot.send_message(message.chat.id, 'Внесите ваши Фамилию Имя Отчество полностью, например\n Иванов Иван Иванович"')
        bot.register_next_step_handler(send, review_6)
    

def review_6(message):
    if any(map(str.isdigit, message.text)):
        send = bot.reply_to(message, 'Без цифр')
        bot.register_next_step_handler(send, review_6)
    else:
        USER_DICT['name'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        credit = types.KeyboardButton('Заполнить анкету заново')
        markup.add(credit)
        send = bot.send_message(message.chat.id, 'Укажите дату рождения в формате 01.01.2000:', reply_markup=markup)
        bot.register_next_step_handler(send, review_7)


def review_7(message):
    if message.text == 'Заполнить анкету заново':
        review_5(message=message)
    else:
        USER_DICT['data'] = message.text
        send = bot.send_message(message.chat.id, 'Укажите телефон:')
        bot.register_next_step_handler(send, review_8)


def review_8(message):
    if message.text == 'Заполнить анкету заново':
        review_5(message=message)
    else:
        USER_DICT['tel'] = message.text
        name = USER_DICT['name']
        data = USER_DICT['data']
        tel = USER_DICT['tel']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        credit = types.KeyboardButton('Заполнить анкету заново')
        raschet = types.KeyboardButton('Пересчитать сумму')
        markup.add(credit, raschet)
        send = bot.send_message(message.chat.id, 'Ваша заявка принята, в ближайшее время наш менеджер свяжется с вами.', reply_markup=markup)
        bot.register_next_step_handler(send, func)
        message_to_save = f'{name} \n {data} \n {tel}'
        try:
            bot.send_message(CHAT_ID, message_to_save)
        except:
            bot.send_message(message.chat.id, 'Сервер перезагрузился, пожалуйста, укажите ID чата через /editid')


@bot.message_handler(content_types=['text'])
def not_found(message):
    if message.text != '/editid' and message.text != '/editpar' and message.text != '/start' and message.text != 'Сформировать онлайн заявку' and message.text != 'Пересчитать сумму' and message.text != 'Расчитать сумму':
        bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')


bot.polling(non_stop=True)
bot.infinity_polling()
