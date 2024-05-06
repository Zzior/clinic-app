import flet as ft

user_pages = ["/appointment", "/history", "/"]


def navigate(e: ft.ControlEvent) -> None:
    e.page.go(user_pages[e.control.selected_index])


navigation_bar = ft.NavigationBar(
    destinations=[
        ft.NavigationDestination(icon=ft.icons.EDIT_NOTE),
        ft.NavigationDestination(icon=ft.icons.HISTORY),
        ft.NavigationDestination(icon=ft.icons.PERSON)
    ],
    on_change=navigate
)

