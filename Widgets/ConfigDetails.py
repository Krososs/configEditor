from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView

from Utils.Constants import Constants
from Widgets.Popups import NewCupPopup, DeleteCupPopup, \
    DeleteConfigPopup, ChangePositionPopup

from Widgets.TreeView import PartTreeNode


class ConfigDetails(BoxLayout):

    def __init__(self, **kwargs):
        super(ConfigDetails, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self._parent = None
        self.selectedConfig = None
        self.selectedCup = None
        self.popup = None

    def set_parent(self, parent):
        self._parent = parent

    def set_config(self, config):
        self.selectedConfig = config

    def back_to_list(self):
        self.cup_options.clear_widgets()
        self._parent.show_config_list()

    def init(self):
        self.scrollview.scroll_y = 1
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()

        self.config_name.text = self.selectedConfig.name
        self.config_destination.text = self.selectedConfig.destination
        self.list_name.text = Constants.STR_CUPS

        self.layout.height = len(self.selectedConfig.cups) * 100
        for cup in self.selectedConfig.cups:
            cup.set_parent(self)
            cup.show_details()
            self.layout.add_widget(cup)
        self.scrollview.add_widget(self.layout)

    def add_new_cup(self, cup_name, cup_position):

        if self.selectedConfig.config_includes_cup(cup_name):
            self.popup.error.text = \
                Constants.ER_CUP_NAME_TAKEN
        elif self.selectedConfig.position_taken(cup_position):
            self.popup.error.text = Constants.ER_POSITION_TAKEN
        else:
            self.popup.dismiss()
            self.selectedConfig.add_cup(cup_name, int(cup_position))
            self.init()

    def change_cup_position(self, new_position):
        if len(new_position) == 0:
            self.popup.error.text = Constants.ER_POSITION_EMPTY
        elif new_position == str(self.selectedCup.position):
            self.popup.dismiss()
        elif self.selectedConfig.position_taken(new_position):
            self.popup.error.text = Constants.ER_POSITION_TAKEN
        else:
            self.popup.dismiss()
            self.selectedCup.set_position(int(new_position))
            self.selectedConfig.save()
            self.update_list_details()

    def delete_cup(self):
        self.selectedConfig.delete_cup(self.selectedCup.name)
        self.init()

    def delete_config(self):
        if self.selectedConfig.is_default():
            self.popup.error.text = \
                Constants.ER_DELETE_DEFAULT
        else:
            self.popup.dismiss()
            self.selectedConfig.delete()
            self._parent.show_config_list()

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

    def back_to_cup_list(self, instance):
        self.cup_options.clear_widgets()
        self.init()

    def add_cup_options(self):
        self.cup_options.clear_widgets()
        change_position = Button(text=Constants.STR_CHANGE_POSITION, size_hint=(.25,
                                                                                1),
                                 background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        change_position.bind(on_press=self.open_position_popup)

        delete_cup = Button(text=Constants.STR_DELETE, size_hint=(.25, 1),
                            background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        delete_cup.bind(on_press=self.open_delete_cup_popup)

        back_button = Button(text=Constants.STR_BACK, size_hint=(.25, 1),
                             background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        back_button.bind(on_press=self.back_to_cup_list)

        self.cup_options.add_widget(back_button)
        self.cup_options.add_widget(change_position)
        self.cup_options.add_widget(delete_cup)

    def show_cup_details(self, cup):
        self.selectedCup = cup
        self.update_list_details()
        self.scrollview.scroll_y = 1
        self.add_cup_options()
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()

        _tree = TreeView(hide_root=True)
        counter = 0
        for c in self._parent.categories:
            node = PartTreeNode(text=c['Name'], source=None)
            n = _tree.add_node(node)
            child = PartTreeNode(text="partBlank", source=None)
            node.set_tree(_tree, n, c['Parts'], child)
            node.set__parent(self)
            if self.cup_contains_category(c['Parts']):
                node.checkbox.active = True
            _tree.add_node(child, n)
            counter += 1
        self.layout.height = counter * dp(55)
        self.layout.add_widget(_tree)
        self.scrollview.add_widget(self.layout)

    def update_list_details(self):
        self.list_name.text = self.selectedCup.name + " (" + str(
            len(self.selectedCup.parts)) + ") " + " position: " + str(self.selectedCup.position)

    def resize(self, height):
        self.layout.height += height

    def get_parts(self):
        return self.selectedCup.parts

    def add_parts(self, parts):
        for b in parts:
            self.selectedCup.add_part(b)
        self.update_list_details()
        self.selectedConfig.save()

    def remove_parts(self, bricks):
        for b in bricks:
            self.selectedCup.remove_part(b)
        self.update_list_details()
        self.selectedConfig.save()

    def cup_contains_category(self, parts):
        for part in parts:
            if not self.selectedCup.contains_part(part['part_num']):
                return False
        return True
