import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

import os
import json

with open('config.json', 'r') as f: DATA = json.load(f)
def getenv(var): return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = getenv("STRING")
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")

@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am batch maker bot", reply_to_message_id=None)

@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	print(message.text)
	bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=None)
	url = message.text
	try:
		os.system('ffmpeg -i ' + url + ' -c copy -bsf:a aac_adtstoasc main.mp4') 
		bot.send_video(message.chat.id, "main.mp4",progress=progress, reply_to_message_id=None, progress_args=[message,"up"])
		os.remove("main.mp4")
	except:
		bot.send_message(message.chat.id, 'Give correct url', reply_to_message_id=None)


bot.run()
#
