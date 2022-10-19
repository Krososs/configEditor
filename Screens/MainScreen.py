import os
import pickle

from kivy.uix.screenmanager import Screen

from Widgets.ConfigList import ConfigList
from Widgets.ConfigDetails import ConfigDetails


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.configList = ConfigList()
        self.configDetails = ConfigDetails()

    def on_enter(self):
        if not os.path.exists('././settings.cfg'):
            data = dict(default='None')
            with open('././settings.cfg', 'wb') as f:
                pickle.dump(data, f)
        self.show_config_list()

    def show_config_list(self):
        self.configList.init(self)
        self.bottom.clear_widgets();
        self.bottom.add_widget(self.configList)

    def show_config_details(self, config):
        self.bottom.clear_widgets();
        self.configDetails.set_config(config)
        self.configDetails.set_parent(self)
        self.configDetails.init()
        self.bottom.add_widget(self.configDetails)
