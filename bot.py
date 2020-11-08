# import pyshorteners
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import re
from golink_tokens import tokens
from os import environ
import aiohttp



BOT_TOKEN = environ.get('BOT_TOKEN')
def start(update, context):

    update.message.reply_text(
        f"<b>Hi {update.message.from_user.first_name}!<\b>\n\n"
        "I'm Golinksrt bot. Just send me link and get short link\n\n/help for more details\n\n"
        "<b>Join my  <a href="https://t.me/Golinksrt/"update channel</a><\b>")


def help_command(update, context):

    update.message.reply_text("**Hello {update.message.from_user.first_name}!**\n\n"
        "Send me any valid url I will give you the short link\n\n"
        "🙏**Register [Golinksrt](https://golinksrt.xyz/auth/signup)\n\nEARN MONEY**\n\nJoin my [support channel](https://t.me/Golinksrt)")


def echo(update, context):

    if 'https://golinksrt.xyz/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://golinksrt.xyz/api?api=", "")
        token = re.sub("&.*", "", url)
        tokens[chat] = str(token)
        with open('golink_tokens.py', 'w') as file:
            file.write('tokens = ' + str(tokens))
            update.message.reply_text(f'Your CHAT_ID : {chat} IS REGISTERED WITH GOLINK API TOKEN : {token}\n\nIF YOU SEND ME AGAIN A DIFFRENT API URL IT WIL BE RE ASSIGNE TO YOUR CHAT_ID')
    elif 'https://golinksrt.xyz/api?api=' not in str(update.message.text) and (re.search('^http://.*', str(update.message.text)) or re.search('^https://.*', str(update.message.text))):
        try:
            chat = str(update.message.chat_id)
            gptoken = tokens[chat]
            url_convert = update.message.text
        except:
            update.message.reply_text("TOKEN NOT FOUND USE /help FOR MORE ")

        req = requests.get(f'https://golinksrt.xyz/api?api={gptoken}&url={url_convert}')
        r = json.loads(req.content)

        if r['status'] == 'success':
            update.message.reply_text(' Status : ' + r['status'])
            update.message.reply_text(' shortenedUrl : ' + r['shortenedUrl'])
        if r['status'] == 'error':
            update.message.reply_text(' Error : ' + r['message'])

def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
      
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
  

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
