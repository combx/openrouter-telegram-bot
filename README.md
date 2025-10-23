# Telegram Bot with OpenRouter.ai Integration

**English** | [**Русский**](#-c--openrouterai)

This is a multifunctional Telegram bot written in Python that integrates with the OpenRouter.ai API. It allows users to interact with various large language models for free, featuring a rich admin panel and persistent user data storage.

This project was developed with the assistance of an AI assistant and serves as an excellent example of a production-ready, modular Telegram bot.

## Features

- **Multi-language Support**: User interface in English and Russian.
- **Model Selection**: Users can choose from a list of available AI models on the fly.
- **Role Selection**: Users can assign a personality/role to the bot from a predefined list or set a custom one.
- **Chat Memory**: Option to enable/disable conversation history.
- **Streaming Responses**: Answers appear word by word for a better user experience.
- **Smart Edit Handling**: Editing the last message triggers a new, corrected response, and the old one is deleted.
- **Persistent Storage**: All user settings and conversation history are stored in an SQLite database, ensuring data is not lost on restart.
- **Rich Admin Panel**:
    - View bot usage statistics (`/stats`).
    - Check user information and recent history (`/userinfo`).
    - Ban/unban users (`/ban`, `/unban`).
    - Get paginated lists of all users (`/listusers`).
    - Receive real-time error notifications.
- **Modular Architecture**: The code is organized into logical modules (`handlers`, `shared`, `database`) for easy maintenance and scalability.
- **Deployment Ready**: Comes with instructions for running as a `systemd` service for reliability.

## Currently Available Models

This bot currently includes the following free models from OpenRouter.ai:

- `Meta Llama 3.3 8B`
- `OpenAI GPT-OSS 20B`
- `Nvidia Nemotron 9B`
- `Qwen3 235B`
- `DeepSeek Chimera R1T2`
- `GLM 4.5 Air`

**To change the list of models:**
1.  Open the `shared.py` file.
2.  Find the `AVAILABLE_MODELS` dictionary.
3.  Modify the list by adding, removing, or changing the model identifiers. The key is the user-facing name, and the value is the official API identifier from OpenRouter.

## Currently Available Roles

The bot supports the following predefined roles in both English and Russian:
- Helpful Assistant (Default)
- Python Expert
- Translator
- Marketer
- Storyteller
- Poet
- Chef

**To change the list of roles:**
1.  Open the `shared.py` file.
2.  Find the `AVAILABLE_ROLES` dictionary.
3.  Modify the list for the desired language (`ru` or `en`).

## Finding More Models on OpenRouter.ai

You can easily find and add more models to this bot.

1.  Go to the official models page: **[openrouter.ai/models](https://openrouter.ai/models)**.
2.  On this page, you can see a complete table of all available models. To find the model identifier needed for the code, look in the **"ID"** column.
3.  **Difference between free and paid models:**
    - **Free Models:** These models are marked with a price of **$0.00 / 1M tokens**. Using them does not require any funds on your OpenRouter account. They are often excellent open-source models.
    - **Paid Models:** These include powerful proprietary models like OpenAI's GPT-4o or Anthropic's Claude 3 Opus. Their price is listed per 1 million input and output tokens. To use them, you need to add credits to your OpenRouter account balance.

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/combx/openrouter-telegram-bot.git
    cd openrouter-telegram-bot
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory and fill it with your keys:
    ```env
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_TOKEN"
    OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"
    ADMIN_ID="YOUR_TELEGRAM_USER_ID"
    ```
    *(You can get your `ADMIN_ID` by messaging `@userinfobot` on Telegram)*

5.  **Run the bot:**
    ```bash
    python3 bot.py
    ```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to:
- **Open an Issue** to discuss what you would like to change.
- **Submit a Pull Request** with your proposed changes.

---

<br>

## Телеграм-бот с интеграцией OpenRouter.ai

[**English**](#telegram-bot-with-openrouterai-integration) | **Русский**

Это многофункциональный Телеграм-бот, написанный на Python и интегрированный с API OpenRouter.ai. Он позволяет пользователям бесплатно взаимодействовать с различными большими языковыми моделями, обладает богатой админ-панелью и сохраняет данные пользователей.

Этот проект был разработан при содействии ИИ-ассистента и служит прекрасным примером готового к работе модульного Телеграм-бота.

## Функционал

- **Мультиязычность**: Пользовательский интерфейс на русском и английском языках.
- **Выбор модели**: Пользователи могут на лету выбирать из списка доступных ИИ-моделей.
- **Выбор роли**: Пользователи могут назначить боту "личность"/роль из предопределенного списка или задать свою.
- **Память чата**: Возможность включать и отключать историю диалога.
- **Стриминг ответов**: Ответы появляются слово за словом для лучшего пользовательского опыта.
- **Умная обработка правок**: Редактирование последнего сообщения вызывает генерацию нового, исправленного ответа, а старый ответ удаляется.
- **Постоянное хранилище**: Все настройки пользователей и история переписки хранятся в базе данных SQLite, что гарантирует сохранность данных при перезапуске.
- **Богатая админ-панель**:
    - Просмотр статистики использования бота (`/stats`).
    - Просмотр информации о пользователе и его недавней истории (`/userinfo`).
    - Блокировка/разблокировка пользователей (`/ban`, `/unban`).
    - Получение списков всех пользователей с пагинацией (`/listusers`).
    - Получение уведомлений об ошибках в реальном времени.
- **Модульная архитектура**: Код организован в логические модули (`handlers`, `shared`, `database`) для простоты поддержки и масштабирования.
- **Готовность к развертыванию**: Включает инструкции для запуска в виде сервиса `systemd` для надежной работы.

## Доступные на данный момент модели

В данный момент бот включает в себя следующие бесплатные модели с OpenRouter.ai:

- `Meta Llama 3.3 8B`
- `OpenAI GPT-OSS 20B`
- `Nvidia Nemotron 9B`
- `Qwen3 235B`
- `DeepSeek Chimera R1T2`
- `GLM 4.5 Air`

**Чтобы изменить список моделей:**
1.  Откройте файл `shared.py`.
2.  Найдите словарь `AVAILABLE_MODELS`.
3.  Измените список, добавляя, удаляя или изменяя идентификаторы моделей. Ключ — это имя для пользователя, а значение — официальный идентификатор API с сайта OpenRouter.

## Доступные на данный момент роли

Бот поддерживает следующие предопределенные роли на русском и английском языках:
- Полезный ассистент (По умолчанию)
- Python-эксперт
- Переводчик
- Маркетолог
- Рассказчик
- Поэт
- Шеф-повар

**Чтобы изменить список ролей:**
1.  Откройте файл `shared.py`.
2.  Найдите словарь `AVAILABLE_ROLES`.
3.  Измените список для нужного языка (`ru` или `en`).

## Как найти другие модели на OpenRouter.ai

Вы можете легко находить и добавлять в бота новые модели.

1.  Перейдите на официальную страницу моделей: **[openrouter.ai/models](https://openrouter.ai/models)**.
2.  На этой странице вы увидите полную таблицу всех доступных моделей. Чтобы найти идентификатор модели для кода, смотрите в колонку **"ID"**.
3.  **Разница между бесплатными и платными моделями:**
    - **Бесплатные модели:** У этих моделей указана цена **$0.00 / 1M tokens**. Их использование не требует средств на вашем балансе OpenRouter. Часто это отличные open-source модели.
    - **Платные модели:** К ним относятся мощные проприетарные модели, такие как GPT-4o от OpenAI или Claude 3 Opus от Anthropic. Их цена указана за 1 миллион входных и выходных токенов. Для их использования необходимо пополнить баланс вашего аккаунта OpenRouter.

## Как запустить

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/combx/openrouter-telegram-bot.git
    cd openrouter-telegram-bot
    ```

2.  **Создайте виртуальное окружение (рекомендуется):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Создайте файл `.env`** в корневой директории и заполните его вашими ключами:
    ```env
    TELEGRAM_BOT_TOKEN="ВАШ_ТЕЛЕГРАМ_ТОКЕН"
    OPENROUTER_API_KEY="ВАШ_КЛЮЧ_OPENROUTER"
    ADMIN_ID="ВАШ_TELEGRAM_USER_ID"
    ```
    *(Вы можете получить ваш `ADMIN_ID`, написав боту `@userinfobot` в Telegram)*

5.  **Запустите бота:**
    ```bash
    python3 bot.py
    ```

## Участие в проекте

Я открыт для ваших идей и предложений! Если вы хотите улучшить проект или добавить новые функции, вы можете:
- **Создать Issue (задачу)**, чтобы обсудить то, что вы хотели бы изменить.
- **Отправить Pull Request (запрос на слияние)** с вашими изменениями.