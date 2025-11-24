from datetime import datetime, timedelta
from unittest.mock import ANY

from fastapi.testclient import TestClient

from main import app
from models.challenge import ChallengeModel
from services.auth_service import get_access_refresh_token


def test_create_challenge():
    challenge = ChallengeModel(
        title="Challenge",
        start=datetime.now(),
        end=datetime.now() + timedelta(days=7),
        prize="Автомобиль",
    )
    is_ok, error = challenge.save()
    assert is_ok is True


def test_get_challenges(get_user):
    challenges = []
    for i in range(5):
        challenge = ChallengeModel(
            title=f"Challenge_{i}",
            start=datetime.now(),
            end=datetime.now() + timedelta(days=7),
            prize=f"Автомобиль {i}",
        )
        is_ok, error = challenge.save()
        assert is_ok is True
        challenges.append(challenge)

    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            "/challenge/get_challenges",
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == [
            dict(
                id=ANY,
                title=challenge.title,
                start=challenge.start.isoformat(),
                end=challenge.end.isoformat(),
                prize=challenge.prize,
                joined=False,
            )
            for challenge in sorted(challenges, key=lambda x: x.id)
        ]


def test_challenge_join(get_user):
    user = get_user(phone="+79991234567", password="password", email="test@example.com")
    access_token, refresh_token = get_access_refresh_token(user)

    challenge = ChallengeModel(
        title="Challenge",
        start=datetime.now(),
        end=datetime.now() + timedelta(days=7),
        prize="Автомобиль",
    )
    challenge.save()

    with TestClient(app) as client:
        response = client.post(
            "/challenge/join",
            json={"challenge_id": challenge.id},
            headers={"Authorization": "Bearer " + access_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert data
        assert user in challenge.users
