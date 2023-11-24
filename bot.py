import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command


from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from utils import *
from states import *
from database import *
from config import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


async def command_menu(dp: Dispatcher):
  await dp.bot.set_my_commands(
    [
      types.BotCommand('start', 'Ishga tushirish'),
    ]
  )
  await create_tables()

@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await message.answer("Salom")
  await add_user(message.from_user.id, message.from_user.username)


@dp.message_handler(content_types=['audio'])
async def get_user_audio_handler(message: types.Message):
  user_id = message.from_user.id
  filename = f"audio_{user_id}.mp3"
  await message.audio.download(destination_file=filename)


  title, subtitle = await media_shazaming(filename)
  await message.reply(f"Nomi: {title}\nIjrochi: {subtitle}")


@dp.message_handler(content_types=['video'])
async def get_user_video_handler(message: types.Message):
  user_id = message.from_user.id
  filename = f"video_{user_id}.mp4"
  file_size = round(message.video.file_size / 1024 / 1024)
  if file_size <= 20:
    await message.video.download(destination_file=filename)

    result = await media_shazaming(filename)
    await message.reply(f"Nomi: {result[0]}\nIjrochi: {result[1]}")
    if len(result) == 3:
            await message.answer_audio(types.InputFile(result[-1]))

    await delete_user_media(user_id)
  else:
    await message.answer("20mb dan yuqori xajimdagi videoni tortaolmiman")

@dp.message_handler(commands=['admin'])
async def admin_handler(message: types.Message):
  users = await get_all_users()   
  await message.answer(f"Userlar soni: {users[0]}")


if __name__ == "__main__":
  executor.start_polling(dp, on_startup=command_menu)
