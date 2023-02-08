import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
# from Controller.MineSweeperController import

import MineSwConfig as cfg
from Utility.observer import Observer

Builder.load_file(os.path.join(os.path.dirname(__file__), "MineSweeperScreen.kv"))


class TopMenu(BoxLayout):
    ...


class MineField(GridLayout):
    cols = cfg.FIELD_COLNUM
    rows = cfg.FIELD_ROWNUM

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_field()

    def create_field(self):
        ...


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
        self.model.add_observer(self)  # register the view as an observer

    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """
        ...



