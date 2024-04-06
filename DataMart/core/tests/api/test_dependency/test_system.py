"""Test the system module."""

import asyncio
from unittest.mock import MagicMock, patch

from datamart_core.api.dependency.system import (
    SystemSettings,
    get_system_settings,
)


@patch("datamart_core.api.dependency.system.SystemService")
def test_get_system_settings(mock_system_service):
    """Test get_system_settings."""
    mock_system_service.return_value.system_settings = SystemSettings()

    response = asyncio.run(get_system_settings(MagicMock(), mock_system_service))  # type: ignore[arg-type]

    assert response
