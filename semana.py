import re, pathlib, tweepy, urllib, datetime, pytesseract
from PIL import Image

from main import bot, tweet, CURRENT_SEASON

def semana(message):
    global CURRENT_SEASON
    regexp = re.compile("semana([2-9]|10?)")
    week = regexp.findall(message.text)[0]
    today = datetime.datetime.today()
    latest = 0

    challenge = f"challenges/{CURRENT_SEASON}/{week}.jpg"
    if not pathlib.Path(f"challenges/{CURRENT_SEASON}").exists():
        pathlib.Path(f"challenges/{CURRENT_SEASON}").mkdir(parents=True,exist_ok=False)
    if pathlib.Path(challenge).is_file():
        bot.send_chat_action(message.chat.id, "upload_photo")
        img = open(challenge, "rb")
        bot.send_photo(message.chat.id, img)
        img.close()
        return
    else:
        for status in tweepy.Cursor(tweet.user_timeline, id="thesquatingdog", tweet_mode="extended").items(1000):
            #Tweets con mas de 80 días descartados
            if abs((status.created_at - today).days) > 80:
                bot.send_message(message.chat.id,f"La semana {week} aún no está publicada.")
                return
            #Definir última semana publicada
            if "CHEAT SHEET" in status.full_text and latest == 0:
                latest = int(float(re.compile("WEEK ([2-9]|10?)").findall(status.full_text)[0]))
            if latest > 0 and int(float(week)) > latest:
                bot.send_message(message.chat.id,f"La semana {week} aún no está publicada.")
                return
            if "CHEAT SHEET" in status.full_text and f"WEEK {week}" in status.full_text and f"SEASON {CURRENT_SEASON}" in status.full_text:
                if len(status.extended_entities["media"]) > 1:
                    url = status.extended_entities["media"][1]["media_url"]
                    next = 0
                else:
                    url = status.extended_entities["media"][0]["media_url"]
                    next = 1

                response = urllib.request.urlopen(url)
                bot.send_chat_action(message.chat.id, "upload_photo")
                f = open(challenge,"wb")
                f.write(response.read())
                f.close()

                ocr = pytesseract.image_to_string(Image.open(challenge))
                if len(ocr) < 100:
                    url = status.extended_entities["media"][next]["media_url"]
                    response = urllib.request.urlopen(url)
                f = open(challenge,"wb")
                f.write(response.read())
                f.close()

                img = open(challenge, "rb")
                bot.send_photo(message.chat.id, img)
                img.close()
                return
        bot.send_message(message.chat.id,f"La semana {week} aún no está publicada.")