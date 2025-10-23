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

## Prerequisites: Getting Your Keys

Before you can run the bot, you need three secret keys.

### 1. Telegram Bot Token
1.  Open Telegram and search for the `@BotFather` bot.
2.  Send the `/newbot` command.
3.  Follow the instructions to give your bot a name and a username.
4.  BotFather will send you a token that looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`. **Save this token.**

### 2. OpenRouter API Key
1.  Go to **[openrouter.ai](https://openrouter.ai/)** and sign up for an account.
2.  Navigate to the **"Keys"** section in your account dashboard.
3.  Click **"Create Key"** and give it a name.
4.  OpenRouter will generate a key that starts with `sk-or-v1-...`. **Copy and save this key.**

#### Important Note on OpenRouter Rate Limits
OpenRouter has rate limits for free models:
-   **By default:** You are limited to **50 requests per day**.
-   **To increase the limit:** You need to add credits to your account. Adding at least **$10 in credits** increases your free request limit to **1,000 requests per day**. You do not need to spend these credits to use the free models; their presence on your balance is enough to lift the limit.

### 3. Your Admin User ID
To use the admin panel, the bot needs to know your personal Telegram User ID.
1.  Open Telegram and search for the `@userinfobot`.
2.  Send it the `/start` command.
3.  The bot will immediately reply with your User ID. **Save this number.**

## How to Run

1.  **Clone the repository:**
    ```bash
    # Replace YourUsername and repository-name with your actual data
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

4.  **Create a `.env` file** in the root directory and fill it with the keys you obtained:
    ```env
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_TOKEN"
    OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY"
    ADMIN_ID="YOUR_TELEGRAM_USER_ID"
    ```

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

## Подготовка: Получение ключей

Перед запуском бота вам понадобятся три секретных ключа.

### 1. Токен Telegram-бота
1.  Откройте Telegram и найдите бота `@BotFather`.
2.  Отправьте ему команду `/newbot`.
3.  Следуйте инструкциям, чтобы дать боту имя и юзернейм.
4.  BotFather пришлет вам токен. **Сохраните этот токен.**

### 2. API-ключ OpenRouter
1.  Перейдите на сайт **[openrouter.ai](https://openrouter.ai/)** и зарегистрируйтесь.
2.  В панели управления вашего аккаунта перейдите в раздел **"Keys"** (Ключи).
3.  Нажмите **"Create Key"** и дайте ключу имя.
4.  OpenRouter сгенерирует ключ, начинающийся с `sk-or-v1-...`. **Скопируйте и сохраните этот ключ.**

#### Важное замечание о лимитах OpenRouter
OpenRouter имеет ограничения на использование бесплатных моделей:
-   **По умолчанию:** Вы ограничены **50 запросами в день**.
-   **Чтобы увеличить лимит:** Вам необходимо пополнить баланс. Пополнение счета на сумму от **$10** увеличивает ваш лимит на бесплатные запросы до **1000 в день**. Вам не нужно тратить эти кредиты на бесплатные модели; их наличие на балансе достаточно для снятия ограничения.

### 3. ID администратора
Чтобы использовать админ-панель, боту нужно знать ваш личный ID в Telegram.
1.  Откройте Telegram и найдите бота `@userinfobot`.
2.  Отправьте ему команду `/start`.
3.  Бот немедленно ответит сообщением, в котором будет указан ваш User ID. **Сохраните это число.**

## Как запустить

1.  **Клонируйте репозиторий:**
    ```bash
    # Замените YourUsername и repository-name на ваши реальные данные
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

4.  **Создайте файл `.env`** в корневой директории и заполните его полученными ключами:
    ```env
    TELEGRAM_BOT_TOKEN="ВАШ_ТЕЛЕГРАМ_ТОКЕН"
    OPENROUTER_API_KEY="ВАШ_КЛЮЧ_OPENROUTER"
    ADMIN_ID="ВАШ_TELEGRAM_USER_ID"
    ```

5.  **Запустите бота:**
    ```bash
    python3 bot.py
    ```

## Участие в проекте

Я открыт для ваших идей и предложений! Если вы хотите улучшить проект или добавить новые функции, вы можете:
- **Создать Issue (задачу)**, чтобы обсудить то, что вы хотели бы изменить или если вы нашли ошибки.
- **Отправить Pull Request** с вашими изменениями если этих ошибок много.