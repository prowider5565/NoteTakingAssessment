from aiogram import types, Bot, Dispatcher
import logging

from src.settings import settings


bot = Bot(token=settings.TOKEN)
dp = Dispatcher()
