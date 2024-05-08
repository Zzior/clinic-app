import flet as ft

from src.components.components import c_text, c_text_field, c_elevated_button

from src.components.navigation import doctor_navigation_bar
from src.services.configuration import conf
from src.services.data_classes import AccessLevel


def doctor_accept_page(page: ft.Page):
    page.title = "Принять приём"

    if page.session_id in conf.sessions and conf.sessions[page.session_id].access_level == AccessLevel.DOCTOR:
        info = conf.sessions[page.session_id]
        accept_title = c_text(value="Принять на приём", size=18)
        doctor_spec = conf.database.get_doctor(phone=info.login).specialization
        spec_title = c_text(value=f"Cпециализация: {doctor_spec}", size=16)
        error_info = c_text(value="Заполните поля", color="red", visible=False)
        complaints_text = c_text_field(label="Жалоба", max_lines=6, multiline=True, read_only=True)
        diagnosis_f = c_text_field(label="Диагноз", max_lines=6, multiline=True)
        appointments_titles = []
        appointments_list = []

        def load_appointments():
            nonlocal appointments_titles
            nonlocal appointments_list
            appointments_titles = []

            appointments_list = conf.database.get_appointment(
                specialization=doctor_spec, diagnosis_filter="without_diagnosis"
            )
            for i in range(len(appointments_list)):
                p_name = conf.database.get_patient(p_id=appointments_list[i].patient_id).name
                appointments_titles.append(ft.dropdown.Option(f"{i + 1}. {p_name}"))

            page.update()

        load_appointments()

        def load_appointment(e):
            index = int(appointments_dropdown.value.split(".")[0]) - 1
            complaints = appointments_list[index].complaints
            complaints_text.value = complaints
            page.update()

        def save(e):
            index = int(appointments_dropdown.value.split(".")[0]) - 1
            if diagnosis_f.value and complaints_text.value:
                conf.database.update_diagnosis(
                    appointment_id=appointments_list[index].id, doctor_id=info.db_id, new_diagnosis=diagnosis_f.value
                )

                e.control.page.snack_bar = ft.SnackBar(ft.Text(f"Добавлен"))
                e.control.page.snack_bar.open = True

                for variable in [complaints_text, diagnosis_f, appointments_dropdown]:
                    variable.value = ""
                page.update()

                error_info.visible = False
                load_appointments()
            else:
                error_info.visible = True
                page.update()

        appointments_dropdown = ft.Dropdown(
            options=list(appointments_titles),
            label="Выберите",
            on_change=load_appointment
        )

        accept_button = c_elevated_button(text="Сохранить", width=200, on_click=save)

        all_controls = ft.Column(
            controls=[accept_title, spec_title, appointments_dropdown, complaints_text, diagnosis_f,
                      error_info, accept_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    else:
        page.go("/")
        all_controls = ft.Text("Выполните вход")

    return ft.View(
        route="/doctor/accept",
        controls=[ft.Row([all_controls], alignment=ft.MainAxisAlignment.CENTER)],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        navigation_bar=doctor_navigation_bar
    )

