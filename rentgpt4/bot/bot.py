import logging, random
import os, django, sys
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from asgiref.sync import sync_to_async
from openai import OpenAI

client = OpenAI(api_key = '')

bot1 = Bot(token = '')
storage1 = MemoryStorage()
dp1 = Dispatcher(storage = storage1)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


@dp1.message(Command('start'))
async def welcome(message: types.Message, state: FSMContext):
    await bot1.send_message(chat_id = message.chat.id, text = 'Welcome to RentGPT4!🤩 \n \n To start using the bot, please, add money to your balance by button below⬇️', reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = 'Pay money', callback_data = 'pay')]]))
    await bot1.send_message(chat_id = message.chat.id, text = 'Your balance: 500 tg 🔥 \n Now, you can ask any question from GPT4')

@dp1.message()
async def answer(message: types.Message, state: FSMContext):
    prompt = message.text
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f'{prompt}'
            }
        ]
    )

    await message.reply(text = completion.choices[0].message.content)

async def main():
    # Run both bots' polling concurrently using separate tasks
    await dp1.start_polling(bot1)

if __name__ == '__main__':
    asyncio.run(main())