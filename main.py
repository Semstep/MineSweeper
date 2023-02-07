from kivy.app import App

from Controller.myscreen import MyScreenController
from Model.myscreen import MyScreenModel


class MineSweeperMain(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = MyScreenModel()
        self.controller = MyScreenController(self.model)

    def build(self):
        return self.controller.get_screen()


MineSweeperMain().run()
