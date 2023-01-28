from kivy.uix.screenmanager import Screen
from Utils import LegoUtil


class ApiScreen(Screen):
    pass

    def save_api_key(self):
        self.ids.error.text = ""
        if LegoUtil.valid_key(self.ids.key.text):
            LegoUtil.save_key(self.ids.key.text)
            self.manager.current = 'loading'
        else:
            self.ids.error.text = "Provided key is invalid"
