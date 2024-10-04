import flet as ft
import asyncio

from audio import Sounds


class Pomodoro:
    """ Class that creates a Pomodoro timer """

    def __init__(self, page:ft.Page, session_seconds=1500, rest_seconds=300) -> None:
        self.page = page
        self.session_seconds = session_seconds
        self.cur_session_seconds = self.session_seconds
        self.rest_seconds = rest_seconds
        self.cur_rest_seconds = self.rest_seconds
        self.timer_state = "STOP"
        self.sessions_count = 0

        self.sound_settings = Sounds(self.page, True)
        self.sounds = self.sound_settings.get_sounds()
        self.sound_button = self.sound_settings.sound_button

        session_clock = ft.TimePicker(
            value="00:25",
            time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
            on_change=self.set_session_time)
        
        self.session_time_button = ft.TextButton(
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
            self.session_time_button,
            alignment=ft.alignment.center)
        
        rest_clock = ft.TimePicker(
            value="00:05",
            time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
            hour_label_text="Minutes",
            minute_label_text="Seconds",
            on_change=self.set_rest_time)

        self.rest_time_button = ft.TextButton(
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
            self.rest_time_button,
            alignment=ft.alignment.center)
        
        self.time_controls = ft.Container(
            ft.Row(
                spacing=25,
                controls=[session_time_container, rest_time_container],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center)
        
        self.session_counter_container = ft.Container(
            ft.Text(
                value=f"Session count: {str(self.sessions_count)}",
                color="#000000",
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One",
                visible=False),
            alignment=ft.alignment.center)
        
        self.start_button = ft.OutlinedButton(
            width=120,
            height=35,
            content=
            ft.Text(
                value="Start".upper(),
                color="#000000",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One"),
            style=ft.ButtonStyle(
                bgcolor="#ff7700",
                overlay_color="#c95e00",
                side=ft.BorderSide(0, "#bdbdbd"),
                shape=ft.RoundedRectangleBorder(5)),
            on_click=lambda _: self.start_session())
        
        self.reset_button = ft.OutlinedButton(
            width=120,
            height=35,
            disabled=True,
            content=
            ft.Text(
                value="Reset".upper(),
                color="#000000",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                font_family="Nixie One"),
            style=ft.ButtonStyle(
                bgcolor="#ff7700",
                overlay_color="#c95e00",
                side=ft.BorderSide(0, "#bdbdbd"),
                shape=ft.RoundedRectangleBorder(5)),
            on_click=lambda _:self.reset_session())

        self.buttons = ft.Container(
            ft.Row(
                [self.start_button, self.reset_button],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            alignment=ft.alignment.center)


    def set_session_time(self, e) -> None:
        """ Sets session time """

        hours, minutes = map(int, e.data.split(":"))
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)

        self.session_seconds = hours * 3600 + minutes * 60
        self.cur_session_seconds = self.session_seconds
        self.session_time_button.content.value = f"{hours_str}:{minutes_str}"
        self.session_time_button.update()
    

    def set_rest_time(self, e) -> None:
        """ Sets rest time """

        minutes, seconds = map(int, e.data.split(":"))
        minutes_str, seconds_str = str(minutes) if minutes >= 10 else "0" + str(minutes), str(seconds) if seconds >= 10 else "0" + str(seconds)

        self.rest_seconds = minutes * 60 + seconds
        self.cur_rest_seconds = self.rest_seconds
        self.rest_time_button.content.value = f"{minutes_str}:{seconds_str}"
        self.rest_time_button.update()


    def start_session(self) -> None:
        """ Start session """

        self.timer_state = "SESSION"

        self.session_counter_container.content.visible = True
        self.start_button.disabled = True
        self.session_time_button.disabled = True
        self.rest_time_button.disabled = True
        self.reset_button.disabled = False

        self.start_button.update()
        self.session_counter_container.update()
        self.session_time_button.update()
        self.rest_time_button.update()
        self.reset_button.update()
        
        # FOR TEST
        # self.session_seconds = 10
        # self.rest_seconds = 10

        self.cur_session_seconds = self.session_seconds
        self.cur_rest_seconds = self.rest_seconds

        self.page.run_task(self.start_time)


    def reset_session(self) -> None:
        """ Resets session if it's starts """

        self.timer_state = "STOP"
        self.sounds["session_end"].play()
        self.sessions_count = 0
        self.session_counter_container.content.value = f"Session count: {self.sessions_count}"
        self.session_counter_container.update()

        hours, minutes  = divmod(self.session_seconds, 60)
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)
        self.session_time_button.content.value = f"{hours_str}:{minutes_str}"
        
        minutes, seconds  = divmod(self.rest_seconds, 60)
        minutes_str, seconds_str = str(minutes) if minutes >= 10 else "0" + str(minutes), str(seconds) if seconds >= 10 else "0" + str(seconds)
        self.rest_time_button.content.value = f"{minutes_str}:{seconds_str}"

        self.start_button.disabled = False
        self.session_counter_container.content.visible = False
        self.session_time_button.disabled = False
        self.rest_time_button.disabled = False
        self.reset_button.disabled = True

        self.start_button.update()
        self.session_counter_container.update()
        self.session_time_button.update()
        self.rest_time_button.update()
        self.reset_button.update()

        self.page.update()
    

    async def start_time(self) -> None:
        """ Controls work and rest sessions """

        self.page.window.to_front()
        self.sounds["session_start"].play()
        self.cur_rest_seconds = self.rest_seconds

        minutes, seconds  = divmod(self.cur_rest_seconds, 60)
        minutes_str, seconds_str = str(minutes) if minutes >= 10 else "0" + str(minutes), str(seconds) if seconds >= 10 else "0" + str(seconds)

        self.rest_time_button.content.value = f"{minutes_str}:{seconds_str}"
        self.rest_time_button.update()

        while self.timer_state == "SESSION" and self.cur_session_seconds >= 0:
            hours, minutes  = divmod(self.cur_session_seconds, 60)
            hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)
            
            self.session_time_button.content.value = f"{hours_str}:{minutes_str}"
            self.session_time_button.update()

            await asyncio.sleep(1)
            self.cur_session_seconds -= 1
            if self.cur_session_seconds == 0:
                self.timer_state = "REST"
        
        self.page.window.to_front()
        if self.timer_state == "REST":
            self.sounds["session_end"].play()

            self.sessions_count += 1
            self.session_counter_container.content.value = f"Session count: {self.sessions_count}"
            self.session_counter_container.update()
            
        self.cur_session_seconds = self.session_seconds

        hours, minutes  = divmod(self.cur_session_seconds, 60)
        hours_str, minutes_str = str(hours) if hours >= 10 else "0" + str(hours), str(minutes) if minutes >= 10 else "0" + str(minutes)
        
        self.session_time_button.content.value = f"{hours_str}:{minutes_str}"
        self.session_time_button.update()

        while self.timer_state == "REST" and self.cur_rest_seconds >= 0:
            minutes, seconds  = divmod(self.cur_rest_seconds, 60)
            minutes_str, seconds_str = str(minutes) if minutes >= 10 else "0" + str(minutes), str(seconds) if seconds >= 10 else "0" + str(seconds)

            self.rest_time_button.content.value = f"{minutes_str}:{seconds_str}"
            self.rest_time_button.update()

            await asyncio.sleep(1)
            self.cur_rest_seconds -= 1
            if self.cur_rest_seconds == -1:
                self.timer_state = "SESSION"
                self.page.run_task(self.start_time)