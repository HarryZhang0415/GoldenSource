"""Constants for the DataMart Market."""

from pathlib import Path

HOME_DIRECTORY = Path.home()
DATAMART_DIRECTORY = Path(HOME_DIRECTORY, ".datamart_platform")
USER_SETTINGS_PATH = Path(DATAMART_DIRECTORY, "user_settings.json")
SYSTEM_SETTINGS_PATH = Path(DATAMART_DIRECTORY, "system_settings.json")
