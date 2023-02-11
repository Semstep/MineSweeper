import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from pprint import pprint

import Model.MineSweeperModel
from Utility.observer import Observer

Builder.load_file(os.path.join(os.path.dirname(__file__), "MineSweeperScreen.kv"))


class FieldCell(Button):
    id: tuple
    ctr = 0
    model_cell: Model.MineSweeperModel.Cell  # ! Для чистоты подхода стоит убрать вместе с импортом

    def __init__(self, cell, **kw):
        super().__init__(**kw)
        self.model_cell = cell

    def on_press(self):
        # # print('Button:', self.last_touch.button)  # last_touch буфер для события тача
        if self.last_touch.button == 'left':
            self.parent.controller.act_opencell(self.model_cell.yx)
        elif self.last_touch.button == 'right':
            self.parent.controller.act_markcell(self.model_cell.yx)


class TopMenu(BoxLayout):
    ...


class MineField(GridLayout):
    controller = ObjectProperty()

    def create_field(self, gamefield):
        self.rows = len(gamefield)
        self.cols = len(gamefield[0])
        for row in gamefield:
            for cell in row:
                self.add_widget(FieldCell(cell))
        print('field widget created')

    def refresh(self, gamover):
        ctr = 0
        for cell in self.children:
            if isinstance(cell, FieldCell):
                stat = cell.model_cell.status
                if not gamover:
                    if stat == 'opened':
                        if not cell.model_cell.has_mine:
                            cell.disabled = True
                            capt = str(cell.model_cell.mined_neibs_cnt)
                            cell.text = capt if capt != '0' else ''
                        else:
                            cell.text = '*'
                    elif stat == 'closed':
                        cell.text = ''
                    elif stat == 'flagged':
                        cell.text = '!'
                    elif stat == 'quested':
                        cell.text = '?'
                    else:
                        raise ValueError('Unknown field state')

                else:
                    if cell.model_cell.has_mine:
                        cell.text = 'X'

        print('View: refreshed', ctr)


class MineSweepScreen(Observer, BoxLayout):
    """
    A class that implements the visual presentation `MyScreenModel`.

    """
    # Оба ObjectProperty прилетают при инициализации этого view в контроллере
    # <Controller.myscreen_controller.MyScreenController object>
    controller = ObjectProperty()
    # <Model.myscreen.MyScreenModel object>.
    model = ObjectProperty()
    minefield = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        mf = self.get_child('MineField')
        mf.controller = self.controller
        mf.create_field(self.controller.get_gamefield())
        self.minefield = mf
        self.model.add_observer(self)  # register the view as an observer

    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """
        self.minefield.refresh(self.model.gameover)

    def get_child(self, cls_name):
        for c in self.children:
            if cls_name in c.__class__.__name__:
                return c
        return None
# class MineSweepScreen():