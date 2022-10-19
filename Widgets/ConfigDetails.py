import pickle

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from Widgets.Popups import NewBrickPopup, NewCupPopup, DeleteCupPopup, \
    DeleteConfigPopup, ChangePositionPopup, DeleteBrickPopup

from Objects.Brick import Brick


class ConfigDetails(BoxLayout):

    def __init__(self, **kwargs):
        super(ConfigDetails, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self._parent = None
        self.config = None
        self.selectedCup = None
        self.selected_brick = None
        self.popup = None

        self.conveyor_address_ph = None
        self.conveyor_port_ph = None
        self.sorter_address_ph = None
        self.sorter_port_ph = None

    def set_parent(self, parent):
        self._parent = parent

    def set_config(self, config):
        self.config = config
        self.conveyor_address.text = self.config.conveyor_address
        self.conveyor_port.text = self.config.conveyor_port
        self.sorter_address.text = self.config.sorter_address
        self.sorter_port.text = self.config.sorter_port

    # addresses change
    def change_conveyor_address(self, text):
        if text != self.config.conveyor_address:
            self.save_button.disabled = False
            self.conveyor_address_ph = text

    def change_conveyor_port(self, text):
        if text != self.config.conveyor_port:
            self.save_button.disabled = False
            self.conveyor_port_ph = text

    def change_sorter_address(self, text):
        if text != self.config.sorter_address:
            self.save_button.disabled = False
            self.sorter_address_ph = text

    def change_sorter_port(self, text):
        if text != self.config.sorter_port:
            self.save_button.disabled = False
            self.sorter_port_ph = text

    def save_changes(self):
        self.config.set_address('conveyor_address',
                                self.conveyor_address_ph)
        self.config.set_address('conveyor_port', self.conveyor_port_ph)
        self.config.set_address('sorter_address',
                                self.sorter_address_ph)
        self.config.set_address('sorter_port', self.sorter_port_ph)
        self.config.save()

    def back_to_list(self):
        self._parent.show_config_list()

    def init(self):
        self.save_button.disabled = True
        self.scrollview.scroll_y = 1
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()

        self.config_name.text = self.config.name
        self.list_name.text = 'Cups'

        if self.config.is_default():
            self.config_name.text += ' (Default)'
            self.default_button.disabled = True
        else:
            self.default_button.disabled = False

        self.layout.height = len(self.config.cups) * 100
        for cup in self.config.cups:
            cup.set_parent(self)
            cup.show_details()
            self.layout.add_widget(cup)
        self.scrollview.add_widget(self.layout)

    def set_brick(self, brick):
        self.selected_brick = brick
        self.open_delete_brick_popup()

    def delete_brick(self):  # set
        self.selectedCup.delete_brick(self.selected_brick)
        self.config.save()
        self.selectedCup.show_details()
        self.show_cup_details(self.selectedCup)

    def add_new_brick(self, brick):
        if self.config.cup_includes_brick(self.selectedCup.name, brick):
            self.popup.error.text = \
                'Cup already contains selected brick'
        else:
            self.config.add_brick(self.selectedCup.name, brick)
            self.show_cup_details(self.selectedCup)

    def add_new_cup(self, cupName, cupPosition):

        if self.config.config_includes_cup(cupName):
            self.popup.error.text = \
                'Config already contains cup with given name'
        elif self.config.position_taken(cupPosition):
            self.popup.error.text = 'Position is already taken'
        else:
            self.popup.dismiss()
            self.config.add_cup(cupName, int(cupPosition))
            self.init()

    def change_cup_position(self, newPosition):
        if len(newPosition) == 0:
            self.popup.error.text = 'Position can not be empty'
        elif newPosition == str(self.selectedCup.position):
            self.popup.dismiss()
        elif self.config.position_taken(newPosition):
            self.popup.error.text = 'Position is already taken'
        else:
            self.popup.dismiss()
            self.selectedCup.set_position(int(newPosition))
            self.config.save()
            self.selectedCup.show_details()
            self.show_cup_details(self.selectedCup)

    def delete_cup(self):
        self.config.delete_cup(self.selectedCup.name)
        self.init()

    def delete_config(self):
        if self.config.is_default():
            self.popup.error.text = \
                'You can not delete default config'
        else:
            self.popup.dismiss()
            self.config.delete()
            self._parent.show_config_list()

    # Config option buttons
    def set_config_as_default(self):
        data = dict(default=self.config.name)
        with open('././settings.cfg', 'wb') as f:
            pickle.dump(data, f)

    def open_new_cup_popup(self):
        self.popup = NewCupPopup()
        self.popup.set_parent(self)
        self.popup.open()

    def open_delete_config_popup(self):
        self.popup = DeleteConfigPopup()
        self.popup.set_parent(self)
        self.popup.open()

    # Cup option buttons
    def open_position_popup(self, instance):
        self.popup = ChangePositionPopup()
        self.popup.set_parent(self)
        self.popup.init(self.selectedCup.position)
        self.popup.open()

    def open_delete_cup_popup(self, instance):
        self.popup = DeleteCupPopup()
        self.popup.set_parent(self)
        self.popup.open()

    def open_new_brick_popup(self, instance):
        self.popup = NewBrickPopup()
        self.popup.set_parent(self)
        self.popup.init()
        self.popup.open()

    def open_delete_brick_popup(self):
        self.popup = DeleteBrickPopup()
        self.popup.set_parent(self)
        self.popup.open()

    def back_to_cup_list(self, instance):
        self.cup_options.clear_widgets()
        self.init()

    def add_cup_options(self):
        self.cup_options.clear_widgets()
        changePosition = Button(text='Change position', size_hint=(.25,
                                                                   1))
        changePosition.bind(on_press=self.open_position_popup)

        deleteCup = Button(text='Delete', size_hint=(.25, 1))
        deleteCup.bind(on_press=self.open_delete_cup_popup)

        addBrick = Button(text='Add brick', size_hint=(.25, 1))
        addBrick.bind(on_press=self.open_new_brick_popup)

        backButton = Button(text='Back', size_hint=(.25, 1))
        backButton.bind(on_press=self.back_to_cup_list)

        self.cup_options.add_widget(backButton)
        self.cup_options.add_widget(changePosition)
        self.cup_options.add_widget(deleteCup)
        self.cup_options.add_widget(addBrick)

    def show_cup_details(self, cup):  # TODO
        self.selectedCup = cup
        self.list_name.text = self.selectedCup.name + " (" + str(len(self.selectedCup.bricks)) + ")"
        self.scrollview.scroll_y = 1
        self.add_cup_options()
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()
        self.layout.height = len(cup.bricks) * 100

        for brick in cup.bricks:
            b = Brick()
            b.set_parent(self)
            b.init(brick)
            self.layout.add_widget(b)
        self.scrollview.add_widget(self.layout)
