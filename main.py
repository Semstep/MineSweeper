from kivy.app import App

from Controller.MineSweeperController import MineSweeperController
from Model.MineSweeperModel import MineSweepModel


class MineSweeperMain(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = MineSweepModel()
        self.controller = MineSweeperController(self.model)

    def build(self):
        return self.controller.get_screen()


MineSweeperMain().run()
