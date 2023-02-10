import pickle
import json
import os

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior

from Objects.Container import Container
from Utils.Constants import Constants


class Config(ButtonBehavior, BoxLayout):

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.containers = []
        self.name = None
        self.destination = None
        self._parent = None

    def on_press(self):
        self._parent.show_config_details(self)

    def add_containers(self, container_name, container_position):
        container = Container()
        container.init(container_name, container_position)
        self.containers.append(container)
        self.save()

    def position_taken(self, container_position):
        for container in self.containers:
            if container.position == int(container_position):
                return True
        return False

    def config_includes_container(self, container_name):
        for container in self.containers:
            if container.name == container_name:
                return True
        return False

    def delete_container(self, container_name):
        for container in self.containers:
            if container.name == container_name:
                self.containers.remove(container)
        self.save()

    def delete(self):
        if os.path.exists(self.destination + '/' + self.name + Constants.STR_FILE_JSON):
            os.remove(self.destination + '/' + self.name + Constants.STR_FILE_JSON)
            with open('././settings.cfg', 'rb') as f:
                data = pickle.load(f)
                del data[self.name + Constants.STR_FILE_JSON]
                with open('././settings.cfg', 'wb') as f2:
                    pickle.dump(data, f2)

    def save(self):
        data = {}
        for container in self.containers:
            data[container.name] = {'position': container.position,
                                    'bricks': container.parts}
        with open(os.path.join(self.destination, self.name + Constants.STR_FILE_JSON), 'w+',
                  encoding='utf8') as json_file:
            json.dump(data, json_file, indent=3, ensure_ascii=True)

    def load(
            self,
            data,
            name,
            destination,
            parent,
    ):
        self._parent = parent
        self.set_name(name)
        self.destination = destination

        if data is not None:
            for line in data:
                new_container = Container()
                new_container.init(line, data[line]['position'])
                for brick in data[line]['bricks']:
                    new_container.add_part(brick)
                self.containers.append(new_container)

    def set_name(self, name):
        self.name = name
        self.add_widget(Label(text=self.name, font_size=20))
