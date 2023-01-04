from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS


lang = InlineKeyboardMarkup(
  row_width=1,
  inline_keyboard=[
    [
      InlineKeyboardButton(text="Канал 1", url='https://t.me/tmportfolio'),
    ],
    [
      InlineKeyboardButton(text="Канал 2", url='https://t.me/tmBots_bek'),
    ],
    [
      InlineKeyboardButton(text="Я ПОДПИСАЛСЯ", callback_data="subchanneldone"),
    ]
  ]
)


# def showChannels():
#   keyboard = InlineKeyboardMarkup(row_width=1)

#   for channel in CHANNELS:
#     btn = InlineKeyboardButton(text=channel[0], url=channel[2])
#     keyboard.insert(btn)

#     btnDoneSub = InlineKeyboardButton(text="Я ПОДПИСАЛСЯ", callback_data="subchanneldone")
#     keyboard.insert(btnDoneSub)
#     return keyboard
