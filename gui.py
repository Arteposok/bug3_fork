import flet as ft
import main as rooms

apartment = rooms.Apartment()


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    # options :)
    themes = (
        "5C6BC0",
        "0288D1",
        "009688",
        "FFA000",
        "5C6BC0",
    )

    page.theme = ft.Theme(
        color_scheme_seed=themes[0],
        use_material3=True,
        font_family="JetBrains Mono",
    )
    page.adaptive = True
    page.window.width = 500
    page.window.height = 500
    page.update()
    room_name_entry = ft.TextField(
        label="Room name",
        border_radius=4,
        filled=True,
        border_width=0,
        content_padding=14,
        text_size=14,
    )
    width_entry = ft.TextField(
        label="Width",
        border_radius=4,
        filled=True,
        border_width=0,
        content_padding=14,
        text_size=14,
    )
    length_entry = ft.TextField(
        label="Length",
        border_radius=4,
        filled=True,
        border_width=0,
        content_padding=14,
        text_size=14,
    )
    height_entry = ft.TextField(
        label="Ceiling height",
        border_radius=4,
        filled=True,
        border_width=0,
        content_padding=14,
        text_size=14,
    )

    async def ex(*arg):
        global apartment
        apartment = rooms.Apartment()
        page.views.pop()
        page.update()

    async def checkout(*arg):
        wall_entry = ft.TextField(
            label="Wall cost per m^2",
            border_radius=4,
            filled=True,
            border_width=0,
            content_padding=16,
            text_size=14,
        )
        floor_entry = ft.TextField(
            label="Ceiling cost per m^2",
            border_radius=4,
            filled=True,
            border_width=0,
            content_padding=16,
            text_size=14,
        )
        ceiling_entry = ft.TextField(
            label="Ceiling cost per m^2",
            border_radius=4,
            filled=True,
            border_width=0,
            content_padding=16,
            text_size=14,
        )

        async def checkout_confirm(*arg):
            page.views.pop()
            wall_cost, ceiling_cost, floor_cost = map(
                float,
                (
                    str(wall_entry.value),
                    str(ceiling_entry.value),
                    str(floor_entry.value),
                ),
            )
            total_cost = apartment.calculate_total_cost(
                wall_cost, ceiling_cost, floor_cost
            )
            print(total_cost)
            rooms.checkout(apartment, total_cost, wall_cost, ceiling_cost, floor_cost)

            page.views.append(
                ft.View(
                    "/results",
                    (
                        ft.Column(
                            (
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Room name")),
                                        ft.DataColumn(ft.Text("Walls' area")),
                                        ft.DataColumn(ft.Text("Ceiling area")),
                                        ft.DataColumn(ft.Text("Floor area")),
                                    ],
                                    rows=[
                                        *[
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text(room.name)),
                                                    ft.DataCell(
                                                        ft.Text(
                                                            str(
                                                                room.calculate_wall_area()
                                                            )
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Text(
                                                            str(
                                                                room.calculate_ceiling_area()
                                                            )
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Text(
                                                            str(
                                                                room.calculate_floor_area()
                                                            )
                                                        )
                                                    ),
                                                ]
                                            )
                                            for room in apartment.rooms
                                        ],
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(ft.Text("Alltogether")),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(apartment.total_wall_area)
                                                    )
                                                ),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(
                                                            apartment.total_ceiling_area
                                                        )
                                                    )
                                                ),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(apartment.total_floor_area)
                                                    )
                                                ),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(ft.Text("Total cost")),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(
                                                            wall_cost
                                                            * apartment.total_wall_area
                                                        )
                                                    )
                                                ),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(
                                                            ceiling_cost
                                                            * apartment.total_ceiling_area
                                                        )
                                                    )
                                                ),
                                                ft.DataCell(
                                                    ft.Text(
                                                        str(
                                                            floor_cost
                                                            * apartment.total_floor_area
                                                        )
                                                    )
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                ft.FilledButton(
                                    text="exit",
                                    expand=True,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=4),
                                        padding=20,
                                    ),
                                    on_click=ex,
                                ),
                            )
                        ),
                    ),
                )
            )
            page.update()

        page.views.append(
            ft.View(
                "/costs",
                (
                    ft.Column(
                        (
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            wall_entry,
                                            floor_entry,
                                            ceiling_entry,
                                        ],
                                        spacing=20,
                                    ),
                                    padding=20,
                                ),
                                elevation=4,
                                shape=ft.RoundedRectangleBorder(radius=4),
                                margin=ft.margin.symmetric(vertical=10),
                            ),
                            ft.FilledButton(
                                text="confirm",
                                expand=True,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=4),
                                    padding=20,
                                ),
                                on_click=checkout_confirm,
                            ),
                        )
                    ),
                ),
            ),
        )
        page.update()

    async def add_room(*arg):
        nonlocal room_name_entry, length_entry, width_entry, height_entry
        name = str(room_name_entry.value)
        length, width, height = map(
            float,
            [
                str(length_entry.value),
                str(width_entry.value),
                str(height_entry.value),
            ],
        )
        room_name_entry.value = ""
        length_entry.value = ""
        width_entry.value = ""
        height_entry.value = ""
        room = rooms.Room(
            name=name,
            length=length,
            width=width,
            height=height,
        )
        apartment.add_room(room=room)
        page.update()

    page.views.append(
        ft.View(
            "/home",
            (
                ft.Container(
                    ft.Column(
                        (
                            ft.Text(
                                "Welcome",
                                size=50,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Room Finishing Cost Calculator",
                                size=25,
                            ),
                            ft.FilledButton(
                                text="Start",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=4),
                                    padding=20,
                                ),
                                on_click=ex,
                            ),
                        ),
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ),
        )
    )
    page.add(
        ft.Column(
            (
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                room_name_entry,
                                width_entry,
                                length_entry,
                                height_entry,
                            ],
                            spacing=20,
                        ),
                        padding=20,
                    ),
                    elevation=4,
                    shape=ft.RoundedRectangleBorder(radius=4),
                    margin=ft.margin.symmetric(vertical=10),
                ),
                ft.FilledTonalButton(
                    text="add room",
                    expand=True,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=4),
                        padding=20,
                    ),
                    on_click=add_room,
                ),
                ft.FilledButton(
                    text="checkout",
                    expand=True,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=4),
                        padding=20,
                    ),
                    on_click=checkout,
                ),
            ),
            expand=True,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )


if __name__ == "__main__":
    ft.app(main)
