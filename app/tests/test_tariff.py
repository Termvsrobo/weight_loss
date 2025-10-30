import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth_service import get_access_refresh_token

from models.tariff import TariffModel


@pytest.mark.parametrize(
    "tariff_data",
    [None, dict(name="Challenge_15", percent=2, description="Описание 15")],
)
def test_get_tarif(get_user, tariff_data):
    if tariff_data:
        tariff = TariffModel(**tariff_data)
        is_ok, error = tariff.save()
        assert is_ok is True
        user = get_user(
            phone="+79991234567",
            password="password",
            email="test@example.com",
            tariff_id=tariff.id,
        )
    else:
        user = get_user(
            phone="+79991234567", password="password", email="test@example.com"
        )
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/tariff/get_tarif", headers={"Authorization": "Bearer " + access_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert data == dict(
            name="Стартовый",
            percent=1,
            description="Стартовый тариф для новичков",
        )
