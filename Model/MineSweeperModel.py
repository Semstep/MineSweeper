# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.
import MineSwConfig as cfg

class Cell:
    _statuses = ['opened', 'closed', 'flagged', 'quested']  # закрыта, открыта, с флажком, с вопросиком
    col: int
    row: int
    status: str
    is_mined: bool

    def __init__(self, self_col, self_row):
        self.col, self.row = self_col, self_row
        self.status = 'closed'
        self.is_mined = False

    def check_status(self, new_status: str):
        return True if new_status in self._statuses else False

    def open(self):
        if self.status == 'closed':
            self.status = 'opened'
            return True
        return False

    def change_mark(self):
        if self.status == 'opened':
            return False
        nextidx = self._statuses.index(self.status) + 1
        if nextidx >= len(self._statuses):
            nextidx = 1
        self.status = self._statuses[nextidx]
        return True

    def is_mine(self):
        return self.is_mined

    def set_mined(self):
        self.is_mined = True

class MineSweepModel:
    """
    The MyScreenModel class is a data model implementation. The model stores
    the values of the variables `c`, `d` and their sum. The model provides an
    interface through which to work with stored values. The model contains
    methods for registration, deletion and notification observers.

    The model is (primarily) responsible for the logic of the application.
    MyScreenModel class task is to add two numbers.
    """
    minefield: list = []

    def __init__(self):
        self._observers = []
        for i in range(cfg.FIELD_COLNUM):
            minefield_row = []
            for j in range(cfg.FIELD_ROWNUM):
                minefield_row.append(Cell(i, j))
            self.minefield.append(minefield_row)
        print('field_created')

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()

    def on_field_open(self, *args):
        print('Opened', {args})
        ...

    def on_field_mark(self, *args):
        print('Marked', {args})

    def get_field(self):
        return self.minefield

    def get_cell_id(self, cell: Cell):
        return cell.row, cell.col
