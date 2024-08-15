import flet as ft


class Sounds:
    """ Class For Work With Sound """

    def __init__(self, page: ft.Page, sound_on: bool) -> None:
        self.page = page

        self.sounds = {
            "session_start": f"/audio/session_start.mp3",
            "session_end": f"/audio/session_end.mp3"
        }

        self.sound_on = sound_on

        self.sound_button = ft.IconButton(
            icon=ft.icons.VOLUME_OFF_ROUNDED if self.sound_on else ft.icons.VOLUME_UP_ROUNDED,
            icon_size=25,
            icon_color="#000000",
            on_click=lambda _: self._set_volume())
        
        for sound in self.sounds:
            self.sounds[sound] = ft.Audio(src=self.sounds[sound], volume=0.5, balance=0)
            self.page.overlay.append(self.sounds[sound])
    

    def _set_volume(self) -> None:
        """ Sets Volume On Or Off """
        if self.sound_on:
            self.sound_button.icon=ft.icons.VOLUME_UP_ROUNDED
        else:
            self.sound_button.icon=ft.icons.VOLUME_OFF_ROUNDED
        self.sound_button.update()

        self.sound_on = not(self.sound_on)
        for sound in self.sounds:
            self.sounds[sound].volume = 0.5 if self.sound_on else 0
            self.sounds[sound].update()


    def get_sounds(self) -> dict[str, ft.Audio]:
        """ Returns sounds """
        return self.sounds