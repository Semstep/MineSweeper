from View.MineSweeperView import MineSweepScreen
from Model.MineSweeperModel import MineSweepModel
import MineSwConfig as cfg


class MineSweeperController:
    """
    The `MyScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.

    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        """
        The constructor takes a reference to the model.
        The constructor creates the view.
        """
        # ! Странно, что этот класс не добавляется в модель как наблюдаемый
        self.model: MineSweepModel = model
        self.gamefield = self.model.minefield
        self.view = MineSweepScreen(
            controller=self, model=self.model)  # инициализируем оба kivy.OblectProperty в классе view

    def get_screen(self):
        """The method creates get the view."""
        return self.view

    def get_gamefield(self):
        return self.gamefield

    def get_cell_id(self, cell):
        return self.model.get_cell_id(cell)

    def act_opencell(self, cell_id: tuple):
        if self.model.was_no_moves:
            self.start_game()
        if not self.model.gameover:
            self.model.opencell(cell_id)

    def act_markcell(self, cell_id: tuple):
        if not self.model.gameover:
            self.model.mark_cell(cell_id)

    def act_restart_game(self):
        self.model.init_game(cfg.FIELD_ROWNUM, cfg.FIELD_COLNUM, cfg.NUM_OF_MINES)
        self.model.notify_observers()

    def start_game(self):
        self.model.was_no_moves = False
        self.model.place_mines()
        # self.view.topmenu.timer_start()


