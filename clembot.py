#!/usr/bin/env python
# coding: utf-8

get_ipython().system('pip install nltk')
get_ipython().system('pip install python-telegram-bot')
get_ipython().system('pip install python-telegram-bot --upgrade')


#improt database (convert ito JSON)
form database import database
#import utils
import json
import random
import time
import datetime
#import main library "nltk"
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import *

#import other
import sklearn
import requests 
from bs4 import BeautifulSoup

stemmer = PorterStemmer()


# In[4]:


len(database['intents'])


# In[5]:


from nltk import * #моветон так делать, лучше импортировать конкретные нужные функции, или вызывать функции как nltk.func()
def filter_text(text):
    text = text.lower()
    text_sep =  list(text)
    text_sep2 = text_sep.copy()
    text_sep3 = [c for c in text_sep if c in 'abcdefghijklmnopqrstuvwxyz ']
    text_sep4 = nltk.word_tokenize(''.join(text_sep3))
    text_sep5 = []
    for word in text_sep4:
        word = WordNetLemmatizer().lemmatize(word)
        text_sep5.append(word)
    text_sep5 = ' '.join(text_sep5)
        
   
    return text_sep5


# In[6]:


X = []
y = []
for intent, intent_data in database['intents'].items():
     for quest in intent_data['questions']:
            X.append(filter_text(quest))
            y.append(intent)


# In[7]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)


# In[8]:


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression().fit(X, y)


# In[9]:


def get_intent_ML(text):
    textbase = []
    textbase.append(filter_text(text))
    probas = clf.predict_proba(vectorizer.transform(textbase))[0]
    if max(probas) < 0.15:
        return None
    return clf.predict(vectorizer.transform(textbase))[0]


# In[10]:


get_intent_ML('temperature now')


# In[11]:


def timenow():
    #seconds = time.time()
   
    c =  [datetime.datetime.now().hour, datetime.datetime.now().minute]
    c[0],c[1] = str(c[0]),str(c[1])
    if len(c[1]) < 2:
        c[1] = '0'+ c[1]
    return ':'.join(c)


# In[12]:


def weather_parser_now():
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Saint Petersburg&appid=60d1330e994b5e282111c87053634edf&units=metric')
    data = res.json()
    b = str()
    b = 'temperature : ' + str(data['main']['temp']) + '°C' + ', ' + str(data['weather'][0]['description'])
    return b


# In[13]:


def weather_forecast():
    b = str()
    res = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Saint Petersburg&appid=60d1330e994b5e282111c87053634edf&units=metric')
    data = res.json()  
    for i in data['list']:
        b += str(time.ctime(i['dt'])) + ' temperature: ' + str(i['main']['temp']) + '°C' + ', ' + str(i['weather'][0]['description']) + '\n'
    return b


# In[14]:


def functions(intent):
    if intent == 'Time':
        return database['intents']['Time']['responses'][0] + str(timenow())
    elif intent == 'Temperature_now':
        return database['intents']['Temperature_now']['responses'][0] + str(weather_parser_now())
    elif intent == 'Weather':
        return database['intents']['Weather']['responses'][0] + str(weather_forecast())


# In[15]:


def get_answer_by_intent(intent):
    if intent in database['intents']:
        if intent in ['Time', 'Weather','Temperature_now']:
            return functions(intent)
        if intent:
            phrases = database['intents'][intent]['responses']
            return random.choice(phrases)
        else:
            return None


# In[16]:


def botok(question):    
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


# In[ ]:


#импорт в телегу


# In[ ]:


#botok() #почему функция без аргумента, когда она ждет question


# In[18]:


#from telegram import Update, ForceReply
#from telegram.ext import Updater
#from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



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


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1807569036:AAGdNkgNSvDu_JZ3TdvfLkK-Ts0mmkm4jZw")

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


# In[ ]:


main()

