import flet as ft


text_args = {"size": 14}
filed_args = {"border_color": ft.colors.BLUE, "adaptive": True}
e_button_args = {"color": ft.colors.BLUE}


def c_text(value="change", **kwargs) -> ft.Text:
    return ft.Text(value, **{**text_args, **kwargs})


def c_text_field(label: str = "", **kwargs) -> ft.TextField:
    return ft.TextField(label=label, **{**filed_args, **kwargs})


def c_elevated_button(text: str = "", **kwargs) -> ft.ElevatedButton:
    return ft.ElevatedButton(text=text, **{**e_button_args, **kwargs})


def create_table(titles: list, datas: list[list]) -> ft.DataTable:
    columns = []
    rows = []

    # Create columns with appropriate data types and set width
    for title in titles:
        if isinstance(title, (int, float)):
            columns.append(ft.DataColumn(ft.Text(str(title)), numeric=True))
        else:
            columns.append(ft.DataColumn(ft.Text(title)))

    # Create rows with limited cell content
    for data in datas[-10:]:
        cells = []
        for item in data:
            cell_text = ft.Text(str(item)[:30] + "..." if len(str(item)) > 30 else str(item))
            cells.append(ft.DataCell(cell_text))
        rows.append(ft.DataRow(cells=cells))

    # Create DataTable with border, paging, and styling
    return ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, ft.colors.BLACK),  # Add border around the table
        # paging=ft.DataTablePagination(page_size=10),  # Enable paging with 10 rows per page
        heading_row_color=ft.colors.BLUE_GREY_100,  # Style the heading row
    )
