import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument
from telegram import * 
from telegram.ext import *
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

async def request(update: Update, context: CallbackContext):
  chat = -1001487075546
  chat2 = -1001550963689
  bot = context.bot
  chat = upsate.effective_chat 
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
  keybo = []
  count = 0
  text = ''
  async for message in takemichi.iter_messages(chat, search=query):
    try:
      text = f"{message.text[2:20]}..."
      msg_id = message.id 
      link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
      keybo.append([InlineKeyboardButton(text=f"{text}", url = link)])
    except TypeError:
      pass
  count2 = 0
  if keybo == []:
    async for message in takemichi.iter_messages(chat2, search = query, reverse = True, filter = InputMessagesFilterDocument):
      bot.send_document(chat.id, document = message.document)
    if not count2 == 0:
      await mikey.reply_text("👆")
    if count2 == 0:
      if req_log == "True":
        req_user = f"[{mikey.from_user.first_name}](tg://user?id={mikey.from_user.id})" 
        message_link = f"https://t.me/c/1364238597/{mikey.message_id}"
        text = f"Request: {query}\nRequested by: {req_user}\n"
        bot.send_message(-1001226512514, text, buttons = [[InlineKeyboardButton(text = "Message", url = message_link)], [InlineKeyboardButton(text="Request Complete", callback_data = "recomp")]])
        mikey.reply("Roger! Request sent, Now wait like a good citizen.")
        return
      else:
        mikey.reply("Gotcha, Now wait like a good citizen!!")
  else:
    m = mikey.reply(text, reply_markup = InlineKeyboardMarkup([keybo]))
  
def start(update: Update, context: CallbackContext):
  chat = update.effective_chat
  msg = update.effective_message
  bot = context.bot
  if chat.type == "private":
    msg.reply_text(f"Im {bot_name} a bot made by @DontKnowWhoRU, i was made to handle requsest!")
    bot.send_message(-1001569337079, f"#START\n[{message.from_user.first_name}](tg://user?id={message.from_user.message_id}) started the bot!")
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
takemichi.run_until_disconnected()