# from View.MineSweeperView import MyScreenView
from View.MineSweeperView import MineSweepScreen


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
        self.model = model
        self.view = MineSweepScreen(
            controller=self, model=self.model)  # инициализируем оба kivy.OblectProperty в классе view

    def get_screen(self):
        """The method creates get the view."""
        return self.view
