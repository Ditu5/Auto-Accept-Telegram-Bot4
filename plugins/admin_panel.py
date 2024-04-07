from config import Config
from helper.database import db
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime
from pyromod.exceptions import ListenerTimeout

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# approve all pending request is only for user for more info https://docs.pyrogram.org/api/methods/approve_all_chat_join_requests#pyrogram.Client.approve_all_chat_join_requests:~:text=Approve%20all%20pending%20join%20requests%20in%20a%20chat. only Usable by User not bot

user = Client(name="User", api_id=Config.API_ID,
              api_hash=Config.API_HASH, session_string=Config.SESSION)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(
        time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")


# Restart to cancell all process
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ⚠️ Broadcasting only those people who has started your bot


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")


async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500


@Client.on_message(filters.private & filters.command('acceptall') & filters.user(Config.ADMIN))
async def handle_acceptall(bot: Client, message: Message):
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)

    if len(list(chat_ids)) == 0:
        return await ms.edit("**I'm not admin in any Channel or Group yet !**")

    button = []
    for id in chat_ids:
        info = await bot.get_chat(id)
        button.append([InlineKeyboardButton(
            f"{info.title} {str(info.type).split('.')[1]}", callback_data=f'acceptallchat_{id}')])

    await ms.edit("Select Channel or Group Bellow Where you want to accept pending request\n\nBelow Channels or Group I'm Admin there", reply_markup=InlineKeyboardMarkup(button))


@Client.on_message(filters.private & filters.command('declineall') & filters.user(Config.ADMIN))
async def handle_declineall(bot: Client, message: Message):
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)

    if len(list(chat_ids)) == 0:
        return await ms.edit("**I'm not admin in any Channel or Group yet !**")

    button = []
    for id in chat_ids:
        info = await bot.get_chat(id)
        button.append([InlineKeyboardButton(
            f"{info.title} {str(info.type).split('.')[1]}", callback_data=f'declineallchat_{id}')])

    await ms.edit("Select Channel or Group Bellow Where you want to accept pending request\n\nBelow Channels or Group I'm Admin there", reply_markup=InlineKeyboardMarkup(button))


@Client.on_callback_query(filters.regex('^acceptallchat_'))
async def handle_accept_pending_request(bot: Client, update: CallbackQuery):
    # await update.message.delete()
    chat_id = update.data.split('_')[1]
    ms = await update.message.edit("**Please Wait Accepting the peding requests. ♻️**")
    try:
        while True:
            try:
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                asyncio.sleep(t.value)
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except Exception as e:
                print('Error on line {}'.format(
                    sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                pass

                pass
    except:
        await update.message.reply_text(f"**Task Completed** ✓ **Approved ✅ All Pending Join Request**")
        await ms.delete()


@Client.on_callback_query(filters.regex('^declineallchat_'))
async def handle_delcine_pending_request(bot: Client, update: CallbackQuery):
    ms = await update.message.edit("**Please Wait Declining all the peding requests. ♻️**")
    chat_id = update.data.split('_')[1]

    try:
        while True:
            try:
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                asyncio.sleep(t.value)
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except:
                pass

    except:
        await ms.delete()
        await update.message.reply_text("**Task Completed** ✓ **Declined ❌ All The Pending Join Request**")
