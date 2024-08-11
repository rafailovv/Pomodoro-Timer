import flet as ft
import asyncio


def main(page: ft.Page):
    def set_session_time(e):
        hours, minutes = map(int, e.data.split(":"))
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)

        session_time_button.content.value = f"{hours_str}:{minutes_str}"
        session_time_button.update()


    page.window.width = 200 * 2
    page.window.height = 200 * 3
    page.window.resizable = False
    page.bgcolor = "#FFBB00"

    page.fonts = {
        "Lato" : "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
        "Nixie One": "https://github.com/google/fonts/raw/main/ofl/nixieone/NixieOne-Regular.ttf"
    }

    page.update()

    title = ft.SafeArea(
        ft.Text(
                "Pomodoro Timer!",
                width=page.width,
                color="#000000",
                size=30,
                text_align=ft.TextAlign.CENTER,
                font_family="Lato"))
    

    session_clock = ft.TimePicker(
        time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
        on_change=set_session_time)
    
    session_time_button = ft.TextButton(
        content=
            ft.Text(
                value="01:00",
                color="#000000",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One"),
        on_click=lambda _: page.open(session_clock))
    
    session_time_container = ft.Container(
        session_time_button,
        alignment=ft.alignment.center)

    page.add(title, session_time_container)


if __name__ == "__main__":
    ft.app(main)