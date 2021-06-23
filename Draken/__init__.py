import os 
from telethon.sync import TelethonClient

bot_token = os.environ.get('BOT_TOKEN')
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

draken = TelethonClient('bot', api_id, api_hash).start(bot_token=bot_token)

