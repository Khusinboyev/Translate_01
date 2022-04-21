from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()

#  5098772001:AAFd4zTQxb-Bew6SCs0f7B5yTiNp_Hekwg8

TOKEN = "5098772001:AAFd4zTQxb-Bew6SCs0f7B5yTiNp_Hekwg8"

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
