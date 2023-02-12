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
DEBUG = True

class FieldCell(Button):
    id: tuple
    ctr = 0
    model_cell: Model.MineSweeperModel.Cell  # ! Для чистоты подхода стоит убрать вместе с импортом

    def __init__(self, cell, **kw):
        super().__init__(**kw)
        self.model_cell = cell

    def on_press(self):
        if self.last_touch.button == 'left':
            self.parent.controller.act_opencell(self.model_cell.yx)
        elif self.last_touch.button == 'right':
            self.parent.controller.act_markcell(self.model_cell.yx)


class TopMenu(BoxLayout):
    controller = ObjectProperty()
    minecnt = ObjectProperty()
    gamestatus = ObjectProperty()
    gamemenu = ObjectProperty()

    def show_remaining(self, remains):
        self.minecnt.text = str(remains)


class MineField(GridLayout):

    def create_field(self, gamefield):
        self.rows = len(gamefield)
        self.cols = len(gamefield[0])
        for row in gamefield:
            for cell in row:
                self.add_widget(FieldCell(cell))
        print('field widget created')

    def refresh(self):
        ctr = 0
        for cell in self.children:
            if isinstance(cell, FieldCell):
                stat = cell.model_cell.status
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

        print('View: refreshed', ctr)


class MineSweepScreen(Observer, BoxLayout):
    """
    A class that implements the visual presentation `MyScreenModel`.

    """
    # Оба ObjectProperty прилетают при инициализации этого view в контроллере
    controller = ObjectProperty()
    model = ObjectProperty()

    minefield = ObjectProperty()
    topmenu = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        mf = self.get_subclass(MineField)
        tm = self.get_subclass(TopMenu)
        self.topmenu = tm
        tm.controller = self.controller
        tm.minecnt.text = str(self.model.mines_remain)
        mf.controller = self.controller
        mf.create_field(self.controller.get_gamefield())
        self.minefield = mf
        self.model.add_observer(self)  # register the view as an observer

    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        """
        self.minefield.refresh()
        self.topmenu.minecnt.text = str(self.model.mines_remain)
        if self.model.gameover:
            print('---------GAMOVER------------')
            if self.model.is_win:
                self.topmenu.gamestatus.text = 'КРОСАВЧЕГ'
            else:
                self.topmenu.gamestatus.text = 'ЛУЗЕР'

    def start_new_game(self):
        self.controller.act_restart_game()


    def get_subclass(self, cls):
        for c in self.children:
            if isinstance(c, cls):
                return c
