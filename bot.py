from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChatAdminRequiredError
from os import getenv
from utils import link_gen
import logging
import webbrowser
from dotenv import load_dotenv
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")
bot_token = getenv("BOT_TOKEN")
force_sub_channel = getenv("FORCE_SUB", "my_introvert_world")

if not api_id or not api_hash or not bot_token:
    raise ValueError("API ID, API HASH, and BOT TOKEN must be set")

bot = TelegramClient(
    'Linkchanger',
    api_id=api_id,
    api_hash=api_hash
).start(
    bot_token=bot_token
)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hi, I am the link changer of Physics Wallah")

@bot.on(events.NewMessage(pattern='https://'))
async def change(event):
    try:
        await bot.get_permissions(force_sub_channel, event.sender_id)
    except UserNotParticipantError:
        await event.respond(f"Subscribe to @{force_sub_channel}")
    except ChatAdminRequiredError:
        await event.respond(f"Make me admin in your force subscribe group!\nForce subscribe here: @{force_sub_channel}")
    else:
        try:
            link_hash = event.raw_text.split('/')[3]
        except IndexError:
            await event.respond("Invalid URL!")
        except Exception as e:
            await event.respond(str(e))
        else:
            await link_gen(link_hash, bot, event)

@bot.on(events.NewMessage(pattern='/Bulk'))
async def Bulk(event):
    await event.respond(
        "*Follow Steps To Genrate Link In Bulk*\n"
        "1. Generate Your Secret ID:\n"
        "- Click on the \"Get Secret Id\" button.\n"
        "- The bot will send you a message with your secret ID in monospace format.\n"
        "- Copy this ID for later use.\n\n"
        "2. Start Bulk Bink maker Panel:\n"
        "- Click on the \"Get script\" button to initiate the link maker panel.\n\n"
        "3. Enter Your Details:\n"
        "- Paste your JSON data: Enter the JSON data required for the script.\n"
        "- Select Quality: Choose the desired quality setting for your script.\n"
        "- Paste your Secret ID: Enter the secret ID you obtained from the Alpha bot.\n"
        # "- Enter your Batch Name: Provide a name for your batch process.\n\n"
        "4. Send File to Telegram Bot:\n"
        "- Click on the \"Send to Telegram bot\" button to submit your details and start the link changing process.",
        buttons=[Button.url("Get Link In Bulk", "https://t.me/Alpha_Script_Robot/AlphaNetwork"),Button.inline("Get Chat ID", b"get_chat_id")]
        
    )
@bot.on(events.CallbackQuery(data=b"get_chat_id"))
async def get_chat_id(event):
    chat_id = event.chat_id
    await event.respond(f"Chat ID: `{chat_id}`")    

@bot.on(events.NewMessage(pattern='/Get_Secret_ID'))
async def get_chat_id(event):
    chat_id = event.chat_id
    await event.respond(f"Your Secret ID Is: `{chat_id}`")
logger.info("Bot started..")
bot.run_until_disconnected()
