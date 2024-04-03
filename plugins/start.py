from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from helper.database import db
from config import Config, TxT
from helper.utils import (
    OnWelcBtn,
    OnLeavBtn,
    OffWelcBtn,
    OffLeavBtn,
    OnAutoacceptBtn,
    OffAutoacceptBtn,
)


@Client.on_message(filters.private & filters.command("start"))
async def handle_start(bot: Client, message: Message):
    SnowDev = await message.reply_text(text="**Please Wait...**", reply_to_message_id=message.id)
    await db.add_user(b=bot, m=message)
    text = f"Hi, {message.from_user.mention}\n\n I'm Auto Accept Bot I can accpet user from any channel and group just make me admin there."
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Developer 👨‍💻", url="https://t.me/Snowball_Official")],
            [InlineKeyboardButton("Help", callback_data="help")],
        ]
    )
    if Config.START_PIC:
        if message.from_user.id == Config.ADMIN:
            await SnowDev.delete()
            await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=reply_markup)
        else:
            await SnowDev.delete()
            await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Developer 👨‍💻", url="https://t.me/Snowball_Official")]]))
    else:
        if message.from_user.id == Config.ADMIN:
            await SnowDev.edit(text=text, reply_markup=reply_markup)
        else:
            await SnowDev.edit(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Developer 👨‍💻", url="https://t.me/Snowball_Official")]]))


@Client.on_message(filters.private & filters.command("set_welcome") & filters.user(Config.ADMIN))
async def set_welcome_msg(bot: Client, message: Message):
    welcome_msg = message.reply_to_message
    if welcome_msg:
        SnowDev = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
        try:
            if welcome_msg.photo or welcome_msg.video or welcome_msg.animation:
                await db.set_welcome(message.from_user.id, welcome_msg.caption)
                await db.set_welc_file(message.from_user.id, welcome_msg.photo.file_id if welcome_msg.photo else welcome_msg.video.file_id if welcome_msg.video else welcome_msg.animation.file_id)
            else:
                await db.set_welcome(message.from_user.id, welcome_msg.text)
                await db.set_welc_file(message.from_user.id, None)
        except Exception as e:
            return await SnowDev.edit(e)
        await SnowDev.edit("Successfully Set Your Welcome Message ✅")
    else:
        await message.reply_text("Invalid Command !\n⚠️ Format ➜ `Hey, {user} Welcome to {title}` \n\n **Reply to message**")


@Client.on_message(filters.private & filters.command("set_leave") & filters.user(Config.ADMIN))
async def set_leave_msg(bot: Client, message: Message):
    leave_msg = message.reply_to_message
    if leave_msg:
        SnowDev = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
        try:
            if leave_msg.photo or leave_msg.video or leave_msg.animation:
                await db.set_leave(message.from_user.id, leave_msg.caption)
                await db.set_leav_file(message.from_user.id, leave_msg.photo.file_id if leave_msg.photo else leave_msg.video.file_id if leave_msg.video else leave_msg.animation.file_id)
            else:
                await db.set_leave(message.from_user.id, leave_msg.text)
                await db.set_leav_file(message.from_user.id, None)
        except Exception as e:
            return await SnowDev.edit(e)
        await SnowDev.edit("Successfully Set Your Leave Message ✅")
    else:
        await message.reply_text("Invalid Command !\n⚠️ Format ➜ `Hey, {user} By See You Again from {title}` \n\n **Reply to message**")
        
        
@Client.on_message(filters.private & filters.command('auto_approves') & filters.user(Config.ADMIN))
async def handle_auto_approves(bot: Client, message:Message):
    
    SnowDev = await message.reply_text('**Please Wait...**', reply_to_message_id=message.id)

    btns = []

    db_channels = await db.get_admin_channels()
    try:
        for key, value in db_channels.items():
            chnl = await bot.get_chat(key)
            if value:
                
                btns.append([InlineKeyboardButton(f'{chnl.title} ✅', callback_data=f'autoapprove_{key}')])
            else:
                btns.append([InlineKeyboardButton(f'{chnl.title} ❌', callback_data=f'autoapprove_{key}')])
        
    
        await SnowDev.edit("**Here are the channels where I'm admin and you can toggle the auto accept functionality.**", reply_markup=InlineKeyboardMarkup(btns))
    except Exception as e:
        print(e)


@Client.on_message(filters.private & filters.command('option') & filters.user(Config.ADMIN))
async def set_bool_welc(bot: Client, message: Message):
    SnowDev = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)

    user_id = message.from_user.id
    bool_welc = await db.get_bool_welc(user_id)
    bool_leav = await db.get_bool_leav(user_id)
    bool_auto_accept = await db.get_bool_auto_accept(user_id)

    welc_buttons = [OnWelcBtn, OffWelcBtn]
    leav_buttons = [OnLeavBtn, OffLeavBtn]
    autoaccept_buttons = [OnAutoacceptBtn, OffAutoacceptBtn]

    # Determine button configurations based on user settings
    welc_button_row = [welc_buttons[0] if bool_welc else welc_buttons[1],
                       leav_buttons[0] if bool_leav else leav_buttons[1]]
    autoaccept_button_row = [autoaccept_buttons[0]
                             if bool_auto_accept else autoaccept_buttons[1]]

    # Update text and buttons based on user settings
    text = "Click the button from below to toggle Welcome & Leaving Message also Auto Accept."
    reply_markup = InlineKeyboardMarkup(
        [welc_button_row, autoaccept_button_row])

    # Edit message with updated text and buttons
    await SnowDev.edit(text=text, reply_markup=reply_markup)


