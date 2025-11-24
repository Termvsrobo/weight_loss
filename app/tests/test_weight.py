from datetime import datetime

from fastapi.testclient import TestClient

from main import app
from models.weight import WeightLogModel
from schemas.weight import WeightStatusType
from services.auth_service import get_access_refresh_token


def test_get_weights(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    weights = []
    for i in range(5):
        weight = WeightLogModel(
            status=WeightStatusType.PENDING,
            weight=i,
            date=datetime.now(),
            user_id=user.id,
        )
        is_ok, error = weight.save()
        assert is_ok is True
        weights.append(weight)

    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/weight/get_history", headers={"Authorization": "Bearer " + access_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert data == [
            dict(
                status=weight.status,
                weight=weight.weight,
                date=weight.date.isoformat(),
                media_url=None,
            )
            for weight in sorted(weights, key=lambda x: x.id)
        ]


def test_submit_weight(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.post(
            "/weight/submit_weight",
            json={
                "status": WeightStatusType.PENDING,
                "weight": 9.2,
                "date": datetime.now().isoformat(),
            },
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data
