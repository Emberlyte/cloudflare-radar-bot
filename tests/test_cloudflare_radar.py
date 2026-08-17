from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from service.cloudflare_radar import CloudflareRateLimitError

def make_mock_response(status: int, json_data: dict | None = None):
    mock_response = AsyncMock()
    mock_response.status = status
    if json_data is not None:
        mock_response.json = AsyncMock(return_value=json_data)

    mock_context = AsyncMock()
    mock_context.__aenter__.return_value = mock_response
    mock_context.__aexit__.return_value = None
    return mock_context


async def test_summary_device_type_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"desktop": "60.0", "mobile": "39.0", "other": "1.0"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.summary_device_type(date_range="30d")

    assert result["summary_0"]["desktop"] == "60.0"


async def test_summary_device_type_rate_limited(radar_client):
    mock_response = make_mock_response(status=429)

    with patch.object(radar_client._session, "get", return_value=mock_response):
        with pytest.raises(CloudflareRateLimitError):
            await radar_client.summary_device_type(date_range="30d")


async def test_summary_device_type_api_error(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={"success": False, "errors": [{"code": 1000, "message": "bad token"}]},
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="Radar API error"):
            await radar_client.summary_device_type(date_range="30d")


async def test_summary_device_type_uses_cache(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"desktop": "60.0", "mobile": "39.0", "other": "1.0"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response) as mock_get:
        await radar_client.summary_device_type(date_range="30d")
        result = await radar_client.summary_device_type(date_range="30d")

        mock_get.assert_called_once()

    assert result["summary_0"]["desktop"] == "60.0"


async def test_attacks_layer3_summary_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"UDP": "93.1", "TCP": "6.8", "GRE": "0.04", "ICMP": "0.02"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.attacks_layer3_summary()

    assert result["summary_0"]["UDP"] == "93.1"


async def test_attacks_layer7_summary_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"GET": "81.1", "POST": "15.1"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.attacks_layer7_summary()

    assert result["summary_0"]["GET"] == "81.1"


async def test_dns_by_protocol_summary_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"UDP": "84.6", "TLS": "7.0", "HTTPS": "6.2", "TCP": "2.2"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.dns_by_protocol_summary()

    assert result["summary_0"]["UDP"] == "84.6"


async def test_email_threat_category_summary_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {"summary_0": {"Link": "67.5", "Scam": "65.4"}},
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.email_threat_category_summary()

    assert result["summary_0"]["Link"] == "67.5"


async def test_top_internet_services_success(radar_client):
    mock_response = make_mock_response(
        status=200,
        json_data={
            "success": True,
            "errors": [],
            "result": {
                "top_0": [
                    {"rank": 1, "service": "Google"},
                    {"rank": 2, "service": "Facebook"},
                ]
            },
        },
    )

    with patch.object(radar_client._session, "get", return_value=mock_response):
        result = await radar_client.top_internet_services(limit=10)

    assert result["top_0"][0]["service"] == "Google"
    assert result["top_0"][1]["rank"] == 2