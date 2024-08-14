import flet as ft


class Sounds:
    """ Class For Work With Sound """

    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.sounds = {
            "session_start": f"/audio/session_start.mp3",
            "session_end": f"/audio/session_end.mp3"
        }

        for sound in self.sounds:
            self.sounds[sound] = ft.Audio(src=self.sounds[sound], volume=0.5, balance=0)
            self.page.overlay.append(self.sounds[sound])
    

    def get_sounds(self):
        """ Returns sounds """
        return self.sounds