@Client.on_callback_query()
async def handle_CallbackQuery(bot: Client, query: CallbackQuery):

    data = query.data
    
    
    if data.startswith('autoapprove_'):
        id = data.split('_')[1]
        
        text = "**Here are the channels where I'm admin and you can toggle the auto accept functionality.**"

        db_channels = await db.get_admin_channels()
        btn = []
        try:
            for key, value in db_channels.items():
                channel = await bot.get_chat(key)
                
                if key == id:
                    if value:
                        await db.update_admin_channel(id, False)
                        btn.append([InlineKeyboardButton(f'{channel.title} ❌', callback_data=f'autoapprove_{key}')])
                    else:
                        await db.update_admin_channel(id, True)
                        btn.append([InlineKeyboardButton(f'{channel.title} ✅', callback_data=f'autoapprove_{key}')])
                
                else:
                    if value:
                        btn.append([InlineKeyboardButton(f'{channel.title} ✅', callback_data=f'autoapprove_{key}')])
                    else:
                        btn.append([InlineKeyboardButton(f'{channel.title} ❌', callback_data=f'autoapprove_{key}')])
            
            await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))        
        except Exception as e:
            return query.message.edit("**I'm Not admin in any channel or group yet**\n\nOR Maybe you make me admin in any channels or group when i was offline so make sure to remove me and make me admin again !")
                    

    elif data.startswith('welc'):
        text = "Click the button from below to toggle Welcome & Leaving Message also Auto Accept."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_welc(query.from_user.id, False)
            if await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

        elif boolean == 'off':
            await db.set_bool_welc(query.from_user.id, True)
            if await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):

                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

    elif data.startswith('leav'):
        text = "Click the button from below to toggle Welcome & Leaving Message also Auto Accept."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_leav(query.from_user.id, False)
            if await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

        elif boolean == 'off':
            await db.set_bool_leav(query.from_user.id, True)
            if await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                if await db.get_bool_auto_accept(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn], [OffAutoacceptBtn]]))

    elif data.startswith('autoaccept'):
        text = "Click the button from below to toggle Welcome & Leaving Message also Auto Accept."
        boolean = data.split('-')[1]

        if boolean == 'on':
            await db.set_bool_auto_accept(query.from_user.id, False)
            if await db.get_bool_welc(query.from_user.id) and await db.get_bool_leav(query.from_user.id):
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            elif await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_leav(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))

            elif await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_welc(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OffAutoacceptBtn]]))

            else:
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OffAutoacceptBtn]]))
        else:
            await db.set_bool_auto_accept(query.from_user.id, True)
            if await db.get_bool_welc(query.from_user.id) and await db.get_bool_leav(query.from_user.id):
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

            elif await db.get_bool_welc(query.from_user.id):
                if await db.get_bool_leav(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

            elif await db.get_bool_leav(query.from_user.id):
                if await db.get_bool_welc(query.from_user.id):
                    return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OnWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OnLeavBtn], [OnAutoacceptBtn]]))

            else:
                return await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[OffWelcBtn, OffLeavBtn], [OnAutoacceptBtn]]))

    elif data == 'help':
        await query.message.edit(TxT.HELP_MSG, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✘ Close ✘', callback_data='close')]]))

    elif data == 'close':
        await query.message.delete()
        await query.message.continue_propagation()
