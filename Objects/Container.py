from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Container(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.name = None
        self.position = None
        self._parent = None
        self.parts = []

    def on_press(self):
        self._parent.show_container_details(self)

    def show_details(self):
        self.clear_widgets()
        self.add_widget(Label(text=self.name, font_size=18))
        self.add_widget(Label(text="Position: " + str(self.position), font_size=18))

    def set_parent(self, parent):
        self._parent = parent

    def set_position(self, position):
        self.position = position

    def init(self, name, position):
        self.name = name
        self.position = position

    def contains_part(self, part):
        return part in self.parts

    def add_part(self, part):
        if not self.contains_part(part):
            self.parts.append(part)

    def remove_part(self, part):
        if self.contains_part(part):
            self.parts.remove(part)
