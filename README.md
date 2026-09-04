
# Cloudflare Radar Bot

[![CI/CD](https://github.com/emberlyte/cloudflare-radar-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/emberlyte/cloudflare-radar-bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Telegram-бот, показывающий статистику интернет-трафика через [Cloudflare Radar API](https://radar.cloudflare.com/) — публичный сервис Cloudflare с агрегированными данными о трафике, атаках, DNS и качестве интернета по всему миру.


## Features

- 📱 **Устройства** — с каких устройств заходят в интернет (телефон, пк и тп)
- 🌍 **Топ локаций** — страны с наибольшим объёмом http-трафика
- 🌐 **Топ провайдеров** — крупнейшие интернет провайдеры
- ⚡ **Качество интернета** — глобальная скорость, задержка, потери пакетов
- 🛡 **Атаки и DDoS** — тренды по layer 3 и layer 7 атакам
- 🔤 **DNS по протоколу** — распределение DNS-запросов (udp,tcp,tls)
- 📧 **Email-угрозы** — топ категорий угроз в почтовом трафике
- 🏆 **Топ интернет-сервисов** — рейтинг популярности сервисов


## Tech Stack

- **Python 3.14**, [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- **[aiogram-i18n](https://github.com/aiogram/i18n)** + Fluent — локализация (RU/EN)
- **pytest** — тестирование
- **Redis** — кэширование ответов API и rate limiting
- **Docker / Docker Compose** — контейнеризация
- **GitHub Actions** — CI/CD (тесты → сборка образа → деплой)



## Requirements

- Docker и Docker Compose
- [uv](https://docs.astral.sh/uv/) (для запуска тестов вне контейнера)
- Токен Telegram-бота — получить у [@BotFather](https://t.me/BotFather)
- Токен Cloudflare Radar API — [инструкция](https://developers.cloudflare.com/radar/get-started/)
## Installation


```bash
git clone https://github.com/emberlyte/cloudflare-radar-bot.git
cd cloudflare-radar-bot
cp .env.example .env
# настрой .env (токен от cf, тг бота и домен(если есть))
docker compose up -d --build
```

Бот запустится в лонг-поллинг режиме, локально ничего дополнительно настраивать не нужно
    
## Environment Variables

| Переменная | Обязательна | Описание |
|---|---|---|
| `BOT_TOKEN` | ✅ | Токен Telegram-бота |
| `CF_TOKEN` | ✅ | Токен Cloudflare Radar API |
| `REDIS_URL` | — | По умолчанию `redis://redis:6379/0` |
| `BOT_MODE` | — | `polling` (по умолчанию) или `webhook` |
| `WEBHOOK_BASE_URL` | для webhook | Публичный домен бота |
## Running Tests


```bash
uv sync
uv run pytest -v
```


## Deployment


Бот поддерживает два режима:

- **Polling** — используется локально по умолчанию, не требует публичного домена
- **Webhook** — для продакшена, требует reverse proxy (nginx) с TLS-сертификатом

CI/CD настроен через GitHub Actions: пуш в `main` → тесты → сборка Docker-образа → публикация в GHCR → деплой на сервер по ssh


## License

[MIT](https://choosealicense.com/licenses/mit/)


