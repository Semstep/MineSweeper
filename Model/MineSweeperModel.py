# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.
import MineSwConfig as cfg
from random import sample
from pprint import pprint

class Cell:
    _statuses = ['opened', 'closed', 'flagged', 'quested']  # закрыта, открыта, с флажком, с вопросиком
    yx: tuple
    status: str
    is_mined: bool
    mined_neibs_cnt: int

    def __init__(self, self_row, self_col):
        self.yx = (self_row, self_col, )
        self.status = 'closed'
        self.is_mined = False
        self.mined_neibs_cnt = 0

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

    def has_mine(self):
        return self.is_mined

    def set_mined(self):
        self.is_mined = True

    def get_yx(self):
        return self.yx

    def __repr__(self):
        return f'Cell {self.yx}'

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
    cell_last_changed: list = []
    nrows = cfg.FIELD_ROWNUM
    ncols = cfg.FIELD_COLNUM

    def __init__(self):
        self._observers = []
        for rown in range(self.nrows):
            minefield_row = []
            for coln in range(self.ncols):
                minefield_row.append(Cell(rown, coln))
            self.minefield.append(minefield_row)
        self.is_newplacement = True
        self._init_field()

        print('field_created')

    def _init_field(self):
        nums = sample(range(self.ncols * self.nrows), cfg.NUM_OF_MINES)
        for num in nums:
            self.get_cell_by_num(num).is_mined = True
        for r in self.get_field():
            for c in r:
                c.mined_neibs_cnt = self._count_neighbours(c)

    def _count_neighbours(self, cell: Cell) -> int:
        return sum([m.has_mine() for m in self.get_neibs(cell)]) - cell.has_mine()

    def get_neibs(self, cell: Cell):
        celly, cellx = cell.get_yx()
        return [cl for rows in self.get_field()[max(0, celly-1):celly+2] for cl in rows[max(0, cellx-1):cellx+2]]

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()

    def on_opencell(self, cell_id):
        print('Model: Opened', *cell_id)

    def on_markcell(self, cell_id):
        print('Model: Marked', *cell_id)

    def get_field(self):
        return self.minefield

    def get_cell_id(self, cell: Cell):
        return cell.get_yx()

    def get_cell_by_num(self, num) -> Cell:
        rown = num // self.ncols
        coln = num % self.ncols
        res = self.minefield[rown][coln]
        return res


if __name__ == '__main__':
    model = MineSweepModel()

    # tc1 = model.get_cell_by_num(16)
    # print(tc1)
    for i in range(16):
        curc = model.get_cell_by_num(i)
        nbs = model.get_neibs(curc)
        print(f'Cell {curc.yx} > {nbs}')
