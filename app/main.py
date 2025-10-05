from nicegui import app as server_app
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

server_app.include_router(admin_router)
server_app.include_router(auth_router)
server_app.include_router(challenge_router)
server_app.include_router(notification_router)
server_app.include_router(referral_router)
server_app.include_router(tariff_router)
server_app.include_router(transaction_router)
server_app.include_router(user_router)
server_app.include_router(weight_router)

server_app.docs_url = "/docs"
server_app.openapi_url = "/api/v1/openapi.json"
server_app.setup()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        show=False,
        host="0.0.0.0",
    )
