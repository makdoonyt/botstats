import telebot
import urllib
from telebot import types

API_TOKEN = '785391201:AAFl25TBU_9CbtCQHiXgT2ZdkPoIkP5yVRI'

bot = telebot.TeleBot(API_TOKEN)

rank_updating = False

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.sex = None
# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Bienvenido shur! los comandos para ver tus estadísticas son los siguientes: "/shurstats <nombre>" "/ranking" "/rankupdate"
""")


@bot.message_handler(commands=['shurstats'])
def fntstats(message):
    shur = message.text.split('/shurstats ')
    if(len(shur)==1):
        bot.send_message(message.chat.id,'Necesito un Usuario de Epic. Vuelve a escribir con /shurstats <usuario>')
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('PC', callback_data='shurstats-PC-' + shur[1]),
            types.InlineKeyboardButton('PSN', callback_data='shurstats-PSN-' + shur[1]),
            types.InlineKeyboardButton('XBOX', callback_data='shurstats-XBOX-' + shur[1])
        )
        bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige la plataforma:', reply_markup=keyboard)

@bot.message_handler(commands=['ranking'])
def fntstats(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Lifetime', callback_data='rank-lifetime'),
        types.InlineKeyboardButton('Temporada', callback_data='rank-current')
    )
    bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige la plataforma:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('shurstats-'):
        bot.answer_callback_query(query.id)
        send_stats(query.message,data[4:])
    if data.startswith('rank-'):
        bot.answer_callback_query(query.id)
        window = data[4:].split('-')[1]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('K/D', callback_data='rank2-' + window + '-kd'),
            types.InlineKeyboardButton('Kills', callback_data='rank2-' + window + '-kills')
        )
        keyboard.row(
            types.InlineKeyboardButton('Winrate', callback_data='rank2-' + window + '-winrate'),
            types.InlineKeyboardButton('Wins', callback_data='rank2-' + window + '-wins')
        )
        keyboard.row(
            types.InlineKeyboardButton('Matches', callback_data='rank2-' + window + '-matches')
        )
        bot.edit_message_text('Ahora elige la categoría:', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
    if(data.startswith('rank2-')):
        bot.answer_callback_query(query.id)
        send_rank(query.message,data[4:])

def send_rank(message, callback):
    window = callback.split('-')[1]
    category = callback.split('-')[2]
    url = 'http://mclv.es/fortnite/rank/' + window + '/' + category
    response = urllib.request.urlopen(url)
    if(response.info().get_content_type() == "text/html"):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,'Se ha producido un error al buscar el ranking.')
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        f = open('image.jpg','wb')
        f.write(response.read())
        f.close()
        img = open('image.jpg', 'rb')
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, img)
        img.close()

def send_stats(message, callback):
    plataforma = callback.split('-')[1]
    shur = callback.split('-')[2]
    url = 'http://mclv.es/fortnite/' + plataforma + '/' + shur
    response = urllib.request.urlopen(url)
    if(response.info().get_content_type() == "text/html"):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id,'No encuentro el usuario ' + shur + ' en la plataforma ' + plataforma +'. Recuerda que solo funciona con la cuenta de Epic Games.')
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        f = open('image.jpg','wb')
        f.write(response.read())
        f.close()
        img = open('image.jpg', 'rb')
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, img)
        img.close()

@bot.message_handler(commands=['rankupdate'])
def send_welcome(message):
    global rank_updating

    if(rank_updating):
        bot.send_message(message.chat.id,'Ya hay una actualización del ranking en curso. No seas impaciente.')
    else:
        rank_updating = True
        bot.send_message(message.chat.id,'Actualizando ranking... Esto puede llevar unos minutos.')
        url = 'http://mclv.es/fortnite/update'
        response = urllib.request.urlopen(url).read()
        bot.send_message(message.chat.id,'Ranking actualizado correctamente.')
        rank_updating = False

bot.polling()
