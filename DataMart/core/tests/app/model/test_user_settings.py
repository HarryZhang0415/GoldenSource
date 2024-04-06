from datamart_core.app.model.credentials import Credentials
from datamart_core.app.model.defaults import Defaults
from datamart_core.app.model.preferences import Preferences
from datamart_core.app.model.profile import Profile
from datamart_core.app.model.user_settings import UserSettings


def test_user_settings():
    settings = UserSettings(
        credentials=Credentials(),
        profile=Profile(),
        preferences=Preferences(),
        defaults=Defaults(),
    )
    assert isinstance(settings, UserSettings)
