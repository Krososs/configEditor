from kivy.config import Config

Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', 0)
#Window.clearcolor=(46/255,45/255,45/255,0.5)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Screens import DummyScreen
from Screens import MainScreen


class ConfigEditorApp(App):
    def build(self):
        pass


class Manager(ScreenManager):
    pass


if __name__ == '__main__':
    ConfigEditorApp().run()
