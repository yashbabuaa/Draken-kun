import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument
from html_telegraph_poster import TelegraphPoster 
from torrentscrape import thirteenX
print("Starting....")

#variables 

draken_token = os.environ.get('BOT_TOKEN')
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string = os.environ.get('STRING_SESSION')
bot_name = os.environ.get('BOT_NAME', 'Draken')


draken = TelegramClient('bot', api_id, api_hash).start(bot_token=draken_token)

takemichi = TelegramClient(StringSession(string), api_id, api_hash)

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

hina = TelegraphPoster(use_api=True)
hina.create_api_token('DontKnow')

#commands

@draken.on(events.NewMessage(incoming=True, pattern=r'^\/files(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^\/search(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^#request(.*)'))
async def request(mikey):
  chat = -1001487075546
  chat2 = -1001550963689
  if mikey.message.text.startswith("#request"):
    if mikey.is_private:
      return 
  query = mikey.message.text.split(" ", 1)
  try:
    query = query[1]
  except IndexError:
    await mikey.reply("Request something bakayaro!")
    return
  if mikey.message.text.startswith("/files"):
    only_files = "On"
  else:
    only_files = "Off"
  if not mikey.chat_id == -1001364238597:
    req_log = "False"
  elif mikey.message.text.startswith("/search"):
    req_log = "Trufal"
  else:
    req_log = "True"
  if mikey.reply_to_msg_id:
    mikey = await mikey.get_reply_message()
  keybo = []
  count = 0
  text = ''
  if only_files == "Off":
    async for message in takemichi.iter_messages(chat, search=query):
      text = f"{message.text[2:30]}..."
      msg_id = message.id 
      link = f"https://t.me/c/{str(chat)[4:]}/{str(msg_id)}" 
      keybo.append([Button.url(text = text, url = link)])
  else:
    pass
  count2 = 0
  if keybo == []:
    async for message in takemichi.iter_messages(chat2, search = query, reverse = True, filter = InputMessagesFilterDocument):
      hek = await draken.get_messages(chat2, ids = message.id)
      await draken.send_message(mikey.chat_id, file = hek.media)
      count2 += 1 
    if not count2 == 0:
      await mikey.reply("👆")
    if count2 == 0:
      if req_log == "True":
        req_user = f"[{mikey.sender.first_name}](tg://user?id={mikey.sender_id})" 
        message_link = f"https://t.me/c/1364238597/{mikey.id}"
        text = f"Request: {query}\nRequested by: {req_user}\n"
        await draken.send_message(-1001550475256, text, buttons = [[Button.url(text = "Message", url = message_link)], [Button.inline(text="Request Complete", data = "recomp")]])
        await mikey.reply("Roger! Request sent, Now wait like a good citizen.")
        return
      elif req_log == "Trufal":
        await mikey.reply("It isnt in db, will add it soon!!")
      else:
        await mikey.reply("Gotcha, now wait like a good citizen...")
  else:
    m = await mikey.reply("Found some results....", buttons = keybo)
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^(/start(.*)|/start@DRAKENROBOT$)')) 
async def start(mikey):
  if mikey.is_private:
    if not mikey.message.text == '/start':
      if len(mikey.message.text.split(' ', 1)) == 2:
        pass 
      else:
        return
      args = mikey.message.text[6:]
      passer = args.replace('_', '/')
      link = f'https://www.1337xx.to/torrent/{passer}'
      info = thirteenX.get_info(link)
      msg_to_send = f'*Name: {info[0]}\nCategory: {info[1]}\nLeechers: {info[2]}\nSeeders: {info[3]}\n\nMagnet:\n*`{info[4]}`'
      mikey.reply(msg_to_send)
      return
    await mikey.message.reply(f"Im {bot_name} a bot, \n\nMade by @DontKnowWhoRU2 and managed by @TvSeriesArchive")
    await draken.send_message(-1001569337079, f"#START\n[{mikey.sender.first_name}](tg://user?id={mikey.sender_id}) started the bot!")
  else:
    await mikey.reply("Im up and working!")

@draken.on(events.CallbackQuery(pattern=b'recomp'))
async def de(mikey):
  await mikey.delete()

#torrent search 
@draken.on(events.NewMessage(pattern=r'^\/torrent'))
async def torrentsearch(mikey):
  query = mikey.message.text 
  search = thirteenX.search(query)
  count = 0
  count2 = 0
  keybo = []
  msg_to_send = ''
  text = ''
  while count <= 4:
    for i in search:
      count += 1
      msg_to_send += f"*{count}.{i[0]}\n  Size: {i[3]}*\n\n"
      r = i[2][30:]
      passer = r.replace('/', '_')
      keybo.append(Button.url(text=count, url=f'https://t.me/DrakenKunRoBot?start={passer}'))
  for i in search: 
    r2 = i[2][30:]
    passer2 = r2.replace('/', '_')
    link = f'https://t.me/DrakenKunRoBot?start={passer2}'
    text = f'{count2}.{i[0]}\nSize: {i[3]}\n<a href = "{link}">Click here to get more info</a>\n\n'
  h = hina.post(title = f'Results for {query}', author = 'Draken', text=text)  
  url = h.get('url')
  if msg_to_send = '':
    await mikey.reply('Sorry, no results found!')
    return 
  markup = [keybo, [Button.url(text='More Results', url = url)]]
  await mikey.reply(msg_to_send, buttons=markup)

print('Im online!!!')

takemichi.start()
draken.start()
draken.run_until_disconnected()
takemichi.run_until_disconnected()