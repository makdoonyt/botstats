import json, telebot, tweepy

with open("tokens.json") as f:
    token = json.load(f)

auth = tweepy.OAuthHandler(token["consumer_key"], token["consumer_secret"])
auth.set_access_token(token["access_token"], token["access_token_secret"])
tweet = tweepy.API(auth)

bot = telebot.TeleBot(token["API_TOKEN"])

rank_updating = False
separator = "ྖ"
CURRENT_SEASON = "7"

#Función para borrar mensajes sin error cuando no exista
def delete_message(chat_id,msg_id):
    try:
        bot.delete_message(chat_id, msg_id)
    except Exception as e:
        return