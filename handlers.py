from aiogram import Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton
from services import handle_brand_request

BRANDS = {
    'Samsung': 'samsung',
    'Iphone': 'iphone',
    'Xiaomi': 'xiaomi'
}

def register_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(handle_brand, F.text.in_(BRANDS.keys()))


# Создаем клавиатуру выбора бренда смартфонов
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=brand) for brand in BRANDS]],
                                         resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Выберите бренд', reply_markup=keyboard)


# Обрабатываем выбор бренда и запускаем обработку запроса
async def handle_brand(message: types.Message):
    brand_key = BRANDS[message.text]
    await handle_brand_request(brand_key, message)
