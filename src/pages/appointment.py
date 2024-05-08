import flet as ft

from src.components.components import c_text, c_text_field, c_elevated_button
from src.static.static_data import specialization_list

from src.components.navigation import user_navigation_bar
from src.services.configuration import conf


def appointment_page(page: ft.Page):
    page.title = "Регистрация"

    if page.session_id in conf.sessions:
        info = conf.sessions[page.session_id]

        name = c_text(value=info.name, size=18)
        make_text = c_text(value="Записаться на приём", size=16)
        complaints_text = c_text_field(label="Жалоба", max_lines=6, multiline=True, width=400)
        specializations = [ft.dropdown.Option(s) for s in specialization_list]
        spec_dropdown = ft.Dropdown(
            options=list(specializations),
            label="Выберите направление",
            width=400
        )
        error_info = c_text(value="", color="red", visible=False)

        def send_appointment(e: ft.ControlEvent):
            if len(complaints_text.value) > 3 and spec_dropdown.value:
                conf.database.add_appointment(
                    patient_id=info.db_id, complaints=complaints_text.value, specialization=spec_dropdown.value
                )
                complaints_text.value = ""
                spec_dropdown.value = None
                error_info.visible = False
                page.go("/history")

            else:
                error_info.value = "Заполните поля"
                error_info.visible = True

        send_button = c_elevated_button(text="Отправить запрос", width=200, on_click=send_appointment)

        make_appointment = ft.Column(
            controls=[name, make_text, complaints_text, spec_dropdown, error_info, send_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            adaptive=True
        )

    else:
        page.go("/")
        make_appointment = c_text("Выполните вход")

    return ft.View(
        route="/appointment",
        controls=[ft.Row([make_appointment], alignment=ft.MainAxisAlignment.CENTER)],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        navigation_bar=user_navigation_bar
    )

