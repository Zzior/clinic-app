import flet as ft

from components.navigation import user_pages


def main(page: ft.Page):
    page.theme_mode = "light"
    print(page.session_id)
    user_pages[2](page=page)


ft.app(target=main, view=ft.WEB_BROWSER)
