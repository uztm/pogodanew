import logging
from aiogram import Bot, Dispatcher, executor, types
from markups import *
from config import *
import datetime
import requests
open_weather_token = "d7748d00159d9aa009b940c9e80a5100"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def check_sub_channels(channels, user_id):
  for channel in channels:
    chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
    # print(chat_member['status'])
    if chat_member['status'] == 'left':
       return False
  return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  if message.chat.type == 'private':
    if await check_sub_channels(CHANNELS, message.from_user.id):
      await message.answer(f"Привет {'<b>'}{message.from_user.full_name}{'</b>'} Пожалуйста, введите название города для получения информации о погоде. 🌤️",parse_mode = 'HTML')
    else:
      await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)
  # print(message)

# @dp.message_handler()
# async def bot_message(message: types.Message):
#   if message.chat.type == 'private':
#     if await check_sub_channels(CHANNELS, message.from_user.id):
#       if message.text == 'Профил':
#         await bot.send_message(message.from_user.id, "Привет !")
#         # await bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")
#       else:
#             await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)


@dp.message_handler()
async def get_weather(message: types.Message):
  if message.chat.type == 'private':
    if await check_sub_channels(CHANNELS, message.from_user.id):
        code_to_smile = {
            "Clear": "Ochiq \U00002600",
            "Clouds": "Bulutli \U00002601",
            "Rain": "Yomg'ir \U00002614",
            "Drizzle": "Yomg'ir \U00002614",
            "Thunderstorm": "Momaqaldiroq \U000026A1",
            "Snow": "Qor \U0001F328",
            "Mist": "Tuman \U0001F32B"
        }

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                  f"🌤️ Погода в городе: {city}\n🌡️ Температура: {cur_weather}C° {wd}\n"
                  f"💧 Влажность: {humidity}%\n🔵 Давление: {pressure} mm.s\n🌬️ Ветер: {wind} m/s\n"
                  f"🌅 Восход: {sunrise_timestamp}\n🌅 Закад: {sunset_timestamp}\n⏳ Продолжительность дня: {length_of_the_day}\n"
                  f"***Хорошего дня!*** \n\n @tmpogodabot"
                  )

        except:
            await message.reply("🆎 Проверьте название города 🆎")
    else:
              await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)


# # print(message.text)
@dp.callback_query_handler(text="subchanneldone")
async def  subchanneldone(message: types.Message):
  await bot.delete_message(message.from_user.id, message.message.message_id)
  if await check_sub_channels(CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, f"{'<b>'}{message.from_user.full_name}{'</b>'} Пожалуйста, введите название города для получения информации о погоде. 🌤️",parse_mode = 'HTML')
  else:
     await bot.send_message(message.from_user.id, NOT_SUB_MESSAGE, reply_markup=lang)



if __name__ == "__main__":
  executor.start_polling(dp, skip_updates=True)