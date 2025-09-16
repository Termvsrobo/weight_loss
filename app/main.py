import uvicorn
from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.challenge import router as challenge_router
from app.api.v1.notification import router as notification_router
from app.api.v1.referral import router as referral_router
from app.api.v1.tariff import router as tariff_router
from app.api.v1.transaction import router as transaction_router
from app.api.v1.user import router as user_router
from app.api.v1.weight import router as weight_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(challenge_router)
app.include_router(notification_router)
app.include_router(referral_router)
app.include_router(tariff_router)
app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(weight_router)


if __name__ == "__main__":
    uvicorn.run()
