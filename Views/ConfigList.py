import pickle
import os
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from Objects.Config import Config
from Utils import StringUtil
from Utils.Constants import Constants
from Views.Popups import SaveDialog


class ConfigList(BoxLayout):
    def __init__(self, **kwargs):
        super(ConfigList, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.selected_destination = None
        self.configs = []
        self.mainScreen = None
        self.popup = None

    def init(self, parent):
        self.name.text = Constants.EMPTY
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

    def open_destination_popup(self):
        content = SaveDialog(save=self.set_destination, cancel=self.close_destination_popup)
        self.popup = Popup(title="Save file", content=content,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def close_destination_popup(self):
        self.popup.dismiss()

    def set_destination(self, path):
        self.destination.text = path
        self.selected_destination = path
        self.popup.dismiss()

    def save_new_config(self):
        if self.selected_destination is None:
            self.error.text = Constants.ER_WRONG_DESTINATION
        elif len(self.name.text) == 0:
            self.error.text = Constants.ER_NAME_EMPTY
        elif os.path.exists(self.selected_destination + '/' + self.name.text + Constants.STR_FILE_JSON):
            self.error.text = Constants.ER_FILE_EXIST
        elif StringUtil.name_contains_forbidden_characters(self.name.text):
            self.error.text = Constants.ER_FORBIDDEN_CHARS
        else:
            self.error.text = ""
            self.name.text += Constants.STR_FILE_JSON
            data = {}
            with open(os.path.join(self.selected_destination, self.name.text), 'w', encoding='utf8') as json_file:
                json.dump(data, json_file, indent=3, ensure_ascii=True)
            self.save_destination(self.name.text, self.selected_destination)
            self.display_configs()
            self.name.text = ""

    def save_destination(self, name, destination):
        with open('././settings.cfg', 'rb') as f:
            data = pickle.load(f)
            with open('././settings.cfg', 'wb') as f:
                data[name] = destination
                pickle.dump(data, f)

    def load_configs(self):
        self.configs = []
        with open('././settings.cfg', 'rb') as f:
            data = pickle.load(f)
            for key, value in data.items():
                if key != Constants.STR_API_KEY and key != "default" and os.path.exists(value + '/' + key):
                    with open(os.path.join(value, key)) as f:
                        try:
                            config_data = json.load(f)
                        except json.decoder.JSONDecodeError:
                            config_data = None
                    name = key.split(".")
                    config = Config()
                    config.load(config_data, name[0], value, self)
                    self.configs.append(config)

    def show_config_details(self, config):
        self.mainScreen.show_config_details(config)
