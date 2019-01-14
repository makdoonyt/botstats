# -*- coding: utf-8 -*-
import telebot, urllib, re, time, datetime, tweepy, pathlib
from telebot import types
from pathlib import Path

consumer_key = '**********'
consumer_secret = '**********'
access_token = '**********'
access_token_secret = '**********'


API_TOKEN = '**********'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweet = tweepy.API(auth)
bot = telebot.TeleBot(API_TOKEN)

rank_updating = False
separator = "ྖ"
CURRENT_SEASON = "7"

#Función para borrar mensajes sin error cuando no exista
def delete_message(chat_id,msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception as e:
        return

class User:
    def __init__(self, name):
        self.name = name
        self.sex = None

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, 'Bienvenido shur! el comando para ver tus estadísticas es "/shurstats <usuario>"')

@bot.message_handler(regexp="/semana([2-9]|10?)")
def semana(message):
    global CURRENT_SEASON
    regexp = re.compile("semana([2-9]|10?)")
    week = regexp.findall(message.text)[0]
    today = datetime.datetime.today()
    latest = 0

    challenge = Path("challenges/" + CURRENT_SEASON + "/" + week + ".jpg")
    if not Path("challenges/" + CURRENT_SEASON).exists():
        pathlib.Path("challenges/" + CURRENT_SEASON).mkdir(parents=True,exist_ok=False)
    if challenge.is_file():
        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open(challenge, 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
        return
    else:
        for status in tweepy.Cursor(tweet.user_timeline, id="thesquatingdog", tweet_mode="extended").items(1000):
            #Tweets con mas de 80 días descartados
            if abs((status.created_at - today).days) > 80:
                bot.send_message(message.chat.id,"La semana " + week + " aún no está publicada.")
                return
            #Definir última semana publicada
            if "CHEAT SHEET" in status.full_text and latest == 0:
                latest = int(float(re.compile("WEEK ([2-9]|10?)").findall(status.full_text)[0]))
            if latest > 0 and int(float(week)) > latest:
                bot.send_message(message.chat.id,"La semana " + week + " aún no está publicada.")
                return
            if "CHEAT SHEET" in status.full_text and "WEEK " + week in status.full_text and "SEASON " + CURRENT_SEASON in status.full_text:
                if len(status.extended_entities["media"]) > 1:
                    url = status.extended_entities["media"][1]["media_url"]
                else:
                    url = status.extended_entities["media"][0]["media_url"]

                response = urllib.request.urlopen(url)
                bot.send_chat_action(message.chat.id, 'upload_photo')
                f = open('challenges/' + CURRENT_SEASON + '/' + week + '.jpg','wb')
                f.write(response.read())
                f.close()
                img = open('challenges/' + CURRENT_SEASON + '/' + week + '.jpg', 'rb')
                bot.send_photo(message.chat.id, img)
                img.close()
                return
        bot.send_message(message.chat.id,"La semana " + week + " aún no está publicada.")

@bot.message_handler(commands=['shurstats','SHURSTATS','Shurstats','ShurStats','sHURSTATS'])
def fntstats(message):
    global separator
    # El usuario viene tras 11 caracteres: "/shurstats "
    shur = message.text[11:]
    if shur == "":
        bot.send_message(message.chat.id,'Necesito un Usuario de Epic. Vuelve a escribir con /shurstats <usuario>')
        return

    # Botones de estadísticas. Elección de plataforma
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton( 'PC', callback_data=separator.join( ['stats', str(message.from_user.id), 'pc', shur] ) ),
        types.InlineKeyboardButton( 'PSN', callback_data=separator.join( ['stats', str(message.from_user.id), 'psn', shur] ) ),
        types.InlineKeyboardButton( 'XBOX', callback_data=separator.join( ['stats', str(message.from_user.id), 'xbox', shur] ) )
    )
    msg = bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige la plataforma:', reply_markup=keyboard)
    time.sleep(10)
    delete_message(msg.chat.id, msg.message_id)

@bot.message_handler(commands=['ranking','Ranking','RANKING','rANKING'])
def fntstats(message):
    global separator
    if isinstance(message.from_user.username, str) is False:
        bot.send_message(message.chat.id,'Ha ocurrido un error.')
        print(message)
        return
    # Botones de ranking. Elección del periodo
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Lifetime', callback_data=separator.join( ['rank', str(message.from_user.id), 'lifetime'] ) ),
        types.InlineKeyboardButton('Temporada', callback_data=separator.join( ['rank', str(message.from_user.id), 'current'] ) )
    )
    msg = bot.send_message(message.chat.id,'Bien @' + message.from_user.username + ', ahora elige el periodo:', reply_markup=keyboard)
    print("Ranking pedido por " + message.from_user.username)
    time.sleep(15)
    delete_message(msg.chat.id, msg.message_id)

def send_rank(message, window, category):
    url = 'http://mclv.es/fortnite/rank/' + window + '/' + category
    response = urllib.request.urlopen(url)
    if(response.info().get_content_type() == "text/html"):
        bot.send_message(message.chat.id,'Se ha producido un error al buscar el ranking.')
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        f = open('image.jpg','wb')
        f.write(response.read())
        f.close()
        img = open('image.jpg', 'rb')
        delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, img)
        img.close()

