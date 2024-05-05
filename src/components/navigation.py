import flet as ft

from src.pages.user_history import user_history
from src.pages.appointment import appointment
from src.pages.profile import profile

user_pages = [appointment, user_history, profile]


def navigate(e: ft.ControlEvent) -> None:
    page: ft.Page = e.page
    page.clean()
    user_pages[page.navigation_bar.selected_index](page=page)


def add_navigation_component(page: ft.Page) -> None:
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EDIT_NOTE),
            ft.NavigationDestination(icon=ft.icons.HISTORY),
            ft.NavigationDestination(icon=ft.icons.PERSON)
        ],
        on_change=navigate
    )

    page.update()

