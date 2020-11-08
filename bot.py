from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', '5fd20df0c4db85798dd4f5ff3d03e3606a94f98b')

bot = Client('golink bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm Golinksrt bot. Just send me link and get short link\n\n/help for more details\n\n"
        "**Join my [update channel](https://t.me/Golinksrt)**")
      
      
@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello {message.chat.first_name}!**\n\n"
        "Send me any valid url I will give you the short link\n\n"
        "🙏**Register [Golinksrt](https://golinksrt.xyz/auth/signup)\n\nEARN MONEY**\n\nJoin my [support channel](https://t.me/Golinksrt)")
    
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import re
from golink_tokens import tokens
from os import environ
import aiohttp



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

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
