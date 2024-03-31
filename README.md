# Телеграм бота для автоматической посещаемости в университете ЛЭТИ

### Description
Простой асинхронный телеграм бот, который предоставляет возможность пользователям авторизоваться в личном кабинете и перестать беспокоиться о электронной посещаемости на парах.
### Технологии
- python 3.12
- selenium *для взаимодействия с личным кабинетом ЛЭТИ*
- aiogram *для взаимодействия с Telegram Bot API*
- psycopg3 *для взаимодействия с базой данных*
- docker *для запуска*
### Внести вклад в разработку
#### Зависимости
- docker 23 и выше
#### Шаги установки
1. делаем fork репозитория
2. клонируем репозиторий
3. создаем `.env` файл внутри *app* директории
  устанавливаем следующие переменные окружения:
  - CELERY_BROKER_URL
  - CELERY_RESULT_BACKEND
  - BOT_TOKEN
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
  - POSTGRES_PORT
4. в основной директории `docker compose --env-file ./app/.env up -d --build`
5. создаем Pull Request в мой репозиторий

**Удачи!**

MIT License

Copyright (c) [2024] [Michael Sitnikov]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
