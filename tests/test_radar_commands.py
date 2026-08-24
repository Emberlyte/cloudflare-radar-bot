from unittest.mock import MagicMock
from aiogram_i18n import I18nContext

import pytest

from bot.handlers.radar_commands import (
    show_devices,
    show_locations,
    show_ases,
    show_quality,
    show_attacks_layer3,
    show_attacks_layer7,
    show_dns,
    show_email_threats,
    back_to_menu,
    ask_period_devices, show_top_services,
)

from service.cloudflare_radar import CloudflareRateLimitError


async def test_show_devices_success(mock_callback, mock_radar_client, mock_i18n):
    mock_callback.data = "period:devices:30d"
    mock_radar_client.summary_device_type.return_value = {
        "summary_0": {"desktop": "60.0", "mobile": "39.0", "other": "1.0"}
    }

    await show_devices(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.summary_device_type.assert_called_once_with(date_range="30d")
    mock_callback.message.edit_text.assert_called_once()
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "devices-title" in text_arg  # проверяем, что нужный ключ перевода использовался
    mock_callback.answer.assert_called_once()


async def test_show_devices_rate_limited(mock_callback, mock_radar_client, mock_i18n):
    mock_callback.data = "period:devices:30d"
    mock_radar_client.summary_device_type.side_effect = CloudflareRateLimitError("rate limited")

    await show_devices(mock_callback, mock_radar_client, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "error-rate-limited" in text_arg
    mock_callback.answer.assert_called_once()


async def test_show_devices_timeout(mock_callback, mock_radar_client, mock_i18n):
    mock_callback.data = "period:devices:30d"
    mock_radar_client.summary_device_type.side_effect = TimeoutError()

    await show_devices(mock_callback, mock_radar_client, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "error-timeout" in text_arg


async def test_show_devices_unexpected_error(mock_callback, mock_radar_client, mock_i18n):
    mock_callback.data = "period:devices:30d"
    mock_radar_client.summary_device_type.side_effect = ValueError("something broke")

    await show_devices(mock_callback, mock_radar_client, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "error-generic" in text_arg


async def test_ask_period_devices(mock_callback, mock_i18n):
    await ask_period_devices(mock_callback, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "period-ask-devices" in text_arg
    mock_callback.answer.assert_called_once()


async def test_show_attacks_layer3_success(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.attacks_layer3_summary.return_value = {
        "summary_0": {"UDP": "93.1", "TCP": "6.8", "GRE": "0.04", "ICMP": "0.02"}
    }

    await show_attacks_layer3(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.attacks_layer3_summary.assert_called_once()
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "UDP" in text_arg
    mock_callback.answer.assert_called_once()


async def test_show_attacks_layer7_success(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.attacks_layer7_summary.return_value = {
        "summary_0": {"GET": "81.1", "POST": "15.1"}
    }

    await show_attacks_layer7(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.attacks_layer7_summary.assert_called_once()
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "GET" in text_arg


async def test_show_dns_success(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.dns_by_protocol_summary.return_value = {
        "summary_0": {"UDP": "84.6", "TLS": "7.0", "HTTPS": "6.2", "TCP": "2.2"}
    }

    await show_dns(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.dns_by_protocol_summary.assert_called_once()
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "UDP" in text_arg


async def test_show_email_threats_success(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.email_threat_category_summary.return_value = {
        "summary_0": {"Link": "67.5", "Scam": "65.4"}
    }

    await show_email_threats(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.email_threat_category_summary.assert_called_once()
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "Link" in text_arg


async def test_show_attacks_layer3_rate_limited(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.attacks_layer3_summary.side_effect = CloudflareRateLimitError("rate limited")

    await show_attacks_layer3(mock_callback, mock_radar_client, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "Слишком много запросов" in text_arg



async def test_show_top_services_success(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.top_internet_services.return_value = {
        "top_0": [
            {"rank": 1, "service": "Google"},
            {"rank": 2, "service": "Facebook"},
        ]
    }

    await show_top_services(mock_callback, mock_radar_client, mock_i18n)

    mock_radar_client.top_internet_services.assert_called_once_with(limit=10)
    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "Google" in text_arg
    assert "Facebook" in text_arg
    mock_callback.answer.assert_called_once()


async def test_show_top_services_rate_limited(mock_callback, mock_radar_client, mock_i18n):
    mock_radar_client.top_internet_services.side_effect = CloudflareRateLimitError("rate limited")

    await show_top_services(mock_callback, mock_radar_client, mock_i18n)

    text_arg = mock_callback.message.edit_text.call_args[0][0]
    assert "Слишком много запросов" in text_arg