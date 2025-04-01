import logging
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    mongo = MongoCli(MONGO_DB)
    db = mongo.users
    db = db.users_db
    logger.info("MongoDB connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    # Provide a fallback
    mongo = None
    db = None


# ----------------------------------------------------------- #

async def get_users():
    try:
        if not db:
            logger.error("Database connection not available")
            return []
        user_list = []
        async for user in db.users.find({"user": {"$gt": 0}}):
            user_list.append(user['user'])
        return user_list
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return []

# ----------------------------------------------------------- #

async def get_user(user):
    try:
        users = await get_users()
        if user in users:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error checking user {user}: {str(e)}")
        return False
    
# ----------------------------------------------------------- #

async def add_user(user):
    try:
        if not db:
            logger.error("Database connection not available")
            return False
        users = await get_users()
        if user in users:
            return True
        else:
            await db.users.insert_one({"user": user})
            return True
    except Exception as e:
        logger.error(f"Error adding user {user}: {str(e)}")
        return False

# ----------------------------------------------------------- #

async def del_user(user):
    try:
        if not db:
            logger.error("Database connection not available")
            return False
        users = await get_users()
        if not user in users:
            return False
        else:
            await db.users.delete_one({"user": user})
            return True
    except Exception as e:
        logger.error(f"Error deleting user {user}: {str(e)}")
        return False
    


