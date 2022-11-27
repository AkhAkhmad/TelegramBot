import telebot
from telebot import types


API_KEY = '5924672396:AAEsfX7vyFgA3uy7GrugRR5w8_rXfhW54U8'

USER_ID = -1001818313548

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
    sent = bot.reply_to(message, 'Пароль:')
    bot.register_next_step_handler(sent, edit_2)


def edit_2(message):
    if message.text == PASSWORD:
        sent = bot.reply_to(message, 'Введите новый ID:')
        bot.register_next_step_handler(sent, edit_3)
    else:
        bot.send_message(message.chat.id, 'Ошибка!')
        bot.send_message(message.chat.id, 'Для повторной попытки нажмите на /edit!')

def edit_3(message):
    global USER_ID
    USER_ID = message.text
    bot.send_message(message.chat.id, 'ID сменен успешно!')
    bot.send_message(message.chat.id, 'Для активации бота нажмите на /start')


@bot.message_handler(commands=['start'])
def start_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    credit = types.KeyboardButton('Сформировать онлайн заявку')
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы оформить рассрочку нажмите на кнопку "Сформировать онлайн заявку"', reply_markup=markup)
    bot.register_next_step_handler(message, start_2)

def start_2(message):
    sent = bot.reply_to(message, 'Внесите ваше ФИО:')
    bot.register_next_step_handler(sent, review_1)

def review_1(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    sent = bot.reply_to(message, 'Укажите дату рождения в формате 01.01.2000:')
    bot.register_next_step_handler(sent, review_2)
        
def review_2(message):
    chat_id = message.chat.id
    birthday = message.text
    user = user_dict[chat_id]
    user.birthday = birthday
    sent = bot.reply_to(message, 'Укажите телефон:')
    bot.register_next_step_handler(sent, review_3)

def review_3(message):
    chat_id = message.chat.id
    tel = message.text
    user = user_dict[chat_id]
    user.tel = tel
    bot.send_message(message.chat.id, 'Ваша заявка принята, в ближайшее время наш менеджер свяжется с вами.')
    message_to_save = f'{user.name} \n {user.birthday} \n {user.tel}'
    bot.send_message(USER_ID, message_to_save)

bot.polling(non_stop=True)
bot.infinity_polling()
