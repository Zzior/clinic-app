import flet as ft

from src.components.components import c_text_field, c_elevated_button, c_text
from src.static.static_data import clinic_name, about, phone, address
from src.services.configuration import conf


def profile(page: ft.Page):
    page.title = "MedSam"

    img = ft.Image(
        src="https://cdn.pixabay.com/photo/2023/07/30/09/34/partner-8158482_960_720.jpg",
        width=page.width * 0.3,
        height=page.height * 0.9,
        fit=ft.ImageFit.NONE,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(15)
    )

    if page.session_id in conf.sessions:
        profile_info = ft.Column()

    else:
        # global
        phone_filed = c_text_field(value="998", label="Номер телефона", icon=ft.icons.PHONE)
        password_filed = c_text_field(label="Пароль", password=True, can_reveal_password=True, icon=ft.icons.PASSWORD)
        confirm_button = c_elevated_button("Вход", width=140)
        error_info = c_text(value="", color="red", visible=False)

        # Reg
        name_filed = c_text_field(label="Ф.И.О.", visible=False, icon=ft.icons.PERSON)
        password_confirm_filed = c_text_field(
            label="Подтвердите пароль", password=True, visible=False, icon=ft.icons.PASSWORD
        )

        def change_mode(e: ft.ControlEvent = None):
            if mode.selected_index == 1:
                confirm_button.text = "Регистрация"
                name_filed.visible = True
                password_confirm_filed.visible = True
            else:
                confirm_button.text = "Вход"
                name_filed.visible = False
                password_confirm_filed.visible = False
            page.update()

        def register(e):
            valid = True

            if 5 > len(name_filed.value.split()) > 1:
                name_filed.border_color = ft.colors.GREEN
            else:
                name_filed.border_color = ft.colors.RED
                valid = False

            if len(phone_filed.value) == 12 and phone_filed.value.isdigit() and phone_filed.value.startswith("998"):
                phone_filed.border_color = ft.colors.GREEN
            else:
                phone_filed.border_color = ft.colors.RED
                valid = False

            if (len(password_filed.value) > 5) and (password_filed.value == password_confirm_filed.value):
                password_filed.border_color = ft.colors.GREEN
                password_confirm_filed.border_color = ft.colors.GREEN
            else:
                password_filed.border_color = ft.colors.RED
                password_confirm_filed.border_color = ft.colors.RED
                valid = False

            if valid:
                conf.database.add_patient(name=name_filed.value, phone=phone_filed.value)
                error_info.value = "Успешная регистрация"
                error_info.color = ft.colors.GREEN
            else:
                error_info.value = "Исправьте не валидные поля!"

            page.update()

        mode = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=change_mode,
            controls=[ft.Text("Вход"), ft.Text("Регистрация")],
            height=50,
            width=300
        )
        all_columns = ft.Column(
            controls=[
                c_text(clinic_name, size=20),
                mode,
                phone_filed,
                password_filed,
                password_confirm_filed,
                name_filed,
                confirm_button,
                error_info,
                c_text(about, size=14),
                c_text(phone, size=14),
                c_text(address, size=14)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            adaptive=True
        )

        page.add(
            ft.Row(controls=[all_columns, img], alignment=ft.MainAxisAlignment.SPACE_EVENLY, adaptive=True)
        )
        page.update()








