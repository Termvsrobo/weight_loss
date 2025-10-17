from fastapi import FastAPI
from nicegui import app as nicegui_app
from nicegui import ui

from api.v1.admin import router as admin_router
from api.v1.auth import router as auth_router
from api.v1.challenge import router as challenge_router
from api.v1.notification import router as notification_router
from api.v1.referral import router as referral_router
from api.v1.tariff import router as tariff_router
from api.v1.transaction import router as transaction_router
from api.v1.user import router as user_router
from api.v1.weight import router as weight_router
from config import settings
from services.auth_service import JWTAuthenticationMiddleware

if settings.TEST_MODE:
    app = FastAPI()
else:
    nicegui_app.docs_url = "/docs"
    nicegui_app.openapi_url = "/api/v1/openapi.json"
    nicegui_app.setup()

    app = nicegui_app
    app.include_router(admin_router)

app.include_router(auth_router)
app.include_router(challenge_router)
app.include_router(notification_router)
app.include_router(referral_router)
app.include_router(tariff_router)
app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(weight_router)

app.add_middleware(
    JWTAuthenticationMiddleware,
    exclude_urls=[
        "/auth/register",
        "/auth/login",
        "/auth/send_sms_code",
        "/auth/verify_sms_code",
    ]
)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        show=False,
        host="0.0.0.0",
    )
