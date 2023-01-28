import pickle
import json
import os

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior

from Objects.Cup import Cup


class Config(ButtonBehavior, BoxLayout):

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.cups = []
        self.name = None
        self._parent = None

    def on_press(self):
        self._parent.show_config_details(self)

    def is_default(self):
        with open('././settings.cfg', 'rb') as f:
            data = pickle.load(f)
        return data['default'] == self.name

    def add_cup(self, cup_name, cup_position):
        cup = Cup()
        cup.init(cup_name, cup_position)
        self.cups.append(cup)
        self.save()

    def position_taken(self, cup_position):
        for cup in self.cups:
            if cup.position == int(cup_position):
                return True
        return False

    def config_includes_cup(self, cup_name):
        for cup in self.cups:
            if cup.name == cup_name:
                return True
        return False

    def delete_cup(self, cup_name):
        for cup in self.cups:
            if cup.name == cup_name:
                self.cups.remove(cup)
        self.save()

    def delete(self):

        if os.path.exists(self._parent.directory + '/' + self.name
                          + '.json'):
            os.remove(self._parent.directory + '/' + self.name + '.json'
                      )

    def save(self):
        data = {}
        for cup in self.cups:
            data[cup.name] = {'position': cup.position,
                              'bricks': cup.parts}

        with open(self._parent.directory + '/' + self.name + '.json',
                  'w+', encoding='utf8') as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=True)

    def load(
            self,
            data,
            name,
            parent,
    ):
        self._parent = parent
        self.set_name(name)

        if data is not None:
            for line in data:
                new_cup = Cup()
                new_cup.init(line, data[line]['position'])
                for brick in data[line]['bricks']:
                    new_cup.add_part(brick)
                self.cups.append(new_cup)

    def set_name(self, name):
        self.name = str(name)
        if self.is_default():
            self.add_widget(Label(text=self.name + ' (Default)'))
        else:
            self.add_widget(Label(text=self.name))
