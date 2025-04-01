import asyncio
import logging
import sys
import os
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------- #

loop = asyncio.get_event_loop()

# Create sessions directory if it doesn't exist
try:
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
        logger.info("Created sessions directory")
except Exception as e:
    logger.error(f"Failed to create sessions directory: {str(e)}")

try:
    app = Client(
        "sessions/restrict_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=32  
    )
    logger.info("Telegram Client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Telegram Client: {str(e)}")
    sys.exit(1)

# ----------------------------Bot-Info---------------------------- #

async def bot_info():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    try:
        await app.start()
        getme = await app.get_me()
        BOT_ID = getme.id
        BOT_USERNAME = getme.username
        app.set_parse_mode(ParseMode.DEFAULT)
        if getme.last_name:
            BOT_NAME = getme.first_name + " " + getme.last_name
        else:
            BOT_NAME = getme.first_name
        logger.info(f"Bot started as {BOT_NAME} (@{BOT_USERNAME})")
    except Exception as e:
        logger.error(f"Error getting bot info: {str(e)}")
        sys.exit(1)

try:
    loop.run_until_complete(bot_info())
except Exception as e:
    logger.error(f"Fatal error during initialization: {str(e)}")
    sys.exit(1)

# ---------------------------------------------------------------- #



