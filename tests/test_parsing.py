import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException
from parsing import get_parsing

# Тестовая HTML-разметка страниц для BeautifulSoup
fake_html = """
<div class="catalog-item">
    <div class="catalog-item-title">
        <a href="/smartfon-samsung-s24">Samsung Galaxy S24</a>
    </div>
    <div class="catalog-item-price">2500 p.</div>
</div>
<div class="catalog-item">
    <div class="catalog-item-title">
        <a href="/smartfon-xiaomi-14">Xiaomi 14 Pro</a>
    </div>
    <div class="catalog-item-pricemini">1800 p.</div>
</div>
<div class="catalog-item">
    <div class="catalog-item-title">
        <a href="/unknown-phone">Nokia 3310</a>
    </div>
</div>
"""

@patch('parsing.webdriver.Chrome')
@patch('parsing.WebDriverWait')
def test_get_parsing_logic(mock_wait, mock_chrome, mocker):
    """Тест парсера: проверка инициализации Selenium, разбора HTML и фильтрации брендов"""

    # Настройка mock-браузера Selenium и перехват сохранения файлов
    mock_browser = MagicMock()
    mock_browser.page_source = fake_html
    mock_chrome.return_value = mock_browser
    mock_write_json = mocker.patch('parsing.write_json')

    # Ограничение цикла: симулируем отсутствие карточек на второй странице
    mock_wait.return_value.until.side_effect = [True, TimeoutException("No cards found")]

    # Запуск парсера
    get_parsing()

    # Проверка вызовов драйвера Selenium
    mock_chrome.assert_called_once()
    mock_browser.get.assert_any_call('https://www.777555.by/elektronika/telefoniya_i_svyaz/smartfony/page1/')
    assert mock_browser.quit.called

    # Валидация результатов парсинга BeautifulSoup
    assert mock_write_json.called
    captured_data = mock_write_json.call_args[0][0]

    # Проверка распределения товаров по брендам
    assert len(captured_data['samsung']) == 1
    assert captured_data['samsung'][0]['prod_name'] == 'Samsung Galaxy S24'
    assert captured_data['samsung'][0]['price'] == '2500 p.'

    assert len(captured_data['xiaomi']) == 1
    assert captured_data['xiaomi'][0]['discount_price'] == '1800 p.'

    # Проверка отсеивания нецелевых брендов
    assert len(captured_data['iphone']) == 0





