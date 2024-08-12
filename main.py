import flet as ft
import asyncio


def main(page: ft.Page):
    def set_session_time(e):
        hours, minutes = map(int, e.data.split(":"))
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)

        session_time_button.content.value = f"{hours_str}:{minutes_str}"
        session_time_button.update()
    

    def set_rest_time(e):
        hours, minutes = map(int, e.data.split(":"))
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)

        rest_time_button.content.value = f"{hours_str}:{minutes_str}"
        rest_time_button.update()

    page.title = "Pomodoro Timer"
    page.bgcolor = "#FFBB00"
    page.window.width = 200 * 2
    page.window.height = 200 * 3
    page.window.resizable = False
    page.window.icon = f"/img/favicon.ico"
    page.window.wait_until_ready_to_show = True

    page.fonts = {
        "Lato" : f"/fonts/Lato-Regular.ttf",
        "Nixie One": f"/fonts/NixieOne-Regular.ttf"
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
    

    pomodoro_img = ft.Image(
        width=300,
        height=300,
        src=f"/img/Pomodoro.png")
    
    pomodoro_img_container = ft.Container(
        content=pomodoro_img,
        alignment=ft.alignment.center)
    
    session_clock = ft.TimePicker(
        value="00:25",
        time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
        on_change=set_session_time)
    
    session_time_button = ft.TextButton(
        content=
            ft.Text(
                value="00:25",
                color="#000000",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One"),
        on_click=lambda _: page.open(session_clock))
    
    session_time_container = ft.Container(
        session_time_button,
        alignment=ft.alignment.center)
    
    rest_clock = ft.TimePicker(
        value="00:05",
        time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
        on_change=set_rest_time)

    rest_time_button = ft.TextButton(
        content=
            ft.Text(
                value="00:05",
                color="#000000",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One"),
        on_click=lambda _: page.open(rest_clock))
    
    rest_time_container = ft.Container(
        rest_time_button,
        alignment=ft.alignment.center)
    
    time_controls = ft.Container(
        ft.Row(
            spacing=25,
            controls=[session_time_container, rest_time_container],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center)
    
    page.add(title, pomodoro_img_container, time_controls)


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets")