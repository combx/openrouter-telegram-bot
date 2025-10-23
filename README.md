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