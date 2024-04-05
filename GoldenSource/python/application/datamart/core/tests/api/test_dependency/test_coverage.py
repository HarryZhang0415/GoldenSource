"""Test the coverate module."""

import asyncio
from unittest.mock import MagicMock

from datamart_core.api.dependency.coverage import get_command_map


def test_get_system_settings():
    """Test get_system_settings."""

    response = asyncio.run(get_command_map(MagicMock()))  # type: ignore[arg-type]

    assert response
