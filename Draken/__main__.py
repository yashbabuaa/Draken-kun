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

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

hina = TelegraphPoster(use_api=True)
hina.create_api_token('DontKnow')

#commands
admins = []

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
  await get_all_admins 
  await mikey.reply('Done!')
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^\/files(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^\/search(.*)'))
@draken.on(events.NewMessage(incoming=True, pattern=r'^#request(.*)'))
async def request(mikey):
  chat = -1001487075546
  chat2 = -1001550963689
  if mikey.message.text.startswith("#request"):
    search = False
    if mikey.is_private:
      return
  else:
    if not mikey.is_private:
      return
    search = True
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
  if search == True:
    count2 = 0
    if keybo == []:
      async for message in takemichi.iter_messages(chat2, search = query, reverse = True, filter = InputMessagesFilterDocument):
        hek = await draken.get_messages(chat2, ids = message.id)
        await draken.send_message(mikey.chat_id, file = hek.media)
        count2 += 1 
      if not count2 == 0:
        await mikey.reply("👆")
      if count2 == 0:
        await mikey.reply('Not found')
    else:
      m = await mikey.reply("Found some results....", buttons = keybo)
    return
  if keybo == []:
    poki = []
    cnt = 0
    async for message in takemichi.iter_messages(-1001567289850, search = query, reverse = True):
      if message.media:
        if cnt == 1:
          break
        link = f'https://t.me/c/1567289850/{message.id}'
        poki.append([Button.url(text=f'{message.file.name[:-10]}...', url=link)])
        cnt += 1
      else:
        pass
    if not poki == []:
      poki.append([Button.url(text='Join Channel to access', url = 'https://t.me/joinchat/p0HI9d4zlc43NTRl')])
      await mikey.reply('Found some results in channel, check if matches your query, else request and be specific....', buttons=poki )
      return
  else:
    await mikey.reply("Found some results....", buttons = keybo)
    return
  if req_log == "True":
    req_user = f"[{mikey.sender.first_name}](tg://user?id={mikey.sender_id})" 
    message_link = f"https://t.me/c/1364238597/{mikey.id}"
    text = f"Request: {query}\nRequested by: {req_user}\n"
    await draken.send_message(-1001550475256, text, buttons = [[Button.url(text = "Message", url = message_link)], [Button.inline(text="Request Complete", data = "recomp")]])
    markup = [Button.url(text='Check Your Request', url='https://t.me/joinchat/p0HI9d4zlc43NTRl')]
    await mikey.reply("Roger! Request taken, Now wait till its posted at the channel given below...", buttons=markup)
  
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
    await mikey.message.reply(f"Im {bot_name} a bot, \n\nMade by @DontKnowWhyRU and managed by @TvSeriesArchive")
    await draken.send_message(-1001161807206, f"#START\n[{mikey.sender.first_name}](tg://user?id={mikey.sender_id}) started the bot!")
  else:
    await mikey.reply("Im up and working!")

@user_admin
@draken.on(events.InlineQuery)
async def post_comp(mikey):
  if mikey.text == '':
    await mikey.answer([], switch_pm_text='Paste the link', switch_pm_param="start")
  link = mikey.text 
  hek = [
    mikey.builder.article(
      title='Post Complete',
      description='Button make for post completion...'
      text='Your request was being posted in the channel, check it out!',
      buttons=[
        [
          Button.url(text='The post', url=link)
          ],
        [
          Button.url(text='Join to Accsss', url='https://t.me/joinchat/p0HI9d4zlc43NTRl')
          ]
        ]
      )
    ]
 await mikey.answer(hek)

@user_admin
@draken.on(events.CallbackQuery(pattern=b'recomp'))
async def de(mikey):
  await mikey.delete()

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

loop.run_until_disconnected(get_all_admins(-1001364238597))

takemichi.start()
draken.start()
draken.run_until_disconnected()
takemichi.run_until_disconnected()