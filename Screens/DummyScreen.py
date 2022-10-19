from kivy.uix.screenmanager import Screen, NoTransition
from kivy.clock import Clock


class DummyScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_screen)

    def switch_screen(self, dt):
        self.manager.transition = NoTransition()
        self.manager.current = "basic"
