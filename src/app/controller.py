from model import Model
from view import View

class Controller:
    def __init__(self, root) -> None:
        self.model = Model()
        self.view = View(root)

        return