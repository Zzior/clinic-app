import flet as ft

from src.components.components import create_table, c_text
from src.components.navigation import user_navigation_bar, doctor_navigation_bar
from src.services.data_classes import AccessLevel

from src.services.configuration import conf


def history_page(page: ft.Page):
    page.title = "История приёмов"
    if page.session_id in conf.sessions:
        info = conf.sessions[page.session_id]
        if info.access_level == AccessLevel.USER:
            navigation_bar = user_navigation_bar
            appointments = conf.database.get_appointment(patient_id=info.db_id)
            list_appointments = [
                [conf.database.get_doctor(doctor_id=i.doctor_id).name if i.doctor_id else "Не назначен",
                 i.appointment_time.strftime('%Y.%m.%d'), i.specialization, i.complaints,
                 i.diagnosis if i.diagnosis else "Не назначен"] for i in appointments[-10:]
            ]

            table = create_table(
                ["Врач", "Дата", "Направление", "Жалоба", "Диагноз"], list_appointments
            )
        else:
            navigation_bar = doctor_navigation_bar
            appointments = conf.database.get_appointment(doctor_id=info.db_id)
            list_appointments = [
                [conf.database.get_patient(p_id=i.patient_id).name, i.appointment_time.strftime('%Y.%m.%d'),
                 i.complaints, i.diagnosis] for i in appointments[-10:]
            ]

            table = create_table(
                ["Пациент", "Дата", "Жалоба", "Выставленный диагноз"], list_appointments
            )

        table_info = ft.Column(
            controls=[c_text("Последние приёмы", size=20), table],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            adaptive=True)

        return ft.View(
            route="/history",
            controls=[ft.Row([table_info], alignment=ft.MainAxisAlignment.CENTER)],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            navigation_bar=navigation_bar
        )

    else:
        page.go("/")
        return ft.View(
            route="/history",
            controls=[],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            navigation_bar=user_navigation_bar
        )
