from kivy.uix.screenmanager import Screen
from Utils import LegoUtil
from Utils.Constants import Constants
from Utils.Database import Database

class ApiScreen(Screen):
    pass

    def save_api_key(self):
        self.ids.error.text = Constants.EMPTY
        if LegoUtil.valid_key(self.ids.key.text):
            LegoUtil.save_key(self.ids.key.text)
            if Database.database_exist():
                self.manager.current = Constants.SCREEN_BASIC
            else:
                self.manager.current = Constants.SCREEN_LOADING
        else:
            self.ids.error.text = Constants.ER_KEY_INVALID
