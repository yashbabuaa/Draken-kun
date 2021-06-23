import logging 
import os 
from telethon import TelegramClient, events, Button

bot_token = os.environ.get('BOT_TOKEN')
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

@bot.on(events.NewMessage(incoming=True, pattern=r'^#request(.*)'))
async def request(mikey):
  query = mikey.message.text.split(" ", 1)
  chat = -1001487075546
  try:
    query = query[1]
  except IndexError:
    await mikey.message.reply("Request something bakayaro!")
    return
  keybo = []
  async for message in bot.iter_message(chat):
    title = message.text[:20]
    msg_id = message.id 
    link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
    keybo.append([Button.url(text = title, url = link)])
  if keybo == []:
    req_user = f"[{mikey.from_user.first_name}](tg://user?id={mikey.from_user.id})" 
    message_link = f"https://t.me/c/1364238597/{mikey.message.id}"
    text = f"Request: {query}\nRequested by: {req_user}\nMessage link: [limk]({link})"
    await bot.send_message(-1001226512514, text)
    await mikey.message.reply_text("Roger! Request sent, Now wait like a good citizen.")
    return
  m = await mikey.message.reply("Found Some Results!", buttons = [[Button.url(text = "Check Pm!", url = "http://t.me/botROBOT")]])
  try:
    await bot.send_message(message.from_user.id, text = "Found some matches for you!", buttons = [keybo])
  except UserIsBlockedError:
    await m.edit("I haven't met you yet please start me and request again!", button = [[Button.url(text="Start", url = "https://t.me/botROBOT")]])
  
    
@bot.on(events.NewMessage(incoming=True, pattern=r'^/start|/start@botROBOT')) 
async def start(mikey):
  await mikey.message.reply('Ahh you can request now @SeriesArchiveDiscussion, Im a bot specifically made just to handle request, so go and request if you want something!!!', buttons = [[Button.url(text = "SeriesArchiveDiscussion", url = "https://t.me/SeriesArchiveDiscussion")], [Button.url(text = "Creator", url = "https://t.me/DontKnowWhoRU")]])


print('Starting.......')
print('Im online!!!')