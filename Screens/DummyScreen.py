import pickle
import os
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.clock import Clock
from Utils.Database import Database


class DummyScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_screen)

    def switch_screen(self, dt):
        self.manager.transition = NoTransition()

        if not os.path.exists('././settings.cfg'):
            data = dict(default='None', API_KEY='None')
            print(data)
            with open('././settings.cfg', 'wb') as f:
                pickle.dump(data, f)

        with open('././settings.cfg', 'rb') as f:
            data = pickle.load(f)

        if data['API_KEY'] == 'None':
            self.manager.current = "api"
        else:
            if not Database.database_exist():
                self.manager.current = "loading"
            else:
                self.manager.current = "basic"
