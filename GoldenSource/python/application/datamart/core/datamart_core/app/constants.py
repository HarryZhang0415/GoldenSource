"""Constants for the DataMart Market."""

from pathlib import Path
import os

HOME_DIRECTORY = Path(os.environ.get("PROJECT_BUILD_DIR"), "cfg")
DATAMART_DIRECTORY = Path(HOME_DIRECTORY, "datamart")
USER_SETTINGS_PATH = Path(DATAMART_DIRECTORY, "user_settings.json")
SYSTEM_SETTINGS_PATH = Path(DATAMART_DIRECTORY, "system_settings.json")
