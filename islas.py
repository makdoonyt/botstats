from telebot import types
from main import bot, separator

def islas(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton( '1', callback_data=separator.join( ['islas', '1'] ) ),
        types.InlineKeyboardButton( '2', callback_data=separator.join( ['islas', '2'] ) ),
        types.InlineKeyboardButton( '3', callback_data=separator.join( ['islas', '3'] ) ),
        types.InlineKeyboardButton( '4', callback_data=separator.join( ['islas', '4'] ) ),
        types.InlineKeyboardButton( '5', callback_data=separator.join( ['islas', '5'] ) )
    )
    keyboard.row(
        types.InlineKeyboardButton( '<<', callback_data=separator.join( ['islas', 'prev'] ) ),
        types.InlineKeyboardButton( '>>', callback_data=separator.join( ['islas', 'next'] ) )
    )
    msg = bot.send_message(message.chat.id,
        'Lista de islas en creativo:   *1/5*\n'
        '*1.* Aim & Build: 0237-9611-6059\n'
        '*2.* Tree Map: 3211-7139-3608\n'
        '*3.* Feisty Favelas: 1115-5430-5035', parse_mode="Markdown")