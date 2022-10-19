from kivy.uix.boxlayout import BoxLayout


class Brick(BoxLayout):
    def __init__(self, **kwargs):
        super(Brick, self).__init__(**kwargs)
        self._number = None
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def init(self, number):
        self._number = number
        self.number.text = number

    def set_brick(self):
        self._parent.set_brick(self._number)
