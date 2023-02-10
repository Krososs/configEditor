from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
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

    def change_container_position(self):
        self._parent.change_container_position(self.position.text)


class DeleteContainerPopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteContainerPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def delete_container(self):
        self.dismiss()
        self._parent.delete_container()


class NewContainerPopup(Popup):
    def __init__(self, **kwargs):
        super(NewContainerPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def add_container(self):
        if len(self.name.text) == 0:
            self.error.text = Constants.ER_NAME_EMPTY
        elif len(self.position.text) == 0:
            self.error.text = Constants.ER_POSITION_EMPTY
        else:
            self._parent.add_new_container(self.name.text, self.position.text)


class DeleteConfigPopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteConfigPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def delete_config(self):
        self._parent.delete_config()


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
