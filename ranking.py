import time, urllib
from telebot import types
from main import bot, separator, delete_message, rank_updating

def rank(message):
    global separator
    username = message.from_user.first_name
    userid = message.from_user.id
    if isinstance(username, str) is False:
        bot.send_message(message.chat.id,"Ha ocurrido un error.")
        print(message)
        return
    # Botones de ranking. Elección del periodo
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("Lifetime", callback_data=separator.join( ["rank", str(message.from_user.id), "lifetime"] ) ),
        types.InlineKeyboardButton("Temporada", callback_data=separator.join( ["rank", str(message.from_user.id), "current"] ) )
    )
    msg = bot.send_message(message.chat.id,f"Bien <a href='tg://user?id={userid}'>{username}</a>, ahora elige el periodo:", reply_markup=keyboard, parse_mode="HTML")
    print(f"Ranking pedido por {username}")
    time.sleep(15)
    delete_message(msg.chat.id, msg.message_id)

def rankUpdate(message):
    global rank_updating
    if(rank_updating):
        bot.send_message(message.chat.id,"Ya hay una actualización del ranking en curso. No seas impaciente.")
    else:
        rank_updating = True
        print("Actualizando ranking...")
        msg = bot.send_message(message.chat.id,"Actualizando ranking... Esto puede llevar unos minutos.")
        url = "http://mclv.es/fortnite/update"
        response = urllib.request.urlopen(url).read()
        delete_message(msg.chat.id, msg.message_id)
        print("Actualización del ranking completada.")
        bot.send_message(message.chat.id,"Ranking actualizado correctamente.")
        rank_updating = False

def rankEdit(message):
    global separator
    if(message.chat.id in [-1001427150679,-1001132498727] and bot.get_chat_member(message.chat.id,message.from_user.id).status in ["administrator","creator"]):
        shur = message.text[10:]
        if shur == "":
            bot.send_message(message.chat.id,"Necesito un Usuario de Epic. Vuelve a escribir con /rankedit Usuario")
            return
        if shur == None:
            bot.send_message(message.chat.id,"Ha ocurrido un error.")
            return
        # Botones de estadísticas. Elección de plataforma
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton( "Añadir", callback_data=separator.join( ["rankedit", str(message.from_user.id), "add", shur] ) ),
            types.InlineKeyboardButton( "Eliminar", callback_data=separator.join( ["rankedit", str(message.from_user.id), "remove", shur] ) )
        )
        msg = bot.send_message(message.chat.id,f"¿Qué quieres hacer con {shur}?", reply_markup=keyboard)

def send_rank(message, window, category):
    url = f"http://mclv.es/fortnite/rank/{window}/{category}"
    response = urllib.request.urlopen(url)
    if(response.info().get_content_type() == "text/html"):
        bot.send_message(message.chat.id,"Se ha producido un error al buscar el ranking.")
    else:
        bot.send_chat_action(message.chat.id, "upload_photo")
        f = open("img/sendrank.jpg","wb")
        f.write(response.read())
        f.close()
        img = open("img/sendrank.jpg", "rb")
        delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, img)
        img.close()