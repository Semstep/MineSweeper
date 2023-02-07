from kivy.app import App
from kivy.uix.widget import Widget
from kivy.app import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import MineSwConfig as cfg
from kivy.core.window import Window

Builder.load_file('View/MineSweeperScreen.kv')


class TopMenu(BoxLayout):
    ...


class MineField(GridLayout):
    cols = cfg.FIELD_COLNUM
    rows = cfg.FIELD_ROWNUM

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_field()

    def create_field(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.add_widget(Cell(i, j))

    def on_size(self, *args):
        print('field size is', args[-1])


class MineSweepScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MineSwApp(App):

    def build(self):
        root = MineSweepScreen()
        return root


if __name__ == '__main__':
    MineSwApp().run()