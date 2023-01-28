import os
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from Objects.Config import Config
from Utils import StringUtil


class ConfigList(BoxLayout):
    def __init__(self, **kwargs):
        super(ConfigList, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.directory = 'Configs'
        self.configs = []
        self.mainScreen = None

    def init(self, parent):
        self.name.text = ""
        self.mainScreen = parent
        self.display_configs()

    def display_configs(self):
        self.load_configs()
        self.scrollview.scroll_y = 1
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()
        self.layout.height = len(self.configs) * 100
        for config in self.configs:
            self.layout.add_widget(config)
        self.scrollview.add_widget(self.layout)

    def save_new_config(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if len(self.name.text) == 0:
            self.error.text = "Name can not be empty"
        elif (os.path.exists(self.directory + '/' + self.name.text + '.json')):
            self.error.text = "File already exist"
        elif StringUtil.name_contains_forbidden_characters(self.name.text):
            self.error.text = "Name contains forbidden characters"
        else:
            self.error.text = ""
            data = {}
            with open(self.directory + '/' + self.name.text + '.json', 'w', encoding='utf8') as json_file:
                json.dump(data, json_file, indent=3, ensure_ascii=True)
            self.display_configs()

    def load_configs(self):
        self.configs = []
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        files = os.listdir(self.directory)
        if len(files) > 0:
            for file in files:
                filename = os.path.basename(self.directory + '/' + file)
                name = filename.split(".")
                with open(self.directory + '/' + file) as f:
                    try:
                        data = json.load(f)
                    except json.decoder.JSONDecodeError:
                        data = None

                config = Config()
                config.load(data, name[0], self)
                self.configs.append(config)

    def show_config_details(self, config):
        self.mainScreen.show_config_details(config)
