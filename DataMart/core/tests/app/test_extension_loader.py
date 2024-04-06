"""Tests for the ExtensionLoader class."""

from unittest.mock import patch

import pytest
from datamart_core.app.extension_loader import EntryPoint, ExtensionLoader, DataMartGroups


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Fixture to run before and after each test function.

    This is necessary to reset the singleton instance of ExtensionLoader.
    """
    # Code to run before each test function
    yield  # This is where the test function runs
    # Code to run after each test function
    # pylint: disable=protected-access
    ExtensionLoader._instances = {}


def test_extension_loader():
    """Smoke test for extension loader."""
    extension_loader = ExtensionLoader()
    assert extension_loader is not None


def test_extension_loader_singleton_prop():
    """Test the singleton property of extension loader."""
    extension_loader = ExtensionLoader()
    extension_loader2 = ExtensionLoader()
    assert extension_loader is extension_loader2


def test_datamart_groups():
    """Test the DataMartGroups enum."""
    assert len(DataMartGroups) == 3
    assert DataMartGroups.core.value == "datamart_core_extension"
    assert DataMartGroups.provider.value == "datamart_provider_extension"
    assert DataMartGroups.obbject.value == "datamart_obbject_extension"


def test_obbject_entry_points():
    """Test the obbject entry points property."""
    el = ExtensionLoader()
    assert isinstance(el.obbject_entry_points, list)

    for ep in el.obbject_entry_points:
        assert ep.group == DataMartGroups.obbject.value


def test_core_entry_points():
    """Test the core entry points property."""
    el = ExtensionLoader()
    assert isinstance(el.core_entry_points, list)
    for ep in el.core_entry_points:
        assert ep.group == DataMartGroups.core.value


def test_provider_entry_points():
    """Test the provider entry points property."""
    el = ExtensionLoader()
    assert isinstance(el.provider_entry_points, list)
    for ep in el.provider_entry_points:
        assert ep.group == DataMartGroups.provider.value


def test_sorted_entry_points():
    """Test the _sorted_entry_points method."""
    # pylint: disable=protected-access
    core_entry_points = ExtensionLoader._sorted_entry_points(DataMartGroups.core.value)
    for ep in core_entry_points:
        assert ep.group == DataMartGroups.core.value


def test_get_entry_point():
    """Test the _get_entry_point method."""
    el = ExtensionLoader()
    # pylint: disable=protected-access
    result = el._get_entry_point(el.provider_entry_points, "fmp")
    if result:
        assert result.group == DataMartGroups.provider.value
        assert result.name == "fmp"

    # pylint: disable=protected-access
    result = el._get_entry_point(el.core_entry_points, "equity")
    if result:
        assert result.group == DataMartGroups.core.value
        assert result.name == "equity"


def test_get_entry_point_not_found():
    """Test the _get_entry_point method when the extension is not found."""
    el = ExtensionLoader()
    # pylint: disable=protected-access
    result = el._get_entry_point(el.core_entry_points, "random_extension")
    assert result is None


@patch("datamart_core.app.extension_loader.ExtensionLoader._get_entry_point")
def test_get_obbject_entry_point(mock_get_entry_point):
    """Test the get_obbject_entry_point method."""

    mock_get_entry_point.return_value = EntryPoint(
        name="mock_extension", group=DataMartGroups.obbject.value, value="mock"
    )

    el = ExtensionLoader()
    result = el.get_obbject_entry_point("mock_extension")
    if result:
        assert result.group == DataMartGroups.obbject.value
        assert result.name == "mock_extension"


@patch("datamart_core.app.extension_loader.ExtensionLoader._get_entry_point")
def test_get_entry_point_core(mock_get_entry_point):
    """Test the get_core_entry_point method."""

    mock_get_entry_point.return_value = EntryPoint(
        name="mock_extension", group=DataMartGroups.obbject.value, value="mock"
    )

    el = ExtensionLoader()
    result = el.get_core_entry_point("mock_extension")
    if result:
        assert result.group == DataMartGroups.obbject.value
        assert result.name == "mock_extension"


@patch("datamart_core.app.extension_loader.ExtensionLoader._get_entry_point")
def test_get_entry_point_provider(mock_get_entry_point):
    """Test the get_core_entry_point method."""

    mock_get_entry_point.return_value = EntryPoint(
        name="mock_extension", group=DataMartGroups.obbject.value, value="mock"
    )

    el = ExtensionLoader()
    result = el.get_provider_entry_point("mock_extension")
    if result:
        assert result.group == DataMartGroups.obbject.value
        assert result.name == "mock_extension"


def test_obbject_objects():
    """Test the obbject objects property."""
    # pylint: disable=import-outside-toplevel
    from datamart_core.app.model.extension import Extension

    el = ExtensionLoader()
    assert isinstance(el.obbject_objects, dict)

    for key, value in el.obbject_objects.items():
        assert isinstance(key, str)
        assert isinstance(value, Extension)


def test_core_objects():
    """Test the core objects property."""
    # pylint: disable=import-outside-toplevel
    from datamart_core.app.router import Router

    el = ExtensionLoader()
    assert isinstance(el.core_objects, dict)

    for key, value in el.core_objects.items():
        assert isinstance(key, str)
        assert isinstance(value, Router)


def test_provider_objects():
    """Test the provider objects property."""
    # pylint: disable=import-outside-toplevel
    from datamart_core.provider.abstract.provider import Provider

    el = ExtensionLoader()
    assert isinstance(el.provider_objects, dict)

    for key, value in el.provider_objects.items():
        assert isinstance(key, str)
        assert isinstance(value, Provider)
