import pytest
from fastapi.testclient import TestClient

from main import app
from models.notification import PreferenceModel
from services.auth_service import get_access_refresh_token


def test_get_notifications(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")

    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/notification/get_preferences",
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "motivation": False,
            "reminders": False,
            "accruals": False,
        }


@pytest.mark.parametrize(
    "motivation,reminders,accruals",
    [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True),
        (True, False, False),
        (True, False, True),
        (True, True, False),
        (True, True, True),
    ],
)
def test_set_notifications(get_user, motivation, reminders, accruals):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.post(
            "/notification/set_preferences",
            json={
                "motivation": motivation,
                "reminders": reminders,
                "accruals": accruals,
            },
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "motivation": motivation,
            "reminders": reminders,
            "accruals": accruals,
        }
        assert PreferenceModel.exists(user_id=user.id)
