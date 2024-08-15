import flet as ft
import asyncio

from timer import Pomodoro


def main(page: ft.Page):
    """ App entry point """

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
        width=175,
        height=175,
        src=f"/img/Pomodoro.png")
    
    pomodoro_img_container = ft.Container(
        content=pomodoro_img,
        padding=40,
        alignment=ft.alignment.center)

    pomodoro_timer = Pomodoro(page)
    time_controls = pomodoro_timer.time_controls
    counter = pomodoro_timer.session_counter_container
    buttons = pomodoro_timer.buttons
    
    page.add(title, pomodoro_img_container, time_controls, counter, buttons)


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets")