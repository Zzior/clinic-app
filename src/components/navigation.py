import flet as ft

from src.services.data_classes import AccessLevel


user_pages = ["/appointment", "/history", "/"]
admin_pages = ["/admin/doctors", "/admin/appointment", "/"]


def user_navigate(e: ft.ControlEvent) -> None:
    e.page.go(user_pages[e.control.selected_index])


def admin_navigate(e: ft.ControlEvent) -> None:
    e.page.go(admin_pages[e.control.selected_index])


user_navigation_bar = ft.NavigationBar(
    destinations=[
        ft.NavigationDestination(icon=ft.icons.EDIT_NOTE),
        ft.NavigationDestination(icon=ft.icons.HISTORY),
        ft.NavigationDestination(icon=ft.icons.PERSON)
    ],
    on_change=user_navigate
)

admin_navigation_bar = ft.NavigationBar(
    destinations=[
        ft.NavigationDestination(icon=ft.icons.GROUP_ADD),
        ft.NavigationDestination(icon=ft.icons.HISTORY),
        ft.NavigationDestination(icon=ft.icons.PERSON)
    ],
    on_change=admin_navigate
)

