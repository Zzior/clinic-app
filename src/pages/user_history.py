from flet import Page, Column, CrossAxisAlignment

from src.components.components import create_table, c_text


def user_history(page: Page):
    table = create_table(
        ["Врач", "Дата", "Направление", "Жалоба", "Диагноз"],
        [["Доктор Иванова", f"{i}.05.2024", "Терапия", "Боль в горле и слабость", "ОРВИ"] for i in range(20)]
    )
    table_info = Column(
        controls=[c_text("Последние приёмы", size=20), table],
        horizontal_alignment=CrossAxisAlignment.CENTER,
        adaptive=True)

    page.add(table_info)
