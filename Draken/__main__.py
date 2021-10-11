import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo
from telethon.tl.types import ChannelParticipantsAdmins
from html_telegraph_poster import TelegraphPoster 
from torrentscrape import thirteenX
import asyncio 
import movie
import mimetypes
import requests
import re

print("Starting....")

#variables 

draken_token = os.environ.get('BOT_TOKEN')
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string = os.environ.get('STRING_SESSION')
bot_name = os.environ.get('BOT_NAME', 'Draken')

loop = asyncio.get_event_loop()

draken = TelegramClient('bot', api_id, api_hash).start(bot_token=draken_token)

takemichi = TelegramClient(StringSession(string), api_id, api_hash)

REQ_CHAT = -1001495696882

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")
mylog = logging.getLogger('Draken')

hina = TelegraphPoster(use_api=True)
hina.create_api_token('DontKnow')

#commands
admins = []

def hrs(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

async def get_all_admins(chat_id):
  async for admin in draken.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)

async def user_admin(the_fuc):
  async def check_admin(mikey):
    if slime.sender_id in admins:
      return await the_fuc(mikey)
    else:
      pass

@user_admin
@draken.on(events.NewMessage(incoming=True,pattern=r'^\/admincache'))
async def admincache(mikey):
  await get_all_admins(mikey.chat_id)
  await mikey.reply('Done!')
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^\/files(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^\/search(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^#request(.*)'))
async def request(mikey):
  global REQ_CHAT
  if mikey.is_private:
    return
  chat = -1001487075546
  chat2 = -1001550963689
  adc = -1001392274404
  query = mikey.message.text.split(" ", 1)
  if mikey.message.text.startswith("/files"):
    if not mikey.sender_id in admins:
      try:
        await slime.delete()
      except Exception:
        print(Exception)
        pass
    only_files = "On"
    req_log='False'
  else:
    only_files = "Off"
  if not mikey.chat_id == REQ_CHAT:
    req_log = "False"
  elif mikey.message.text.startswith("/search"):
    if not mikey.sender_id in admins:
      return  
    req_log='False'
  else:
    req_log='True'
  try:
    query = query[1]
  except IndexError:
    await mikey.reply("Request something bakayaro!")
    return
  if mikey.reply_to_msg_id:
    mikey = await mikey.get_reply_message()
  keybo = []
  count = 0
  text = ''
  if only_files == "Off":
    async for message in takemichi.iter_messages(adc, search=query):
      text = message.raw_text.split('•')[0]
      ignore = list(range(196, 254))
      msg_id = message.id 
      if msg_id in ignore:
        pass
      else:
        link = f"https://t.me/c/{str(adc)[4:]}/{str(msg_id)}" 
        keybo.append([Button.url(text = f'{text[:30]}...',url= link)])
  else:
    pass
  if keybo == []:
    sources = [-1001550963689]
    count2 = 0
    for chat in sources:
      async for message in takemichi.iter_messages(chat, search = query, reverse = True):
        hek = await draken.get_messages(chat2, ids=message.id)
        if message.media and (message.video or message.document):
          await draken.send_file(mikey.chat_id, file=hek.media)
          count2 += 1 
      if not count2 == 0:
        await mikey.reply('☝')
        return
    if count2 == 0:
      if req_log == False:
        await mikey.reply('Not found')
        return
  else:
      m = await mikey.reply("Found some results....", buttons = keybo)
      return
  if req_log == "True":
    h = [int(s) for s in re.findall(r'-?\d+\.?\d*', query)]
    cnt = 0
    for i in h:
      if len(str(i)) == 4:
        cnt += 1
    if h == [] or cnt == 0:
      m = await mikey.reply('You didn\'t mention **year!**, Please check [this](https://t.me/c/1183336084/84418) and request!')
      return
      #await asyncio.sleep(10)
      #await mikey.delete()
      #await m.delete()
    req_user = f"[{mikey.sender.first_name}](tg://user?id={mikey.sender_id})" 
    message_link = f"https://t.me/c/{str(REQ_CHAT)[4:]}/{mikey.id}"
    text = f"Request: {query}\nRequested by: {req_user}\n"
    await draken.send_message(-1001550475256, text, buttons = [[Button.url(text = "Message", url = message_link)], [Button.inline(text="Request Complete", data = "recomp")]])
    await mikey.reply("Roger! Request taken, Now wait like a good meme!")
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^/start(.*)|/start@DrakenKunRoBot$')) 
async def start(mikey):
  if mikey.is_private:
    if not mikey.message.text == '/start':
      if len(mikey.message.text.split(' ', 1)) > 2:
        return
      args = mikey.message.text[6:]
      info = thirteenX.get_info(args)
      msg_to_send = f'**Name: {info[0]}\nCategory: {info[1]}\nLeechers: {info[2]}\nSeeders: {info[3]}\nSize: {info[5]}\n\nMagnet:\n**`{info[4]}`'
      await mikey.reply(msg_to_send, parse_mode='md')
      return
    await mikey.message.reply(f"Im {bot_name} a bot, \n\nMade by @HeyDoUKnowMe and managed by @TvSeriesArchive")
    await draken.send_message(-1001161807206, f"#START\n[{mikey.sender.first_name}](tg://user?id={mikey.sender_id}) started the bot!")
  else:
    await mikey.reply("Im up and working!")


@draken.on(events.InlineQuery)
async def post_comp(mikey):
  if mikey.text == '':
      await mikey.answer([], switch_pm='Search in @TvSeriesArchive', switch_pm_param='start')
  the_text = mikey.text 
  keybo = []
  async for message in takemichi.iter_messages(-1001487075546, search=the_text):
      if len(keybo) > 30:
        await mikey.answer([], switch_pm='Try to be a little specific...', switch_pm_param='start')
        return
      msg_id = message.id 
      link = f"https://t.me/c/1487075546/{str(msg_id)}" 
      title = message.raw_text.split('\n\n')[0]
      description = message.raw_text.replace('\n', '|')
      keybo.append(
        mikey.builder.article(
          title=f'{title}',
          description=f'{description}......',
          text=f'{message.text}',
          )
        )
  if keybo == []:
      await mikey.answer([], switch_pm='Couldn\'t find...', switch_pm_param='')
  await mikey.answer(keybo)

@user_admin
@draken.on(events.CallbackQuery(pattern=b'recomp'))
async def de(mikey):
  await mikey.delete()

#imdbSearch
@draken.on(events.NewMessage(pattern=r'^\/imdb(.*)'))
async def imdb_search(mikey):
  try:
    query = mikey.message.text.split(' ', 1)[1]
  except IndexError:
    await mikey.reply('What to?')
  search = movie.movie_search(query)
  genres = ','.join(search[3])
  text = f'**{search[1]}**\n**Imdb Rating:** {search[2]}/10.0\n**Genres:** {genres}\n**Year:** {search[5]}\n**Type:** {search[6]}\n\n**Synopsis**: {search[7][0].split(":")[0]}....[­ ]({search[0]})'
  await mikey.reply(text)

@draken.on(events.NewMessage(pattern=r'^\/up(.*)'))
async def upload(mikey):
  if not mikey.is_private:
    return
  if not mikey.sender_id in admins:
    return
  try:
    query = mikey.message.text.split(' ', 1)[1]
  except IndexError:
    return await mikey.reply('wht to?')
  r = request.get(query, stream=True)
  if r.status_code == 200 and r.content:
      #extension = mimtypes.guess_extension(r.headers.get('content-type', '').split(';')[0])
      d = r.headers['content-disposition']
      fname = re.findall("filename=(.+)", d)
      f = open(fname, 'wb')
      m = await mikey.reply(f'Downloading {fname}....')
      count = 0
      size = r.headers['Content-lenght']
      dsize = 0
      for i in r.iter_content(chunk_size=1024*10):
        f.write(i)
        count += 1
        dsize += 1024*10
        if count == 10:
          await m.edit(f'{hrs(dsize)} of {hrs(size)} done...')
      await m.edit('Uploading....')
      await draken.send_file(mikey.chat_id, fname)
  else:
    await mikey.reply('Ahk couldnt!')  
  


#torrent search 
@draken.on(events.NewMessage(pattern=r'^\/torrent'))
async def torrentsearch(mikey):
  query = mikey.message.text.split(' ', 1)
  try:
    query = query[1]
  except IndexError:
    return await mikey.reply('What to search? huh? that too i will decide? dont be lazy dumbass!')
  search = thirteenX.search(query)
  #print(search)
  count = 0
  count2 = 0
  keybo = []
  msg_to_send = ''
  text = ''
  for i in search:
    while count < 5:
      #print(i)
      count += 1
      msg_to_send += f"**{count}.{i[0]}\nSize: {i[2]}**\n\n"
      r = i[1].split('/')[4]
      keybo.append(Button.url(text=str(count), url=f'https://t.me/DrakenKunRoBot?start={r}'))
  for i in search: 
    count2 += 1
    r2 = i[1].split('/')[4]
    link = f'https://t.me/DrakenKunRoBot?start={r2}'
    text += f'{count2}.{i[0]}<br>Size: {i[2]}<br><a href = "{link}">Click here to get more info</a><p>'
  h = hina.post(title = f'Results for {query}', author = 'Draken', text=text)  
  url = h.get('url')
  if msg_to_send == '':
    await mikey.reply('Sorry, no results found!')
    return 
  markup = [keybo, [Button.url(text='More Results', url = url)]]
  await mikey.reply(msg_to_send, buttons=markup, parse_mode = 'md')

print('Im online!!!')

loop.run_until_complete(get_all_admins(REQ_CHAT))

takemichi.start()
draken.start()
draken.run_until_disconnected()
takemichi.run_until_disconnected()
