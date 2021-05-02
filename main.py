import constants as keys
from telegram.ext import *
import responses as R
import datetime
import requests
import json
import logging

#-----------
import os

print("Bot Started...")


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)


#--------------
PORT = int(os.environ.get('PORT', '8443'))
#--------------

#####    Time greeting    ######
currentTime = datetime.datetime.now()
currentTime.hour

if currentTime.hour < 12:
    greetings = 'Good morning, '
elif 12 <= currentTime.hour < 18:
    greetings = 'Good afternoon, '
else:
    greetings = 'Good evening, '
################################

def start_command(update,context):
    update.message.reply_text(greetings+update.message.chat.first_name)

def help_command(update,context):
    update.message.reply_text('You asked for help.')


def handle_image(update,context):
    print("In image handling function.")
    file_id = update.message.photo[-1].file_id
    
    link = "https://api.telegram.org/bot" + keys.API_KEY + "/getFile?file_id="+file_id
    #print(link)
    response_API = requests.get(link)
    data = response_API.text
    parse_json = json.loads(data)
    d_link = "https://api.telegram.org/file/bot"+ keys.API_KEY +"/"+parse_json["result"]["file_path"]
    r = requests.get(d_link)
    #print(d_link)
    with open("wind-turbine.jpeg", "wb") as f:
        f.write(r.content)





def handle_message(update,context):
    print(update)
    print("\n")
    text = str(update.message.text).lower()

    if(text=='pic'):
        url = R.send_dog_pic(text)
        context.bot.send_photo(chat_id=update.message.chat_id , photo=url)
    else:
        response = R.sample_responses(text)
        update.message.reply_text(response)


def error(update,context):
    print(f"|||||||||||||||||||||| Update {update} caused error |||||||||||||||||||||||||{context.error}")
    print("\n")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    ##  commands starts with '/'  
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_handler(MessageHandler(Filters.photo,handle_image))
    dp.add_handler(MessageHandler(Filters.document,handle_image))
    #dp.add_handler(MessageHandler(Filters.document.category("image/jpg"),handle_image))
    #dp.add_handler(MessageHandler(Filters.photo, image_handler))

    dp.add_error_handler(error)
    '''
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook(APP_NAME + keys.API_KEY)
    '''


    ##Stopping Polling
    updater.start_polling()
    updater.idle()


main()
