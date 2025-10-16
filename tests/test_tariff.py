
import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth_service import get_access_refresh_token

from models.tariff import TariffModel


def test_get_tarif(get_user):
    tariffs = []
    for i in range(5):
        tariff = TariffModel(
            name=f"Challenge_{i}",
            percent=i,
            description=f"Описание {i}"
        )
        is_ok, error = tariff.save()
        assert is_ok is True
        tariffs.append(tariff)

    user = get_user(phone='+79991234567', password='password', email='test@example.com')
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            '/tariff/get_tarif',
            headers={
                'Authorization': 'Bearer ' + access_token
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data == [
            dict(
                name=tariff.name,
                percent=tariff.percent,
                description=tariff.description,
            )
            for tariff in sorted(tariffs, key=lambda x: x.id)
        ]