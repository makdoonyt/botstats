# -*- coding: utf-8 -*-
import urllib, time, logging
from telebot import types
from datetime import datetime, date
from urllib.parse import quote

from main import bot, separator, delete_message
from islas import islas
from semana import semana
from shurstats import stats, send_stats
from ranking import rank, rankUpdate, rankEdit, send_rank

logging.basicConfig(filename='logs.log',level=logging.ERROR)

class User:
    def __init__(self, name):
        self.name = name
        self.sex = None

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Bienvenido shur! el comando para ver tus estadísticas es \"/shurstats <usuario>\"")

@bot.message_handler(commands=["evento"])
def evento(message):
    now = datetime.utcnow()
    if now.day == 19 and now.hour >= 20 and now.minute > 0:
        bot.send_message(message.chat.id, "El evento era hoy a las 20:00 hora peninsular. Pide perdón por el retraso.")
    if now.day != 19:
        bot.send_message(message.chat.id, "El evento fue el sábado 19 a las 20:00 hora peninsular. Pide perdón por el retraso.")
    if now.day <= 19 and now.hour < 20:
        bot.send_message(message.chat.id, "El evento será hoy a las 20:00 hora peninsular. Los modos Solo, Dúo y Squad serán sustituídos por unos especiales del evento.")

@bot.message_handler(commands=['islas'])
def imported_islas(message):
    islas(message)

@bot.message_handler(regexp="/semana([2-9]|10?)")
def imported_semana(message):
    semana(message)

@bot.message_handler(commands=["shurstats","SHURSTATS","Shurstats","ShurStats","sHURSTATS"])
def imported_stats(message):
    stats(message)

@bot.message_handler(commands=["ranking","Ranking","RANKING","rANKING"])
def imported_ranking(message):
    rank(message)

@bot.message_handler(commands=["fntupdate","rankupdate"])
def imported_rankUpdate(message):
    rankUpdate(message)

@bot.message_handler(commands=["rankedit"])
def imported_rankEdit(message):
    rankEdit(message)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global separator

    parsed = query.data.split(separator)
    # [0] Identificación de la petición
    # [1] ID de usuario en Telegram. Para bloquar el botón
    if (parsed[0] == "stats" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        bot.delete_message(query.message.chat.id, query.message.message_id)
        try:
            send_stats(query.message, parsed[2], parsed[3])
        except:
            print("DEP")
    if (parsed[0] == "rank" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        window = parsed[2]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton("K/D", callback_data=separator.join( ["rank2", str(query.from_user.id), window, "kd"] )),
            types.InlineKeyboardButton("Kills", callback_data=separator.join( ["rank2", str(query.from_user.id), window, "kills"] ))
        )
        keyboard.row(
            types.InlineKeyboardButton("Winrate", callback_data=separator.join( ["rank2", str(query.from_user.id), window, "winrate"] )),
            types.InlineKeyboardButton("Wins", callback_data=separator.join( ["rank2", str(query.from_user.id), window, "wins"] ))
        )
        keyboard.row(
            types.InlineKeyboardButton("Matches", callback_data=separator.join( ["rank2", str(query.from_user.id), window, "matches"] ))
        )
        bot.edit_message_text("Ahora elige la categoría:", chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
    if(parsed[0] == "rank2" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        delete_message(query.message.chat.id, query.message.message_id)
        send_rank(query.message, parsed[2], parsed[3])
    if(parsed[0] == "rankedit" and int(parsed[1]) == query.from_user.id):
        bot.answer_callback_query(query.id)
        if(parsed[2] == "add"):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton( "PC", callback_data=separator.join( ["rankeditadd", str(query.from_user.id), "pc", parsed[3]] ) ),
                types.InlineKeyboardButton( "PSN", callback_data=separator.join( ["rankeditadd", str(query.from_user.id), "psn", parsed[3]] ) ),
                types.InlineKeyboardButton( "XBOX", callback_data=separator.join( ["rankeditadd", str(query.from_user.id), "xbox", parsed[3]] ) )
            )
            bot.edit_message_text(f"Elige la plataforma de {parsed[3]}:", chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard)
        if(parsed[2] == "remove"):
            epicname = parsed[3].replace(' ','%20')
            url = quote(f"http://mclv.es/fortnite/rankedit/remove/{epicname}",safe=':/?&')
            response = urllib.request.urlopen(url).read()
            delete_message(query.message.chat.id, query.message.message_id)
            bot.send_message(query.message.chat.id, response.decode("utf-8"))
    if(parsed[0] == "rankeditadd" and int(parsed[1]) == query.from_user.id):
        #0: rankedit // 1: userid // 2: Plataforma // 3: Usuario Epic
        epicname = parsed[3].replace(' ','%20')
        bot.answer_callback_query(query.id)
        url = quote(f"http://mclv.es/fortnite/rankedit/add/{epicname}/{parsed[2]}",safe=':/?&')
        response = urllib.request.urlopen(url).read()
        delete_message(query.message.chat.id, query.message.message_id)
        bot.send_message(query.message.chat.id, response.decode("utf-8"))

bot.polling(none_stop=True, timeout=60)
