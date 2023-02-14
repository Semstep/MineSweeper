import logging
import os

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from pprint import pprint

import Model.MineSweeperModel
from Controller import MineSweeperController
from Utility.observer import Observer


Builder.load_file(os.path.join(os.path.dirname(__file__), "MineSweeperScreen.kv"))

logger = logging.getLogger('slave.'+__name__)


class DemineTimer(Label):
    event_onesecond = ObjectProperty()
    timer_ctr = NumericProperty

    def start(self):
        self.timer_ctr = 0
        self.event_onesecond = Clock.schedule_interval(self.update, 1)

    def stop(self):
        if self.event_onesecond:
            self.event_onesecond.cancel()
            logger.info(f'Timer stopped at {self.timer_ctr} s')
            # print('View: Timer stopped')

    def update(self, dt):
        self.timer_ctr += 1
        self.text = f'{self.timer_ctr:03}'

    def reset(self):
        self.stop()
        self.timer_ctr = 0
        self.text = '000'


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
    controller: MineSweeperController = ObjectProperty()
    minecnt = ObjectProperty()
    gamestatus = ObjectProperty()
    demine_timer = ObjectProperty()

    def reset(self):
        self.demine_timer.reset()
        self.gamestatus.text = ''


class MineField(GridLayout):

    def create_field(self, gamefield):
        self.rows = len(gamefield)
        self.cols = len(gamefield[0])
        for row in gamefield:
            for cell in row:
                self.add_widget(FieldCell(cell))
        logger.info(f'Field widget created. {self.rows}:{self.cols}')

    def refresh(self, is_looser=False):
        ctr = 0
        for cell in self.children:
            if isinstance(cell, FieldCell):
                stat = cell.model_cell.status
                if not is_looser:
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
        ctr += 1
        logger.debug(f'Field refreshed {ctr} times')

    def reset(self):
        for widg in self.children[:]:
            if isinstance(widg, FieldCell):
                self.remove_widget(widg)


class MineSweepScreen(Observer, BoxLayout):
    """
    A class that implements the visual presentation `MyScreenModel`.

    """
    # Оба ObjectProperty прилетают при инициализации этого view в контроллере
    controller = ObjectProperty()
    model: Model.MineSweeperModel = ObjectProperty()

    minefield: MineField = ObjectProperty()
    topmenu = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.minefield = self.get_subclass(MineField)
        self.topmenu = self.get_subclass(TopMenu)

        self.topmenu.controller = self.controller
        self.topmenu.minecnt.text = str(self.model.mines_remain)
        self.minefield.controller = self.controller
        self.minefield.create_field(self.controller.get_gamefield())

        self.model.add_observer(self)  # register the view as an observer

    def model_is_changed(self, *args):
        """
        The method is called when the model changes.
        """
        self.minefield.refresh()
        self.topmenu.minecnt.text = str(self.model.mines_remain)
        if self.model.gameover:
            logger.info(f'Game Overed: player is {"winner" if self.model.is_win else "looser"}')
            if self.model.is_win:
                self.topmenu.gamestatus.text = 'КРОСАВЧЕГ'
            else:
                self.topmenu.gamestatus.text = 'ЛУЗЕР'
                self.minefield.refresh(is_looser=True)

    def start_new_game(self):
        self.controller.act_restart_game()
        self.minefield.reset()
        self.minefield.create_field(self.controller.get_gamefield())
        self.topmenu.reset()

    def get_subclass(self, cls):
        for c in self.children:
            if isinstance(c, cls):
                return c

