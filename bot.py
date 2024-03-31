import os
import asyncio
from aiogram import Bot, Dispatcher, types
from motor.motor_asyncio import AsyncIOMotorClient

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017')

# Initialize aiogram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Initialize MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("telegram_bot")
messages_collection = db.get_collection("messages")

# Message handler
@dp.message()
async def save_message(message: types.Message):
    await messages_collection.insert_one(message.model_dump())

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot, polling_timeout=60))
