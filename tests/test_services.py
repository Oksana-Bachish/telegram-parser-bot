import pytest
from unittest.mock import AsyncMock, patch
from services import handle_brand_request

@pytest.mark.asyncio
async def test_handle_brand_request_cached_today(mocker):
    """Тест кеширования: если файл свежий, парсер не вызывается, данные берутся из JSON"""

    # Имитируем, что актуальный файл с кешем существует в системе
    mocker.patch('services.os.path.exists', return_value=True)
    mocker.patch('services.is_today', return_value=True)
    mock_load_json = mocker.patch('services.load_json', return_value=[
        {'prod_name': 'Test Phone', 'link': 'http://test', 'price': '1000 p.', 'discount_price': None}
    ])

    # Перехватываем вызов функции парсинга
    mock_run_parsing = mocker.patch('services.run_parsing', new_callable=AsyncMock)

    mock_message = AsyncMock()
    mock_message.answer = AsyncMock()

    # Запуск тестируемой бизнес-логики
    await handle_brand_request('samsung', mock_message)

    # Проверка, что парсер проигнорирован, а данные отправлены из JSON
    assert not mock_run_parsing.called
    assert mock_load_json.called
    assert mock_message.answer.called

    # Валидация текста отправленной пользователю карточки
    args, kwargs = mock_message.answer.call_args
    assert 'Test Phone' in args[0]


@pytest.mark.asyncio
async def test_handle_brand_request_needs_parsing(mocker):
    """Тест устаревшего кеша: если файла нет, запускается парсинг"""

    # Имитируем отсутствие файла с кешем на диске
    mocker.patch('services.os.path.exists', return_value=False)
    mocker.patch('services.load_json', return_value=[])

    # Изолируем тяжелый вызов парсера в потоке asyncio.to_thread
    mock_to_thread = mocker.patch('services.asyncio.to_thread', new_callable=AsyncMock)

    mock_message = AsyncMock()
    mock_message.answer = AsyncMock()

    # Запуск тестируемой бизнес-логики
    await handle_brand_request('iphone', mock_message)

    # Проверка вывода уведомления пользователю и старта парсера в потоке
    mock_message.answer.assert_any_call('Собираю данные, пожалуйста, подождите...')
    assert mock_to_thread.called
