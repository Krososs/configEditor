from kivy.config import Config

Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', 0)
# Window.clearcolor=(46/255,45/255,45/255,0.5)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from Screens.DummyScreen import DummyScreen
from Screens.MainScreen import MainScreen

Builder.load_file("ConfigEditorApp.kv")
screen_manager = ScreenManager()
screen_manager.add_widget(DummyScreen())
screen_manager.add_widget(MainScreen())


class ConfigEditorApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    ConfigEditorApp().run()
