"""Test the container.py file."""

from datamart_core.app.command_runner import CommandRunner
from datamart_core.app.static.container import Container


def test_container_init():
    """Test container init."""
    container = Container(CommandRunner())
    assert container
