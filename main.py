from kivy.app import App

from Controller.MineSweeperController import MineSweeperController
from Model.MineSweeperModel import MineSweepModel
from kivy.utils import platform

if platform not in ['android', 'ios']:
    # Dispose of that nasty red dot
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse, disable_multitouch')


class MineSweeperMain(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = MineSweepModel()
        self.controller = MineSweeperController(self.model)

    def build(self):
        return self.controller.get_screen()


MineSweeperMain().run()
