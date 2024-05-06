import flet as ft

from src.components.components import c_text, c_text_field, c_elevated_button
from src.static.static_data import specialization_list

from src.components.navigation import navigation_bar
from src.services.configuration import conf


def appointment_page(page: ft.Page):
    page.title = "Регистрация"

    if page.session_id in conf.sessions:
        info = conf.sessions[page.session_id]

        name = c_text(value=info.name, size=18)
        make_text = c_text(value="Записаться на приём", size=16)
        complaints_text = c_text_field(label="Жалоба", max_lines=6, multiline=True, width=400)
        send_button = c_elevated_button(text="Отправить запрос", width=200)

        specializations = [ft.dropdown.Option(s) for s in specialization_list]
        spec_dropdown = ft.Dropdown(
            options=list(specializations),
            label="Выберите направление",
            width=400
        )

        make_appointment = ft.Column(
            controls=[name, make_text, complaints_text, spec_dropdown, send_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            adaptive=True
        )

    else:
        page.go("/")
        make_appointment = ft.Text("Выполните вход")

    return ft.View(
        route="/appointment",
        controls=[ft.Row([make_appointment], alignment=ft.MainAxisAlignment.CENTER)],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        navigation_bar=navigation_bar
    )

