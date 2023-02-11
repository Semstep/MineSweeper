import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from pprint import pprint

from Utility.observer import Observer

Builder.load_file(os.path.join(os.path.dirname(__file__), "MineSweeperScreen.kv"))


class FieldCell(Button):
    id: tuple
    ctr = 0

    def __init__(self, cell, **kw):
        super().__init__(**kw)
        self.id = cell.yx
        if cell.has_mine:
            self.text = '*'
        else:
            self.text = str(cell.mined_neibs_cnt) if cell.mined_neibs_cnt else ''

    def on_press(self):
        # # print('Button:', self.last_touch.button)  # last_touch буфер для события тача
        if self.last_touch.button == 'left':
            self.parent.controller.act_opencell(self.id)
        elif self.last_touch.button == 'right':
            self.parent.controller.act_markcell(self.id)


class TopMenu(BoxLayout):
    ...


class MineField(GridLayout):
    gamefield_view: list = []
    controller = ObjectProperty()

    def create_field(self, gamefield):
        self.rows = len(gamefield)
        self.cols = len(gamefield[0])
        for row in gamefield:
            for cell in row:
                self.add_widget(FieldCell(cell))
        print('field widget created')


class MineSweepScreen(Observer, BoxLayout):
    """
    A class that implements the visual presentation `MyScreenModel`.

    """
    # Оба ObjectProperty прилетают при инициализации этого view в контроллере
    # <Controller.myscreen_controller.MyScreenController object>
    controller = ObjectProperty()
    # <Model.myscreen.MyScreenModel object>.
    model = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        mf = self.get_child('MineField')
        mf.controller = self.controller
        mf.create_field(self.controller.get_gamefield())
        self.model.add_observer(self)  # register the view as an observer

    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """
        ...

    def get_child(self, cls_name):
        for c in self.children:
            if cls_name in c.__class__.__name__:
                return c
        return None
# class MineSweepScreen():