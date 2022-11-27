import telebot
from telebot import types


API_KEY = '5924672396:AAEsfX7vyFgA3uy7GrugRR5w8_rXfhW54U8'

USER_ID = -1001818313548

bot = telebot.TeleBot(API_KEY)

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.birthday = None
        self.tel = None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    credit = types.KeyboardButton('Сформировать онлайн заявку')
    markup.add(credit)
    bot.send_message(message.chat.id, 'Для того, чтобы оформить рассрочку нажмите на кнопку "Сформировать онлайн заявку"', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):
    sent = bot.reply_to(message, 'Внесите ваше ФИО:')
    bot.register_next_step_handler(sent, riview_1)

def riview_1(message):
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    sent = bot.reply_to(message, 'Укажите дату рождения в формате 01.01.2000:')
    bot.register_next_step_handler(sent, riview_2)
        
def riview_2(message):
    chat_id = message.chat.id
    birthday = message.text
    user = user_dict[chat_id]
    user.birthday = birthday
    sent = bot.reply_to(message, 'Укажите телефон:')
    bot.register_next_step_handler(sent, riview_3)

def riview_3(message):
    chat_id = message.chat.id
    tel = message.text
    user = user_dict[chat_id]
    user.tel = tel
    bot.send_message(message.chat.id, 'Ваша заявка принята, в ближайшее время наш менеджер свяжется с вами.')
    message_to_save = f'{user.name} \n {user.birthday} \n {user.tel}'
    bot.send_message(USER_ID, message_to_save)

bot.polling(non_stop=True)
bot.infinity_polling()
