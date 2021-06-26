import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument
print("Starting....")

draken_token = os.environ.get('BOT_TOKEN')
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string = os.environ.get('STRING_SESSION')

draken = TelegramClient('bot', api_id, api_hash).start(bot_token=draken_token)

takemichi = TelegramClient(StringSession(string), api_id, api_hash)

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

@draken.on(events.NewMessage(incoming=True, pattern=r'^#request(.*)'))
async def request(mikey):
  if mikey.is_private:
    return 
  query = mikey.message.text.split(" ", 1)
  chat = -1001487075546
  chat2 = -1001364238597
  try:
    query = query[1]
  except IndexError:
    await mikey.message.reply("Request something bakayaro!")
    return
  keybo = []
  count = 0
  photo = ''
  text = ''
  async for message in takemichi.iter_messages(chat, search=query):
    if count == 1:
      break
    try:
      title = f"{message.text[2:30]}..."
      photo = await draken.download_file(message.photo)
      msg_id = message.id 
      link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
      keybo.append([Button.url(text = title, url = link)])
      count += 1
    except TypeError:
      pass
  count2 = 0
  if keybo == []:
    async for message in takemichi.iter_messages(chat2, search = query, reverse = True, filter = InputMessagesFilterDocument):
      await takemichi.send_message(chat2, file = message.document)
      count2 += 1 
    if not count2 == 0:
      await mikey.reply("👆")
    if count2 == 0:
      req_user = f"[{mikey.sender.first_name}](tg://user?id={mikey.sender_id})" 
      message_link = f"https://t.me/c/1364238597/{mikey.message.id}"
      text = f"Request: {query}\nRequested by: {req_user}\n"
      await draken.send_message(-1001226512514, text, buttons = [[Button.url(text = "Message", url = message_link)], [Button.inline(text="Request Complete", data = "recomp")]])
      await mikey.message.reply("Roger! Request sent, Now wait like a good citizen.")
      return
  else:
    m = await mikey.message.reply(text, file = open(photo, 'rb'), buttons = keybo)
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^/start|/start@DRAKENROBOT')) 
async def start(mikey):
  if mikey.is_private:
    await mikey.message.reply('Ahh you can request now @SeriesArchiveDiscussion, Im draken specifically made just to handle request, so go and request if you want something!!!', buttons = [[Button.url(text = "SeriesArchiveDiscussion", url = "https://t.me/SeriesArchiveDiscussion")], [Button.url(text = "Creator", url = "https://t.me/DontKnowWhoRU")]])
    await draken.send_message(-1001569337079, f"#START\n[{mikey.sender.first_name}](tg://user?id={mikey.sender_id}) started the bot!")
  else:
    await mikey.reply("Im up and working!")

@draken.on(events.CallbackQuery(pattern=b'recomp'))
async def de(mikey):
  await mikey.delete()

print('Im online!!!')

takemichi.start()
draken.start()
draken.run_until_disconnected()
takemichi.run_until_disconnected()