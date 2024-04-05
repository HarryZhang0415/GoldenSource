"""Test custom errors."""

import pytest
from datamart_core.app.model.abstract.error import DataMartError
from datamart_core.provider.utils.errors import EmptyDataError


def function_that_raises_provider_error():
    """Raise a DataMartError."""
    raise DataMartError("An error occurred in the provider.")


def function_that_raises_empty_data_error():
    """Raise an EmptyDataError."""
    raise EmptyDataError()


def test_provider_error_is_raised():
    """Test if the DataMartError is raised."""
    with pytest.raises(DataMartError) as exc_info:
        function_that_raises_provider_error()
    assert str(exc_info.value) == "An error occurred in the provider."


def test_empty_data_error_is_raised():
    """Test if the EmptyDataError is raised."""
    with pytest.raises(EmptyDataError) as exc_info:
        function_that_raises_empty_data_error()
    assert (
        str(exc_info.value) == "No results found. Try adjusting the query parameters."
    )


def test_empty_data_error_custom_message():
    """Test if the EmptyDataError is raised with a custom message."""
    custom_message = "Custom message for no data."
    with pytest.raises(EmptyDataError) as exc_info:
        raise EmptyDataError(custom_message)
    assert str(exc_info.value) == custom_message
