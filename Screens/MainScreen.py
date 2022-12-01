from kivy.uix.screenmanager import Screen
from Widgets.ConfigList import ConfigList
from Widgets.ConfigDetails import ConfigDetails


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.configList = ConfigList()
        self.configDetails = ConfigDetails()

    def on_enter(self):
        self.show_config_list()

    def show_config_list(self):
        self.bottom.clear_widgets()
        self.configList.init(self)
        self.bottom.add_widget(self.configList)

    def show_config_details(self, config):
        self.bottom.clear_widgets()
        self.configDetails.set_config(config)
        self.configDetails.set_parent(self)
        self.configDetails.init()
        self.bottom.add_widget(self.configDetails)
