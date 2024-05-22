from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatAdminRequiredError
from os import getenv
from utils import link_gen
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = TelegramClient(
    'Linkchanger',
    api_id = getenv("API_ID"),
    api_hash = getenv("API_HASH")

).start(
    bot_token = getenv("BOT_TOKEN")

)


force_sub_channel = getenv("FORCE_SUB", "my_introvert_world")

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hi, I am link changer of Physics Wallah")

        
@bot.on(events.NewMessage(pattern='https://'))
async def change(event):
    try:
        await bot.get_permissions(force_sub_channel, event.sender_id)

    except UserNotParticipantError:
        await event.respond(f"Subscribe to @{force_sub_channel}")

    except ChatAdminRequiredError:
        await event.respond(f"Make me admin in your force subscribe group !\nForce subscribe here: @{force_sub_channel}")

    else:
        try:
            link_hash = event.raw_text.split('/')[3]

        except IndexError as e:
            await event.respond("Invalid url !")

        except Exception as e:
            await event.respond(str(e))
        
        else:
            await link_gen(link_hash, bot, event)


logger.info("Bot started..")
bot.run_until_disconnected()