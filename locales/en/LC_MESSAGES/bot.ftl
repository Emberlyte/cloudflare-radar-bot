start-greeting = Hi! I show internet traffic statistics via Cloudflare Radar.

    Choose what to display:

menu-devices = 📱 Devices
menu-locations = 🌍 Top Locations
menu-ases = 🌐 Top Providers
menu-quality = ⚡ Internet Quality
menu-attacks = 🛡 Attacks & DDoS
menu-dns = 🔤 DNS by Protocol
menu-email = 📧 Email Threats
menu-services = 🏆 Top Internet Services
menu-back = ⬅️ Back
menu-choose = Choose what to display:

period-7d = 7 days
period-30d = 30 days
period-90d = 90 days
period-ask-devices = 📱 Show devices for which period?

devices-title = 📊 <b>Devices for { $period }</b>

devices-desktop = 🖥 Desktop: { $value }%
devices-mobile = 📱 Mobile: { $value }%
devices-other = ❓ Other: { $value }%

error-rate-limited = ⏳ Too many requests to Cloudflare. Try again in a minute.
error-timeout = ⏱ Cloudflare is taking too long. Try again.
error-generic = ⚠️ Couldn't fetch data. Try again later.

language-choose = 🌐 Choose language / Выбери язык:
language-changed = ✅ Language changed to English

period-ask-locations = 🌍 Show top locations for which period?
period-ask-ases = 🌐 Show top providers for which period?
period-back = ⬅️ Back

locations-title = 🌍 <b>Top locations for { $period }</b>

ases-title = 🌐 <b>Top providers for { $period }</b>

quality-title = ⚡ <b>Internet Quality (Global)</b>
quality-download = ⬇️ Download: { $value } Mbps
quality-upload = ⬆️ Upload: { $value } Mbps
quality-latency-idle = ⏱ Latency (idle): { $value } ms
quality-latency-loaded = ⏱ Latency (loaded): { $value } ms
quality-jitter-idle = 📶 Jitter (idle): { $value } ms
quality-jitter-loaded = 📶 Jitter (loaded): { $value } ms
quality-packet-loss = 📉 Packet loss: { $value }%

attacks-menu-title = 🛡 Which attack layer to show?
attacks-menu-layer3 = 🌐 Layer 3 (network)
attacks-menu-layer7 = 📡 Layer 7 (HTTP)

attacks-layer3-title = 🌐 <b>Layer 3 attacks — by protocol</b>
attacks-layer7-title = 📡 <b>Layer 7 attacks — by method</b>

dns-title = 🔤 <b>DNS queries by protocol</b>

email-title = 📧 <b>Top email threats for { $period }</b>
email-note = <i>One email may match multiple threat categories, so percentages can exceed 100%.</i>

services-title = 🏆 <b>Top Internet Services</b>

period-ask-email = 📧 Show email threats for which period?
period-ask-dns = 🔤 Show DNS queries for which period?

help-text = 📖 <b>How to use this bot</b>

    /start — open the main menu
    /help — this help message

    <b>Sections:</b>
    📱 <b>Devices</b> — what devices people use to browse (desktop/mobile)
    🌍 <b>Top Locations</b> — countries with the most HTTP traffic
    🌐 <b>Top Providers</b> — largest internet providers (ASes)
    ⚡ <b>Internet Quality</b> — global speed, latency, packet loss

    For sections with history, you can pick a period: 7, 30, or 90 days.

about-text = ℹ️ <b>About this bot</b>

    This bot shows internet traffic statistics via the Cloudflare Radar API — Cloudflare's public service with aggregated data on traffic, attacks, DNS, and internet quality worldwide.

    🔧 Stack: Python, aiogram 3, Redis, Docker
    📊 Data source: Cloudflare Radar (radar.cloudflare.com)
    📄 License: MIT
    Source code: github.com/emberlyte/cloudflare-radar-bot