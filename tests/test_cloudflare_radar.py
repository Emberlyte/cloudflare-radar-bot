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