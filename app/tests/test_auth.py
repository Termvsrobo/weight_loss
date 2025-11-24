from unittest.mock import ANY

from fastapi.testclient import TestClient

from config import settings
from main import app
from schemas.auth import AccessToken
from services.auth_service import access_security, get_subject, refresh_security


def test_register_user():
    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "phone": "+79991234567",
                "password": "password",
                "email": "test@example.com",
            },
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


def test_login(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    subject = get_subject(user)
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "phone": "+79991234567",
                "password": "password",
            },
        )
        assert response.status_code == 200
        data = response.json()
        AccessToken.model_validate(data)
        access_data = access_security.jwt_backend.decode(
            data["access_token"], settings.SECRET_KEY
        )
        refresh_data = refresh_security.jwt_backend.decode(
            data["refresh_token"], settings.SECRET_KEY
        )
        assert access_data["subject"] == subject
        assert refresh_data["subject"] == subject


def test_refresh_token(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    subject = get_subject(user)
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "phone": "+79991234567",
                "password": "password",
            },
        )
        assert response.status_code == 200
        data = response.json()
        AccessToken.model_validate(data)
        access_data = access_security.jwt_backend.decode(
            data["access_token"], settings.SECRET_KEY
        )
        refresh_data = refresh_security.jwt_backend.decode(
            data["refresh_token"], settings.SECRET_KEY
        )
        assert access_data["subject"] == subject
        assert refresh_data["subject"] == subject

        response_refresh = client.post(
            "/auth/refresh_token",
            data={"refresh_token": data["refresh_token"]},
        )
        assert response_refresh.status_code == 200
        data_refresh = response_refresh.json()
        AccessToken.model_validate(data_refresh)
        access_data = access_security.jwt_backend.decode(
            data_refresh["access_token"], settings.SECRET_KEY
        )
        refresh_data = refresh_security.jwt_backend.decode(
            data_refresh["refresh_token"], settings.SECRET_KEY
        )
        assert access_data["subject"] == subject
        assert refresh_data["subject"] == subject
