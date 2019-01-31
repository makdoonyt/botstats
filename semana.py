import re, pathlib, tweepy, urllib, datetime, cv2
from skimage.measure import compare_ssim
from skimage import io

from main import bot, tweet, CURRENT_SEASON

def isChallenge(image):
    test = cv2.resize(cv2.imread("challenges/test.jpg"), (1200, 1200))
    img = cv2.resize(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), (1200, 1200))

    grayTest = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayTest, grayImage, full=True)
    if score > 0.3:
        return True
    else:
        return False

def is_slice_in_list(s,l):
    len_s = len(s) #so we don't recompute length of s on every iteration
    return any(s == l[i:len_s+i] for i in xrange(len(l) - len_s+1))

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
            if re.compile('cheat ?sheet', re.IGNORECASE).match(status.full_text) != None and re.compile(f'season {CURRENT_SEASON}', re.IGNORECASE).match(status.full_text) != None and latest == 0:
                latest = int(float(re.compile("WEEK ([2-9]|10?)", re.IGNORECASE).findall(status.full_text)[0]))
            if latest > 0 and int(float(week)) > latest:
                bot.send_message(message.chat.id,f"La semana {week} aún no está publicada.")
                return

            if re.compile('cheat ?sheet', re.IGNORECASE).match(status.full_text) != None and re.compile(f'week {week}', re.IGNORECASE).match(status.full_text) != None and f"SEASON {CURRENT_SEASON}" in status.full_text:
                if len(status.extended_entities["media"]) > 1:
                    url = status.extended_entities["media"][1]["media_url"]
                    image = io.imread(url)
                    if not isChallenge(image):
                        url = status.extended_entities["media"][0]["media_url"]
                        image = io.imread(url)
                else:
                    url = status.extended_entities["media"][0]["media_url"]
                    image = io.imread(url)

                bot.send_chat_action(message.chat.id, "upload_photo")
                cv2.imwrite(challenge,cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                f = open(challenge,"rb")
                bot.send_photo(message.chat.id, f)
                f.close()
                return
        bot.send_message(message.chat.id,f"La semana {week} aún no está publicada.")