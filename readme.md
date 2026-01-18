# Телеграм-бот Bot_parser
Telegram-бот, который парсит данные с динамического сайта. Проект создан в учебных целях для самостоятельного изучения.

### ⚙️Технологии:

- Python + библиотека **Aiogram**
- **Selenium** — автоматизация браузера
- **BeautifulSoup** — извлечение данных из HTML
- **JSON** — сохранение результатов парсинга

### 🚀 Функциональность

- Получение списка товаров из интернет-магазина по выбранной категории
- Парсинг данных с динамического сайта (с JavaScript-контентом)
- Кэширование данных в JSON-файл для ускорения повторных запросов
- Удобный интерфейс через Telegram-бота

### 🖼 Скриншоты

| Интерфейс бота | Пример парсинга |
|:--:|:--:|
| ![Parser](https://github.com/Oksana-Bachish/telegram-parser-bot/blob/main/png_for_readme/parser_bot.png) | ![Parser_bot](https://github.com/Oksana-Bachish/telegram-parser-bot/blob/main/png_for_readme/parsing_bot.png) |

### 🛠 Установка и запуск

Перед началом убедитесь, что у вас установлен браузер **Google Chrome**.

1. Откройте терминал и перейдите в нужную директорию:
   ```bash
   cd <имя_папки>
   ```

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Oksana-Bachish/telegram-parser-bot.git
   ```

3. Перейдите в директорию проекта:
   ```bash
   cd telegram-parser-bot
   ```

4. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

5. Активируйте окружение:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

6. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

7. Создайте Telegram-бота через [@BotFather](https://t.me/BotFather) и получите токен.

8. Создайте файл `.env` в корне проекта:
   ```bash
   touch .env
   ```

9. Добавьте в `.env`:
   ```env
   TOKEN=your_token
   ```

10. Запустите бота:
    ```bash
    python bot.py
    ```

Бот готов к работе. Откройте Telegram и начните общение с ботом.

### 👩‍💻 Автор:
*Оксана Бачиш*  
https://github.com/Oksana-Bachish?tab=repositories
