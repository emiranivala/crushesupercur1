import asyncio
import importlib
import logging
import signal
import sys
from pyrogram import idle
from Restriction.modules import ALL_MODULES

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ----------------------------Bot-Start---------------------------- #

loop = asyncio.get_event_loop()

# Handle graceful shutdown
def signal_handler(sig, frame):
    logger.info("Shutdown signal received, stopping bot...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def sumit_boot():
    try:
        # Import all modules
        for all_module in ALL_MODULES:
            try:
                importlib.import_module("Restriction.modules." + all_module)
                logger.info(f"Loaded module: {all_module}")
            except Exception as e:
                logger.error(f"Failed to load module {all_module}: {str(e)}")
        
        logger.info("»»»» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
        
        # Keep the bot running
        await idle()
        
        logger.info("»» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")
    except Exception as e:
        logger.error(f"Critical error during bot startup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        loop.run_until_complete(sumit_boot())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

# ------------------------------------------------------------------ #
