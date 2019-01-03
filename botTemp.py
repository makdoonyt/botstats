import telebot, urllib, re, time
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
Bienvenido shur! el comando para ver tus estadísticas es "/shurstats""
""")


@bot.message_handler(commands=['shurstats'])
def fntstats(message):
    shur = message.text.split('/shurstats ')
    if(len(shur)==1):
        bot.send_message(message.chat.id,'Necesito un Usuario de Epic. Vuelve a escribir con /shurstats Usuario')
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('PC', callback_data='stats-' + str(message.from_user.id) + '-pc-' + shur[1]),
            types.InlineKeyboardButton('PSN', callback_data='stats-' + str(message.from_user.id) + '-psn-' + shur[1]),
            types.InlineKeyboardButton('XBOX', callback_data='stats-' + str(message.from_user.id) + '-xbox-' + shur[1])
        )
        msg = bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige la plataforma:', reply_markup=keyboard)
        time.sleep(10)
        bot.delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(commands=['ranking'])
def fntstats(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Lifetime', callback_data='rank-' + str(message.from_user.id) + '-lifetime'),
        types.InlineKeyboardButton('Temporada', callback_data='rank-' + str(message.from_user.id) + '-current')
    )
    msg = bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige el periodo:', reply_markup=keyboard)
    time.sleep(15)
        bot.delete_message(msg.chat.id, msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    parsed = re.compile('(stats|rank|rank2)-([0-9]+)-(pc|psn|xbox)-(.*)').findall(data)[0]
    if (parsed[0] == "stats" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        bot.delete_message(query.message.chat.id, query.message.message_id)
        send_stats(query.message,parsed)
    if (parsed[0] == "rank" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        window = parsed[2]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('K/D', callback_data='rank2-' + str(query.from_user.id) + '-' + window + '-kd'),
            types.InlineKeyboardButton('Kills', callback_data='rank2-' + str(query.from_user.id) + '-' + window + '-kills')
        )
        keyboard.row(
            types.InlineKeyboardButton('Winrate', callback_data='rank2-' + str(query.from_user.id) + '-' + window + '-winrate'),
            types.InlineKeyboardButton('Wins', callback_data='rank2-' + str(query.from_user.id) + '-' + window + '-wins')
        )
        keyboard.row(
            types.InlineKeyboardButton('Matches', callback_data='rank2-' + str(query.from_user.id) + '-' + window + '-matches')
        )
        bot.edit_message_text('Ahora elige la categoría:', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
    if(parsed[0] == "rank2" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        send_rank(query.message,parsed)

def send_rank(message, parsed):
    window = parsed[2]
    category = parsed[3]
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

def send_stats(message, parsed):
    plataforma = parsed[2]
    shur = parsed[3]
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
        bot.send_photo(message.chat.id, img)
        img.close()

@bot.message_handler(commands=['fntupdate'])
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
while True: # Don't let the main Thread end.
    pass
