import logging
import logging.config
from pyrogram import Client
from pyrogram import Client, __version__
from config import Config
from aiohttp import web
from plugins.web_support import web_server
import pyromod


logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="AutoAcceptBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

        if Config.ADMIN:
            try:
                await self.send_message(Config.ADMIN, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except:
                pass

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")


bot = Bot()
bot.run()
