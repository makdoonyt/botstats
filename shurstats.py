import time, urllib
from urllib.parse import quote
from telebot import types
from main import bot, separator, delete_message

def stats(message):
    global separator

    username = message.from_user.first_name
    userid = message.from_user.id
    if isinstance(username, str) is False:
        bot.send_message(message.chat.id,"Ha ocurrido un error.")
        print(message)
        return
    # El usuario viene tras 11 caracteres: "/shurstats "
    shur = message.text[11:]
    if shur == "":
        bot.send_message(message.chat.id,"Necesito un Usuario de Epic. Vuelve a escribir con /shurstats <usuario>")
        return

    # Botones de estadísticas. Elección de plataforma
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton( "PC", callback_data=separator.join( ["stats", str(message.from_user.id), "pc", shur] ) ),
        types.InlineKeyboardButton( "PSN", callback_data=separator.join( ["stats", str(message.from_user.id), "psn", shur] ) ),
        types.InlineKeyboardButton( "XBOX", callback_data=separator.join( ["stats", str(message.from_user.id), "xbox", shur] ) )
    )
    msg = bot.send_message(message.chat.id,f"Bien <a href='tg://user?id={userid}'>{username}</a>, ahora elige la plataforma:", reply_markup=keyboard, parse_mode="HTML")
    time.sleep(10)
    delete_message(msg.chat.id, msg.message_id)

def send_stats(message, plataforma, shur):
    url = quote(f"http://mclv.es/fortnite/{plataforma}/{shur}",safe=':/?&qwertyuiopasdfghjklzxcvbnm')
    print(url)
    response = urllib.request.urlopen(url)
    if response.info().get_content_type() == "text/html":
        print(f"Usuario {shur} no encontrado.")
        bot.send_message(message.chat.id,f"No encuentro el usuario {shur} en la plataforma {plataforma}. Recuerda que solo funciona con la cuenta de Epic Games.")
    else:
        bot.send_chat_action(message.chat.id, "upload_photo")
        bot.send_photo(message.chat.id, response.read())
        print(f"Estadísticas de {shur} enviadas.")
