import telebot
from telebot import types

API_TOKEN = '653272381:AAELYn9Rb1gNdnLOoCoyOmS79PFdFZtNX50'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.sex = None
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Bienvenido shur! los comandos para ver tus estadísticas son los siguientes: "/statspc" "/statspsn" "/statsxbox"
""")


# Handle '/start' and '/help'
@bot.message_handler(commands=['statspc'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hola shur, dime tu nombre en el juego (si tiene espacios, debido a un problema de telegram deberás usar %20 como espacio, EJ: Not%20Tfue)
""")
    bot.register_next_step_handler(msg, process_pc_step)


def process_pc_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, '')
    except Exception as e:
        bot.send_message(chat_id, 'http://mclv.es/fortnite/pc/' + user.name)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['statspsn'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hola shur, dime tu nombre en el juego (si tiene espacios, debido a un problema de telegram deberás usar %20 como espacio, EJ: Not%20Tfue)
""")
    bot.register_next_step_handler(msg, process_psn_step)

def process_psn_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, '')
    except Exception as e:
        bot.send_message(chat_id, 'http://mclv.es/fortnite/psn/' + user.name)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['statsxbox'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hola shur, dime tu nombre en el juego (si tiene espacios, debido a un problema de telegram deberás usar %20 como espacio, EJ: Not%20Tfue)
""")
    bot.register_next_step_handler(msg, process_xbox_step)

def process_xbox_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, '')
    except Exception as e:
        bot.send_message(chat_id, 'http://mclv.es/fortnite/xbox/' + user.name)
    except Exception as e:
        bot.reply_to(message, e)
@bot.message_handler(commands=['update'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Haz clic en este enlace para actualizar el ranking http://mclv.es/fortnite/update
""")
@bot.message_handler(commands=['rankingkd'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
http://mclv.es/fortnite/rank/lifetime/kd
""")




bot.polling()