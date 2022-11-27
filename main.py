import telebot
from telebot import types


API_KEY = '5924672396:AAEsfX7vyFgA3uy7GrugRR5w8_rXfhW54U8'

CHAT_ID = -1001818313548

USER_ID = 748736705

PASSWORD = '1234'

bot = telebot.TeleBot(API_KEY)

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.birthday = None
        self.tel = None



@bot.message_handler(commands=['edit'])
def edit(message):
    try:
        if message.from_user.id == USER_ID:
            sent = bot.reply_to(message, 'Пароль:')
            bot.register_next_step_handler(sent, edit_2)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, пожалуйста, повторите операцию. /edit')


def edit_2(message):
    try:
        if message.text == PASSWORD:
            sent = bot.reply_to(message, 'Введите новый ID:')
            bot.register_next_step_handler(sent, edit_3)
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
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        credit = types.KeyboardButton('Сформировать онлайн заявку')
        markup.add(credit)
        bot.send_message(message.chat.id, 'Для того, чтобы оформить рассрочку нажмите на кнопку "Сформировать онлайн заявку"', reply_markup=markup)
        bot.register_next_step_handler(message, start_2)
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже!')

def start_2(message):
    try:
        sent = bot.reply_to(message, 'Внесите ваше ФИО:')
        bot.register_next_step_handler(sent, review_1)
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже')

def review_1(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        sent = bot.reply_to(message, 'Укажите дату рождения в формате 01.01.2000:')
        bot.register_next_step_handler(sent, review_2)
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже')

def review_2(message):
    try:
        chat_id = message.chat.id
        birthday = message.text
        user = user_dict[chat_id]
        user.birthday = birthday
        sent = bot.reply_to(message, 'Укажите телефон:')
        bot.register_next_step_handler(sent, review_3)
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже')

def review_3(message):
    try:
        chat_id = message.chat.id
        tel = message.text
        user = user_dict[chat_id]
        user.tel = tel
        bot.send_message(message.chat.id, 'Ваша заявка принята, в ближайшее время наш менеджер свяжется с вами.')
        message_to_save = f'{user.name} \n {user.birthday} \n {user.tel}'
        try:
            bot.send_message(CHAT_ID, message_to_save)
        except:
            print('ID не найден. Измените его через Телеграм Бота')
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже')


@bot.message_handler(content_types=['text'])
def not_found(message):
    try:
        if message.text != '/edit' and message.text != '/start' and message.text != 'Сформировать онлайн заявку':
            bot.send_message(message.chat.id, 'Нет такой команды. Введите /start')
        else:
            print(123)
    except:
        bot.send_message(message.chat.id, 'Сервер временно недоступен, пожалуйста, повторите попытку позже')


bot.polling(non_stop=True)
bot.infinity_polling()
