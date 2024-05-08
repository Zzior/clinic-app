import flet as ft

from src.components.components import c_text, c_text_field, c_elevated_button
from src.static.static_data import specialization_list

from src.components.navigation import admin_navigation_bar
from src.services.configuration import conf
from src.services.data_classes import AccessLevel


def admin_doctors_page(page: ft.Page):
    page.title = "Врачи"

    if page.session_id in conf.sessions and conf.sessions[page.session_id].access_level == AccessLevel.ADMIN:
        add_title = c_text(value="Добавить врача", size=18)
        name_f = c_text_field(label="Ф.И.О", icon=ft.icons.PERSON)
        office_number_f = c_text_field(label="Кабинет", icon=ft.icons.SENSOR_DOOR)
        specializations = [ft.dropdown.Option(s) for s in specialization_list]
        spec_dropdown = ft.Dropdown(
            options=list(specializations),
            label="Выберите направление",
            width=260
        )
        phone_f = c_text_field(hint_text="998223334455", label="Номер телефона", icon=ft.icons.PHONE)
        pass_f = c_text_field(label="Пароль", password=True, can_reveal_password=True, icon=ft.icons.KEY)

        del_title = c_text(value="Удалить врача", size=18)
        doctors = [ft.dropdown.Option(s.name) for s in conf.database.get_doctor()]
        doctors_dropdown = ft.Dropdown(
            options=list(doctors),
            label="Выберите врача"
        )
        add_error_info = c_text(value="", color="red", visible=False)
        del_error_info = c_text(value="Выберите врача", color="red", visible=False)

        def add_doctor(e: ft.ControlEvent):
            if name_f.value and spec_dropdown.value and office_number_f.value and phone_f.value and pass_f.value:
                status = conf.authentication.register_user(
                    access_level=AccessLevel.DOCTOR, login=phone_f.value, password=pass_f.value
                )
                if status:
                    conf.database.add_doctor(
                        name=name_f.value, specialization=spec_dropdown.value, office_number=office_number_f.value,
                        phone=phone_f.value
                    )

                    e.control.page.snack_bar = ft.SnackBar(ft.Text(f"Добавлен"))
                    e.control.page.snack_bar.open = True
                    doctors_dropdown.options = [ft.dropdown.Option(s.name) for s in conf.database.get_doctor()]

                    for variable in [name_f, spec_dropdown, office_number_f, phone_f, pass_f]:
                        variable.value = ""
                    page.update()

                else:
                    add_error_info.value = "Врач с таким телефоном существует"
                    add_error_info.visible = True
                    page.update()
            else:
                add_error_info.value = "Заполните поля"
                add_error_info.visible = True
                page.update()

        def del_doctor(e: ft.ControlEvent):
            if doctors_dropdown.value:
                doctors_dropdown.options = [ft.dropdown.Option(s.name) for s in conf.database.get_doctor()]
                doctors_dropdown.value = ""

                e.control.page.snack_bar = ft.SnackBar(ft.Text(f"Deleted"))
                e.control.page.snack_bar.open = True
                del_error_info.visible = False
                page.update()
            else:
                del_error_info.visible = True
                page.update()

        add_button = c_elevated_button(text="Добавить врача", width=200, on_click=add_doctor)
        del_button = c_elevated_button(text="Удалить врача", width=200, on_click=del_doctor)

        add_controls = ft.Column(
            controls=[
                add_title, name_f,
                ft.Row([ft.Icon(ft.icons.DIRECTIONS, color=ft.colors.GREY_800), spec_dropdown], spacing=16),
                office_number_f, phone_f, pass_f, add_error_info, add_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        del_controls = ft.Column(
            [del_title, doctors_dropdown, del_error_info, del_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        all_controls = ft.Column(
            controls=[ft.Row(
                [add_controls, del_controls],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=300,
                adaptive=True)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            adaptive=True
        )

    else:
        page.go("/")
        all_controls = c_text("Выполните вход")

    return ft.View(
        route="/admin/doctors",
        controls=[ft.Row([all_controls], alignment=ft.MainAxisAlignment.CENTER)],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        navigation_bar=admin_navigation_bar
    )

