from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from Utils import LegoUtil
from Utils.Database import Database


class LoadingScreen(Screen):
    pass

    def on_enter(self):
        self.get_category_trigger = Clock.create_trigger(self.get_category)
        self.categories = LegoUtil.get_part_categories()
        self.cat_arr = []
        self.i = 0
        self.get_category_trigger()

    def get_category(self, dt):
        if self.i < len(self.categories):
            self.ids.progress.value = self.i
            category = {
                'Id': self.categories[self.i]['id'],
                'Name': self.categories[self.i]['name'],
                'Parts': LegoUtil.get_parts(self.categories[self.i]['id'])
            }
            self.cat_arr.append(category)
            self.i += 1
            self.get_category_trigger()
        else:
            Database.create_databse(self.cat_arr)
            self.manager.current = 'basic'