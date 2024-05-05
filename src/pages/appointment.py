import flet as ft

from src.components.components import c_text, c_text_field, c_elevated_button
from src.static.static_data import specialization_list


def appointment(page: ft.Page):
    page.title = "Регистрация"
    # page.theme_mode = ft.ThemeMode.LIGHT
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    name = c_text(value="F_name Name L_name", size=18)
    make_text = c_text(value="Записаться на приём", size=16)
    complaints_text = c_text_field(label="Жалоба", max_lines=6, multiline=True)
    send_button = c_elevated_button(text="Отправить запрос")

    specializations = [ft.dropdown.Option(s) for s in specialization_list]
    spec_dropdown = ft.Dropdown(
        options=list(specializations),
        label="Выберите направление"
    )

    make_appointment = ft.Column(
        controls=[name, make_text, complaints_text, spec_dropdown, send_button],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        adaptive=True
    )

    page.add(make_appointment)
    page.update()
