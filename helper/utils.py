from datetime import datetime
from pytz import timezone
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


OnWelcBtn = InlineKeyboardButton(text='Welcome On ✅', callback_data='welc-on')
OffWelcBtn = InlineKeyboardButton(text='Welcome Off ❌', callback_data='welc-off')
OnLeavBtn = InlineKeyboardButton(text='Leave On ✅', callback_data='leav-on')
OffLeavBtn = InlineKeyboardButton(text='Leave Off ❌', callback_data='leav-off')
OnAutoacceptBtn = InlineKeyboardButton(text='Auto accept On ✅', callback_data='autoaccept-on')
OffAutoacceptBtn = InlineKeyboardButton(text='Auto accept Off ❌', callback_data='autoaccept-off')

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {b.mention}"
        )
