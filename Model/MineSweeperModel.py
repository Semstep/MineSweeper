# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.
import MineSwConfig as cfg
from random import sample


class Cell:
    _statuses = ['opened', 'closed', 'flagged', 'quested']  # закрыта, открыта, с флажком, с вопросиком
    _yx: tuple
    _status: str
    _is_mined: bool
    _mined_neibs_cnt: int

    @property
    def yx(self):
        return self._yx

    @yx.setter
    def yx(self, val):
        self._yx = val

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        if val in self._statuses:
            self._status = val
        else:
            raise ValueError(f'Статус должен быть одним из {self._statuses}')

    @property
    def has_mine(self):
        return self._is_mined

    @has_mine.setter
    def has_mine(self, value):
        self._is_mined = value

    @property
    def mined_neibs_cnt(self):
        return self._mined_neibs_cnt

    @mined_neibs_cnt.setter
    def mined_neibs_cnt(self, value):
        self._mined_neibs_cnt = value

    def __init__(self, self_row, self_col):
        self.yx = (self_row, self_col, )
        self.status = 'closed'
        self.has_mine = False
        self.mined_neibs_cnt = 0

    def check_status(self, new_status: str):
        return True if new_status in self._statuses else False

    def open(self):
        if self.status != 'flagged':
            self.status = 'opened'
            return True
        return False

    def change_mark(self):
        if self.status != 'opened':
            nextidx = self._statuses.index(self.status) + 1
            if nextidx >= len(self._statuses):
                nextidx = 1
            self.status = self._statuses[nextidx]
            return self.status
        raise ValueError("opened cell can't be marked")

    def __repr__(self):
        return f'Cell {self.yx}'


class MineSweepModel:
    """
    The MyScreenModel class is a data model implementation. The model stores
    the values of the variables. The model provides an
    interface through which to work with stored values. The model contains
    methods for registration, deletion and notification observers.

    The model is (primarily) responsible for the logic of the application.
    MyScreenModel class task is to add two numbers.
    Состояния игры определяем по двум фалагам: gameover и плюс is_win
    Таймер обеспечивает модуль view или main т.к. суперцикл там
    """

    def __init__(self):
        self.is_win = False
        self.gameover = False
        self.was_no_moves = False
        self.ncols, self.nrows, self.mines_num = 0, 0, 0
        self.minefield: list = []
        self.cell_last_changed: list = []
        self.mines_remain = 0
        self.init_game(cfg.FIELD_ROWNUM, cfg.FIELD_COLNUM, cfg.NUM_OF_MINES)
        self._observers = []

    def init_game(self, rows_num, cols_num, mines_num):
        self.nrows, self.ncols, self.mines_num = rows_num, cols_num, mines_num
        self.mines_remain = self.mines_num

        self.minefield.clear()
        for rown in range(self.nrows):
            minefield_row = []
            for coln in range(self.ncols):
                minefield_row.append(Cell(rown, coln))
            self.minefield.append(minefield_row)
        self.was_no_moves = True

        self.is_win, self.gameover = False, False

    def place_mines(self):
        nums = sample(range(self.ncols * self.nrows), self.mines_num)
        for num in nums:
            self.get_cell_by_num(num).has_mine = True
        for r in self.get_field():
            for c in r:
                c.mined_neibs_cnt = self._count_neighbours(c)

    def _count_neighbours(self, cell: Cell) -> int:
        return sum([m.has_mine for m in self.get_neibs(cell)]) - cell.has_mine

    def get_neibs(self, cell: Cell):
        celly, cellx = cell.yx
        return [cl for rows in self.get_field()[max(0, celly-1):celly+2] for cl in rows[max(0, cellx-1):cellx+2]]

    def _open_empty_cells(self, cell):
        cell.open()
        neibs = self.get_neibs(cell)
        neibs.remove(cell)
        for c in neibs:
            if c.mined_neibs_cnt == 0:
                if c.status == 'opened' or c.status == 'flagged':
                    continue
                self._open_empty_cells(c)
            else:
                c.open()

    def opencell(self, cell_id):
        cell = self.get_cell(cell_id)
        if cell.open():
            if cell.has_mine:
                self.gameover = True
                self.is_win = False
                self.notify_observers()
            else:
                if cell.mined_neibs_cnt == 0:
                    self._open_empty_cells(cell)
            self.test_win()
            self.notify_observers()

    def test_win(self):
        """
        Проверяю только если количество установленных флажков == кол-ву мин
        Если есть кроме того неоткрытые клетки, то победу не присуждаем
        """
        if self.mines_remain == 0:
            for row in self.get_field():
                for cell in row:
                    if cell.status == 'flagged' and not cell.has_mine:
                        return False
                    if cell.status in ('closed', 'quested'):
                        return False
            print('Model: win detected')
            self.gameover = self.is_win = True

    def mark_cell(self, cell_id):
        prevstate = self.get_cell(cell_id).status
        state = self.get_cell(cell_id).change_mark()
        #  Подсчет непомеченных мин, чтоб не проходиться по всему полю считая флажки
        if prevstate == 'flagged' and prevstate != state:
            self.mines_remain += 1
        elif prevstate != 'flagged' and state == 'flagged':
            self.mines_remain -= 1
        self.test_win()
        print('Model: Marked', *cell_id)

        self.notify_observers()

    def get_field(self) -> list:
        return self.minefield

    def get_cell_id(self, cell: Cell):
        return cell.yx

    def get_cell(self, cell_yx) -> Cell:
        row, col = cell_yx
        return self.get_field()[row][col]

    def get_cell_by_num(self, num) -> Cell:
        rown = num // self.ncols
        coln = num % self.ncols
        res = self.minefield[rown][coln]
        return res

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for x in self._observers:
            x.model_is_changed()


if __name__ == '__main__':
    model = MineSweepModel()

    # tc1 = model.get_cell_by_num(16)
    # print(tc1)
    for i in range(16):
        curc = model.get_cell_by_num(i)
        nbs = model.get_neibs(curc)
        print(f'Cell {curc.yx} > {nbs}')
