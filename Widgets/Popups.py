from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from Utils.Constants import Constants


class ImagePopup(Popup):
    def __init__(self, **kwargs):
        super(ImagePopup, self).__init__(**kwargs)
        self.source = None

    def init(self, source):
        self.source = source
        self.img.add_widget(AsyncImage(source=source))


class ChangePositionPopup(Popup):
    def __init__(self, **kwargs):
        super(ChangePositionPopup, self).__init__(**kwargs)
        self._parent = None

    def init(self, position):
        self.position.text = str(position)

    def set_parent(self, parent):
        self._parent = parent

    def change_cup_position(self):
        self._parent.change_cup_position(self.position.text)


class DeleteCupPopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteCupPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def delete_cup(self):
        self.dismiss()
        self._parent.delete_cup()


class NewCupPopup(Popup):
    def __init__(self, **kwargs):
        super(NewCupPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def add_cup(self):
        if len(self.name.text) == 0:
            self.error.text = Constants.ER_NAME_EMPTY
        elif len(self.position.text) == 0:
            self.error.text = Constants.ER_POSITION_EMPTY
        else:
            self._parent.add_new_cup(self.name.text, self.position.text)


class DeleteConfigPopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteConfigPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def delete_config(self):
        self._parent.delete_config()
