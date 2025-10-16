from datetime import datetime
from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth_service import get_access_refresh_token

from models.transaction import TransactionModel
from schemas.transaction import TransactionType


def test_get_transactions(get_user):
    transactions = []
    for i in range(5):
        transaction = TransactionModel(
            type=TransactionType.REFILL,
            amount=i,
            date=datetime.now()
        )
        is_ok, error = transaction.save()
        assert is_ok is True
        transactions.append(transaction)

    user = get_user(phone='+79991234567', password='password', email='test@example.com')
    access_token, refresh_token = get_access_refresh_token(user)
    with TestClient(app) as client:
        response = client.get(
            '/transaction/get_transactions',
            headers={
                'Authorization': 'Bearer ' + access_token
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data == [
            dict(
                id=ANY,
                type=transaction.type,
                amount=transaction.amount,
                date=transaction.date.isoformat(),
            )
            for transaction in sorted(transactions, key=lambda x: x.id)
        ]