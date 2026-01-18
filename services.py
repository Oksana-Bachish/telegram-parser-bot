import json
import os
import asyncio
from datetime import date, datetime
from aiogram import types
from aiogram.utils.markdown import hlink

from parsing import get_parsing

# Основная функция обработки запроса бренда
async def handle_brand_request(brand: str, message: types.Message):
    json_path = get_json_path(brand)
    # Если файла нет или он устарел
    if not os.path.exists(json_path) or not is_today(json_path):
        await run_parsing(message)
    # Загружаем JSON и отправляем данные
    data = load_json(json_path)
    await get_info(data, message)


# Получить путь к JSON по бренду
def get_json_path(brand: str):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'json_files',
        f'{brand}.json'
    )

# Проверка, обновлен ли файл сегодня
def is_today(path: str):
    file_date = date.fromtimestamp(os.path.getmtime(path))
    return file_date == date.today()


# Загрузка данных из JSON
def load_json(path: str):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


# Асинхронный запуск синхронного парсера
async def run_parsing(message: types.Message):
    await message.answer('Собираю данные, пожалуйста, подождите...')
    try:
        await asyncio.to_thread(get_parsing)
    except Exception as e:
        await message.answer(f'Ошибка при парсинге: {e}')
        raise


# Отправка пользователю информации о товарах
async def get_info(data, message: types.Message):
    if not data:
        await message.answer('Товар не найден')
        return
    else:
        for item in data:
            card = hlink(item.get('prod_name'), item.get('link'))
            price = item.get('price') or '-'
            discount_price = item.get('discount_price') or '-'
            text = f'{card}\n ' \
                   f'Цена: {price}; \n ' \
                   f'Цена с клубной картой: {discount_price} 💳'
            await message.answer(text)
