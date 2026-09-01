start-greeting = Привет! Я показываю статистику интернет-трафика через Cloudflare Radar.

    Выбери, что показать:

menu-devices = 📱 Устройства
menu-locations = 🌍 Топ локаций
menu-ases = 🌐 Топ провайдеров
menu-quality = ⚡ Качество интернета
menu-attacks = 🛡 Атаки и DDoS
menu-dns = 🔤 DNS по протоколу
menu-email = 📧 Email-угрозы
menu-services = 🏆 Топ интернет-сервисов
menu-back = ⬅️ Назад
menu-choose = Выбери, что показать:

period-7d = 7 дней
period-30d = 30 дней
period-90d = 90 дней
period-ask-devices = 📱 За какой период показать устройства?

devices-title = 📊 <b>Устройства за { $period }</b>

devices-desktop = 🖥 Десктоп: { $value }%
devices-mobile = 📱 Мобильные: { $value }%
devices-other = ❓ Другое: { $value }%

error-rate-limited = ⏳ Слишком много запросов к Cloudflare. Попробуй через минуту.
error-timeout = ⏱ Cloudflare долго отвечает. Попробуй ещё раз.
error-generic = ⚠️ Не удалось получить данные. Попробуй позже.

language-choose = 🌐 Выбери язык / Choose language:
language-changed = ✅ Язык изменён на русский

period-ask-locations = 🌍 За какой период показать топ локаций?
period-ask-ases = 🌐 За какой период показать топ провайдеров?
period-back = ⬅️ Назад

locations-title = 🌍 <b>Топ локаций за { $period }</b>

ases-title = 🌐 <b>Топ провайдеров за { $period }</b>

quality-title = ⚡ <b>Качество интернета (глобально)</b>
quality-download = ⬇️ Скачивание: { $value } Mbps
quality-upload = ⬆️ Отдача: { $value } Mbps
quality-latency-idle = ⏱ Задержка (простой): { $value } ms
quality-latency-loaded = ⏱ Задержка (под нагрузкой): { $value } ms
quality-jitter-idle = 📶 Джиттер (простой): { $value } ms
quality-jitter-loaded = 📶 Джиттер (под нагрузкой): { $value } ms
quality-packet-loss = 📉 Потеря пакетов: { $value }%

attacks-menu-title = 🛡 Какой уровень атак показать?
attacks-menu-layer3 = 🌐 Layer 3 (сетевой уровень)
attacks-menu-layer7 = 📡 Layer 7 (HTTP)

attacks-layer3-title = 🌐 <b>Layer 3 атаки — по протоколу</b>
attacks-layer7-title = 📡 <b>Layer 7 атаки — по методу</b>

dns-title = 🔤 <b>DNS-запросы по протоколу</b>

email-title = 📧 <b>Топ угроз в email за { $period }</b>
email-note = <i>Одно письмо может попадать сразу под несколько категорий, поэтому сумма процентов может превышать 100%.</i>

services-title = 🏆 <b>Топ интернет-сервисов</b>

period-ask-email = 📧 За какой период показать email-угрозы?
period-ask-dns = 🔤 За какой период показать DNS-запросы?

help-text = 📖 <b>Как пользоваться ботом</b>

    /start — открыть главное меню
    /help — эта справка

    <b>Разделы:</b>
    📱 <b>Устройства</b> — с каких устройств заходят в интернет (десктоп/мобильные)
    🌍 <b>Топ локаций</b> — страны с наибольшим объёмом HTTP-трафика
    🌐 <b>Топ провайдеров</b> — крупнейшие интернет-провайдеры (ASes)
    ⚡ <b>Качество интернета</b> — глобальная скорость, задержка, потери пакетов

    Для разделов с историей можно выбрать период: 7, 30 или 90 дней.

about-text = ℹ️ <b>О боте</b>

    Этот бот показывает статистику интернет-трафика через Cloudflare Radar API — публичный сервис Cloudflare с агрегированными данными о трафике, атаках, DNS и качестве интернета по всему миру.

    🔧 Технологии: Python, aiogram 3, Redis, Docker
    📊 Источник данных: Cloudflare Radar (radar.cloudflare.com)
    📄 Лицензия: MIT
    Исходный код: github.com/emberlyte/cloudflare-radar-bot

