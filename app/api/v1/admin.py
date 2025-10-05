from pathlib import Path

from nicegui import APIRouter, ui


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.page("/", title="Admin")
async def admin_page():
    (ui.link("Фото/видео", "media"),)
    ui.link("Тарифы", "tariffs")
    ui.link("Статистика", "stats")
    ui.link("Пользователи", "users")


@router.page("/tariffs", title="Тарифы")
async def tariffs_page():
    with ui.dialog() as dialog, ui.card():
        (ui.input(label="Название", placeholder="Название тарифа"),)
        (ui.input(label="Цена", placeholder="Цена тарифа"),)
        (ui.input(label="Описание", placeholder="Описание тарифа"),)
        ui.button("Добавить", on_click=lambda: ui.notify("Тариф добавлен"))

    async def show_dialog():
        result = await dialog
        ui.notify(f"You chose {result}")

    ui.button("Добавить тариф", on_click=show_dialog)


@router.page("/media", title="Фото/видео")
async def media_page():
    for i in range(10):
        with ui.card():
            (ui.image(f"https://picsum.photos/seed/{i}/200/200"),)
            (ui.label(f"Фото {i}"),)
            ui.button("Удалить", on_click=lambda: ui.notify("Фото удалено"))


@router.page("/stats", title="Статистика")
async def stats_page():
    for i in range(10):
        with ui.card():
            ui.label(f"Пользователь {i} похудел на {10 - i} кг")


@router.page("/users", title="Пользователи")
async def users_page():
    for i in range(10):
        with ui.row():
            ui.label(f"Пользователь {i}")
