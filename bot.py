import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv('.env')

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017')

# Initialize aiogram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Initialize MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["telegram"]
messages_collection = db.get_collection("messages")

# Message handler
@dp.message()
async def save_message(message: types.Message):
    await messages_collection.insert_one(message.model_dump())

def main():
    dp.start_polling(bot, polling_timeout=60)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
