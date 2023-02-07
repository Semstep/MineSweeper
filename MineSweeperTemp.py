from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import MineSwConfig as cfg

Builder.load_file('MineSwField.kv')


class Cell(Widget):
    ...


class TopMenu(BoxLayout):
    ...


class GameField(GridLayout):
    cols = 10
    rows = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_field()

    def create_field(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.add_widget(Button(text='X'))


class MineSwScreen(BoxLayout):
    # def __init__(self):
    #
    #     super().__init__()
    ...


class MineSwApp(App):
    cell = Button(text='X')
    def build(self):
        root = MineSwScreen()

        return root


if __name__ == '__main__':
    MineSwApp().run()