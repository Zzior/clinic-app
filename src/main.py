from pathlib import Path
import flet as ft
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.pages import profile_page, appointment_page, history_page, admin_doctors_page, doctor_accept_page


pages = {
    "/": profile_page, "/appointment": appointment_page, "/history": history_page,
    "/admin/doctors": admin_doctors_page,
    "/doctor/accept": doctor_accept_page
}


def main(page: ft.Page):
    page.theme_mode = "light"

    def route_change(route):
        page.views.clear()
        if page.route in pages:
            page.views.append(pages[page.route](page=page))
        else:
            error_page = ft.View(
                route="/404",
                controls=[
                    ft.Text("404 Not Found", size=64),
                    ft.ElevatedButton(text="To main", on_click=lambda _: page.go("/"))
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            page.views.append(error_page)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