def send_stats(message, plataforma, shur):
    url = 'http://mclv.es/fortnite/' + plataforma + '/' + shur
    response = urllib.request.urlopen(url)
    if(response.info().get_content_type() == "text/html"):
        print("Usuario " + shur + " no encontrado.")
        bot.send_message(message.chat.id,'No encuentro el usuario ' + shur + ' en la plataforma ' + plataforma +'. Recuerda que solo funciona con la cuenta de Epic Games.')
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        f = open('image.jpg','wb')
        f.write(response.read())
        f.close()
        img = open('image.jpg', 'rb')
        print("Estadísticas de " + shur +" enviadas.")
        bot.send_photo(message.chat.id, img)
        img.close()

@bot.message_handler(commands=['fntupdate','rankupdate'])
def update_rank(message):
    global rank_updating

    if(rank_updating):
        bot.send_message(message.chat.id,'Ya hay una actualización del ranking en curso. No seas impaciente.')
    else:
        rank_updating = True
        print("Actualizando ranking...")
        msg = bot.send_message(message.chat.id,'Actualizando ranking... Esto puede llevar unos minutos.')
        url = 'http://mclv.es/fortnite/update'
        response = urllib.request.urlopen(url).read()
        delete_message(msg.chat.id, msg.message_id)
        print("Actualización del ranking completada.")
        bot.send_message(message.chat.id,'Ranking actualizado correctamente.')
        rank_updating = False

@bot.message_handler(commands=['rankedit'])
def rank_edit(message):
    global separator
    if(message.chat.id in [-1001427150679,-1001132498727] and bot.get_chat_member(message.chat.id,message.from_user.id).status in ["administrator","creator"]):
        shur = message.text[10:]
        if shur == "":
            bot.send_message(message.chat.id,'Necesito un Usuario de Epic. Vuelve a escribir con /rankedit Usuario')
            return
        if shur == None:
            bot.send_message(message.chat.id,'Ha ocurrido un error.')
            return
        # Botones de estadísticas. Elección de plataforma
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton( 'Añadir', callback_data=separator.join( ['rankedit', str(message.from_user.id), 'add', shur] ) ),
            types.InlineKeyboardButton( 'Eliminar', callback_data=separator.join( ['rankedit', str(message.from_user.id), 'remove', shur] ) )
        )
        msg = bot.send_message(message.chat.id,'¿Qué quieres hacer con ' + shur + '?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global separator

    parsed = query.data.split(separator)
    # [0] Identificación de la petición
    # [1] ID de usuario en Telegram. Para bloquar el botón
    if (parsed[0] == "stats" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        bot.delete_message(query.message.chat.id, query.message.message_id)
        send_stats(query.message, parsed[2], parsed[3])
    if (parsed[0] == "rank" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        window = parsed[2]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton('K/D', callback_data=separator.join( ['rank2', str(query.from_user.id), window, 'kd'] )),
            types.InlineKeyboardButton('Kills', callback_data=separator.join( ['rank2', str(query.from_user.id), window, 'kills'] ))
        )
        keyboard.row(
            types.InlineKeyboardButton('Winrate', callback_data=separator.join( ['rank2', str(query.from_user.id), window, 'winrate'] )),
            types.InlineKeyboardButton('Wins', callback_data=separator.join( ['rank2', str(query.from_user.id), window, 'wins'] ))
        )
        keyboard.row(
            types.InlineKeyboardButton('Matches', callback_data=separator.join( ['rank2', str(query.from_user.id), window, 'matches'] ))
        )
        bot.edit_message_text('Ahora elige la categoría:', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
    if(parsed[0] == "rank2" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        delete_message(query.message.chat.id, query.message.message_id)
        send_rank(query.message, parsed[2], parsed[3])
    if(parsed[0] == "rankedit" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        if(parsed[2] == "add"):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton( 'PC', callback_data=separator.join( ['rankeditadd', str(query.from_user.id), 'pc', parsed[3]] ) ),
                types.InlineKeyboardButton( 'PSN', callback_data=separator.join( ['rankeditadd', str(query.from_user.id), 'psn', parsed[3]] ) ),
                types.InlineKeyboardButton( 'XBOX', callback_data=separator.join( ['rankeditadd', str(query.from_user.id), 'xbox', parsed[3]] ) )
            )
            bot.edit_message_text('Elige la plataforma de ' + parsed[3] + ':', chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
        if(parsed[2] == "remove"):
            url = 'http://mclv.es/fortnite/rankedit/remove/' + parsed[3]
            response = urllib.request.urlopen(url).read()
            delete_message(query.message.chat.id, query.message.message_id)
            bot.send_message(query.message.chat.id, parsed[3] + response.decode("utf-8"))
    if(parsed[0] == "rankeditadd" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        url = 'http://mclv.es/fortnite/rankedit/add/' + parsed[3] + '/' + parsed[2]
        response = urllib.request.urlopen(url).read()
        delete_message(query.message.chat.id, query.message.message_id)
        bot.send_message(query.message.chat.id, parsed[3] + response.decode("utf-8"))

bot.polling(none_stop=True, timeout=60)
