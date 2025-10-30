from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth_service import get_access_refresh_token


@pytest.mark.parametrize(
    "deposit",
    [
        None,
        -15,
        25,
        3.45,
    ],
)
def test_deposit(get_user, deposit):
    user = get_user(
        phone="+79991234567",
        password="password",
        email="test@example.com",
        deposit=deposit,
    )
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/user/get_balance", headers={"Authorization": "Bearer " + access_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert data == (deposit or 0)


@pytest.mark.parametrize(
    "amount",
    [
        None,
        pytest.param(-15, marks=pytest.mark.xfail()),
        25,
        3.45,
    ],
)
def test_top_up(get_user, amount):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.post(
            "/user/top_up",
            json={"amount": amount or 0},
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data is True


def test_get_profile(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/user/get_profile", headers={"Authorization": "Bearer " + access_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "id": ANY,
            "phone": "tel:+7-999-123-45-67",
            "email": "test@example.com",
            "name": None,
            "country": None,
            "telegram": None,
            "avatar_url": None,
            "tariff_status": "Стартовый",
            "deposit": None,
        }


def test_update_profile(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.post(
            "/user/update_profile",
            json={
                "country": "Russia",
            },
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "id": ANY,
            "phone": "tel:+7-999-123-45-67",
            "email": "test@example.com",
            "name": None,
            "country": "Russia",
            "telegram": None,
            "avatar_url": None,
            "tariff_status": "Стартовый",
            "deposit": None,
        }
