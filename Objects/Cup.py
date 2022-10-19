from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Cup(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(Cup, self).__init__(**kwargs)
        self.name = None
        self.position = None
        self._parent = None
        self.bricks = []

    def on_press(self):
        self._parent.show_cup_details(self)

    def show_details(self):
        self.clear_widgets()
        self.add_widget(Label(text=self.name))
        self.add_widget(Label(text="Position: " + str(self.position)))

    def set_parent(self, parent):
        self._parent = parent

    def set_position(self, position):
        self.position = position

    def init(self, name, position):
        self.name = name
        self.position = position

    def add_brick(self, brick):
        self.bricks.append(brick)

    def delete_brick(self, brick):
        self.bricks.remove(brick)