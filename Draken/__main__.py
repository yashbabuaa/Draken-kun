import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument
from telegram import * 
from telegram.ext import *
from telethon.utils import pack_bot_file_id
import asyncio
print("Starting....")

draken_token = os.environ.get('BOT_TOKEN')
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string = os.environ.get('STRING_SESSION')
bot_name = os.environ.get('BOT_NAME', 'Draken')

draken = Updater(draken_token)
dispatcher = draken.dispatcher
takemichi = TelegramClient(StringSession(string), api_id, api_hash)

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

loop = asyncio.new_event_loop()

async def search(query):
  chat = -1001487075546
  keybo = []
  async for message in takemichi.iter_messages(chat, search=query):
    try:
      text = f"{message.text[2:20]}..."
      msg_id = message.id 
      link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
      keybo.append([InlineKeyboardButton(text=f"{text}", url = link)])
    except TypeError:
      pass
    if len(keybo) >= 2:
      return keybo 
    else:
      return False
    
async def searchfiles(query):
  chat2 = -1001550963689
  doc = []
  async for message in takemichi.iter_messages(chat2, search = query, reverse = True, filter = InputMessagesFilterDocument):
      doc.append(pack_bot_file_id(message.document))
  if len(doc) >= 1:
    return doc
  else:
    return False
    
    
def request(update: Update, context: CallbackContext):
  bot = context.bot
  chat = update.effective_chat 
  user = update.effective_user 
  message = update.effective_message
  if chat.type == "private":
    if message.text.startswith("!search"):
      pass
    else:
      return 
  query = message.text.split(" ", 1)
  try:
    query = query[1]
  except IndexError:
    message.reply_text("Request something bakayaro!")
    return
  if not chat.id == -1001364238597:
    req_log = "False"
  elif message.text.startswith("!search"):
    req_log = "False"
  else:
    req_log = "True"
  if message.reply_to_message:
    mikey = message.reply_to_message
  else:
    mikey = message
  count = 0
  text = ''
  hek = loop.run_until_complete(search(query))
  if hek == False:
    kek = loop.run_until_complete(searchfiles(query))
    if kek == False:
      if req_log == "True":
        req_user = f"[{mikey.from_user.first_name}](tg://user?id={mikey.from_user.id})" 
        message_link = f"https://t.me/c/1364238597/{mikey.message_id}"
        text = f"Request: {query}\nRequested by: {req_user}\n"
        bot.send_message(-1001226512514, text, buttons = [[InlineKeyboardButton(text = "Message", url = message_link)], [InlineKeyboardButton(text="Request Complete", callback_data = "recomp")]])
        mikey.reply("Roger! Request sent, Now wait like a good citizen.")
        return
    else:
      count = 0
      for i in kek:
        bot.send_document(chat.id, document=i)
      if not count == 0:
        mikey.reply_text("👆")
  else:
    mikey.reply_text("Found some from Series Archive.....", reply_markup=InlineKeyboardMarkup(hek))
  
def start(update: Update, context: CallbackContext):
  chat = update.effective_chat
  msg = update.effective_message
  bot = context.bot
  if chat.type == "private":
    msg.reply_text(f"Im {bot_name} a bot made by @DontKnowWhoRU, i was made to handle requsest!")
    bot.send_message(-1001569337079, f"#START\n[{msg.from_user.first_name}](tg://user?id={msg.from_user.id}) started the bot!")
  else:
    msg.reply_text("Im up and working!")

def de(update: Update, context: CallbackContext):
  query = update.callback_query 
  query.message.delete()


START_HANDLER = CommandHandler("start", start, run_async=True)
REQ_HANDLER = MessageHandler(Filters.regex(r'^#request(.*)'), request, run_async=True)
SEARCH_HANDLER = MessageHandler(Filters.regex(r'^!search(.*)'), request, run_async=True)
DEL_CALL = CallbackQueryHandler(de, pattern="recomp", run_async=True)

dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(REQ_HANDLER)
dispatcher.add_handler(SEARCH_HANDLER)
dispatcher.add_handler(DEL_CALL)


print('Im online!!!')

takemichi.start()
draken.start_polling()