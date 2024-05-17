#       import utils
# import json
import random
import time
import datetime
import os
#       import other
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import requests
from bs4 import BeautifulSoup
#       import telegram-bot
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
#       import main library "nltk"
import nltk
import ssl
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
#       download other ntlk packages
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

#       import database (convert into JSON)
from data import database



def filter_text(text):
    text_lower = [c for c in text.lower() if c in 'abcdefghijklmnopqrstuvwxyz ']
    tokens = nltk.word_tokenize(text_lower)
    lemmed_text = [WordNetLemmatizer().lemmatize(word) for word in tokens]
    return ' '.join(lemmed_text)


def get_intent_ML(text):
    textbase = []
    textbase.append(filter_text(text))
    probas = clf.predict_proba(vectorizer.transform(textbase))[0]
    if max(probas) < 0.15:
        return None
    return clf.predict(vectorizer.transform(textbase))[0]


def timenow():
    hours = datetime.datetime.now().hour
    minutes = datetime.datetime.now().minute
    zero = ''
    if minutes < 10:
        zero = '0'
    return f"{hours}:{zero}{minutes}"


def weather_parser_now():
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Saint Petersburg&appid=60d1330e994b5e282111c87053634edf&units=metric')
    data = response.json()
    output = 'temperature : ' + str(data['main']['temp']) + '°C' + ', ' + str(data['weather'][0]['description'])
    return output


def weather_forecast():
    output = str()
    res = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Saint Petersburg&appid=60d1330e994b5e282111c87053634edf&units=metric')
    data = res.json()  
    for i in data['list']:
        output += str(time.ctime(i['dt'])) + ' temperature: ' + str(i['main']['temp']) + '°C' + ', ' + str(i['weather'][0]['description']) + '\n'
    return output


def functions(intent):
    if intent == 'Time':
        return database['intents']['Time']['responses'][0] + str(timenow())
    if intent == 'Temperature_now':
        return database['intents']['Temperature_now']['responses'][0] + str(weather_parser_now())
    if intent == 'Weather':
        return database['intents']['Weather']['responses'][0] + str(weather_forecast())


def get_answer_by_intent(intent):
    if intent in database['intents']:
        if intent in ['Time', 'Weather','Temperature_now']:
            return functions(intent)
        if intent:
            phrases = database['intents'][intent]['responses']
            return random.choice(phrases)
        else:
            return None


def botok(question):
    """unused func"""
    answer = str()
    intent = str()
    if question != 'break' and intent != 'goodbye' :
        intent = get_intent_ML(question)
        answer = get_answer_by_intent(intent)
        if answer:
            return answer
        else:
            answer = random.choice(database['failure_phrases'])
            return answer

# импорт в телегу


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(botok(update.message.text))


def telegram_bot_start():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_API_TOKEN"))
    print("the token will be received from ENV TELEGRAM_API_TOKEN")

 # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


stemmer = PorterStemmer()
len(database['intents'])
X = []
y = []
for intent, intent_data in database['intents'].items():
     for quest in intent_data['questions']:
            X.append(filter_text(quest))
            y.append(intent)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)
clf = LogisticRegression().fit(X, y)
get_intent_ML('temperature now')
telegram_bot_start()

