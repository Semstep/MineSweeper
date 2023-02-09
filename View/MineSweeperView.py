import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
# from Controller.MineSweeperController import
from Model.MineSweeperModel import MineSweepModel as mdl

import MineSwConfig as cfg
from Utility.observer import Observer

Builder.load_file(os.path.join(os.path.dirname(__file__), "MineSweeperScreen.kv"))


class TopMenu(BoxLayout):
    ...


class MineField(GridLayout):
    # cols = cfg.FIELD_COLNUM
    # rows = cfg.FIELD_ROWNUM
    fld_repr = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fld_repr = mdl.minefield
        self.create_field()

    def create_field(self):
        self.cols, self.rows = len(self.fld_repr), len(self.fld_repr[0])
        for i in range(self.rows):
            for j in range(self.cols):
                self.add_widget(Button())
        print(f'field of {self.rows}, {self.cols} created')


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
        # fld = self.model.get_field()
        # self.children[0].create_field(fld)

        self.model.add_observer(self)  # register the view as an observer


    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """
        ...



