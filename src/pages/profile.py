import flet as ft

from src.components.components import c_text_field, c_elevated_button, c_text
from src.static.static_data import clinic_name, about, phone, address
from src.services.configuration import conf

from src.services.data_classes import SessionInfo, AccessLevel
from src.components.navigation import navigation_bar


def profile_page(page: ft.Page) -> ft.View:
    page.title = "MedSam"
    result_controls = []

    img = ft.Image(
        src="https://cdn.pixabay.com/photo/2023/07/30/09/34/partner-8158482_960_720.jpg",
        width=page.width * 0.3,
        height=page.height * 0.9,
        fit=ft.ImageFit.NONE,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(15)
    )

    navigation_menu = None

    if page.session_id in conf.sessions:
        info = conf.sessions[page.session_id]

        def log_out(e):
            del conf.sessions[page.session_id]
            page.views.append(profile_page(page=page))
            page.update()

        authenticated_columns = ft.Column(
            controls=[
                c_text(clinic_name, size=20),
                ft.Row([ft.Icon(ft.icons.PERSON), ft.Text(info.name)]),
                ft.ElevatedButton(text="Выйти", on_click=log_out, icon=ft.icons.LOGOUT),
                c_text(about, size=14),
                c_text(phone, size=14),
                c_text(address, size=14)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            adaptive=True
        )

        result_controls.append(
            ft.Row(controls=[authenticated_columns, img], alignment=ft.MainAxisAlignment.SPACE_EVENLY, adaptive=True)
        )
        navigation_menu = navigation_bar

    else:
        # global
        phone_f = c_text_field(hint_text="998223334455", label="Номер телефона", icon=ft.icons.PHONE)
        pass_f = c_text_field(label="Пароль", password=True, can_reveal_password=True, icon=ft.icons.KEY)
        confirm_bt = c_elevated_button("Подтвердить", width=140, on_click=None)
        error_info = c_text(value="", color="red", visible=False)

        # Reg
        name_f = c_text_field(label="Ф.И.О.", visible=False, icon=ft.icons.PERSON)
        pass_confirm_f = c_text_field(
            label="Подтвердите пароль", password=True, visible=False, icon=ft.icons.KEY
        )

        def login(e):
            session_info: SessionInfo = conf.authentication.authenticate(login=phone_f.value, password=pass_f.value)
            if session_info is None:
                error_info.value = "Не верный телефон или пароль"
                error_info.visible = True
                page.update()

            elif session_info.access_level == AccessLevel.USER:
                user_info = conf.database.get_patient(phone=phone_f.value)
                session_info.db_id = user_info.id
                session_info.name = user_info.name
                page.go("/appointment")

            elif session_info.access_level == AccessLevel.DOCTOR:
                user_info = conf.database.get_doctor(phone=phone_f.value)
                session_info.db_id = user_info.id
                session_info.name = user_info.name
                page.go("/doctor")

            elif session_info.access_level == AccessLevel.ADMIN:
                page.go("/admin")

            if session_info:
                conf.sessions[page.session_id] = session_info

        def register(e):
            name_valid = 5 > len(name_f.value.split()) > 1
            phone_valid = len(phone_f.value) == 12 and phone_f.value.isdigit() and phone_f.value.startswith("998")
            password_valid = len(pass_f.value) > 5 and pass_f.value == pass_confirm_f.value

            name_f.border_color = ft.colors.GREEN if name_valid else ft.colors.RED
            phone_f.border_color = ft.colors.GREEN if phone_valid else ft.colors.RED
            pass_f.border_color = pass_confirm_f.border_color = ft.colors.GREEN if password_valid else ft.colors.RED

            if not (name_valid and phone_valid and password_valid):
                error_info.value = "Исправьте не валидные поля!"
                error_info.visible = True

            page.update()

            session_info = conf.authentication.register_user(
                access_level=AccessLevel.USER, login=phone_f.value, password=pass_f.value
            )
            if session_info:
                page.go("/appointment")
                conf.sessions[page.session_id] = session_info
                conf.database.add_patient(name=name_f.value, phone=phone_f.value)
                db_info = conf.database.get_patient(phone=phone_f.value)
                session_info.db_id = db_info.id
                session_info.name = db_info.name

            else:
                phone_f.color = ft.colors.RED
                error_info.value = "Пользователь с таким номером существует"
                error_info.visible = True
                page.update()

        def change_mode(e: ft.ControlEvent = None):
            if mode.selected_index == 1:
                confirm_bt.text = "Регистрация"
                confirm_bt.on_click = register
                name_f.visible = True
                pass_confirm_f.visible = True
            else:
                confirm_bt.text = "Вход"
                confirm_bt.on_click = login
                name_f.visible = False
                pass_confirm_f.visible = False
            page.update()

        mode = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=change_mode,
            controls=[ft.Text("Вход"), ft.Text("Регистрация")],
            height=50,
            width=265
        )
        all_columns = ft.Column(
            controls=[
                c_text(clinic_name, size=20),
                ft.Row([ft.Icon(ft.icons.SETTINGS_ETHERNET), mode]),
                phone_f,
                pass_f,
                pass_confirm_f,
                name_f,
                confirm_bt,
                error_info,
                c_text(about, size=14),
                c_text(phone, size=14),
                c_text(address, size=14)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            adaptive=True
        )

        result_controls.append(
            ft.Row(controls=[all_columns, img], alignment=ft.MainAxisAlignment.SPACE_EVENLY, adaptive=True)
        )
        change_mode()

    return ft.View(
        route="/",
        controls=result_controls,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        navigation_bar=navigation_menu
    )
