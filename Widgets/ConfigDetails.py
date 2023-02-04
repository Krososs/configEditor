from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView

from Utils.Constants import Constants
from Widgets.Popups import NewContainerPopup, DeleteContainerPopup, \
    DeleteConfigPopup, ChangePositionPopup

from Widgets.TreeView import PartTreeNode


class ConfigDetails(BoxLayout):

    def __init__(self, **kwargs):
        super(ConfigDetails, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self._parent = None
        self.selected_config = None
        self.selected_container = None
        self.popup = None

    def set_parent(self, parent):
        self._parent = parent

    def set_config(self, config):
        self.selected_config = config

    def back_to_list(self):
        self.container_options.clear_widgets()
        self._parent.show_config_list()

    def init(self):
        self.scrollview.scroll_y = 1
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()

        self.config_name.text = self.selected_config.name
        self.config_destination.text = self.selected_config.destination
        self.list_name.text = Constants.STR_CONTAINERS

        self.layout.height = len(self.selected_config.containers) * 100
        for container in self.selected_config.containers:
            container.set_parent(self)
            container.show_details()
            self.layout.add_widget(container)
        self.scrollview.add_widget(self.layout)

    def add_new_container(self, container_name, container_position):

        if self.selected_config.config_includes_container(container_name):
            self.popup.error.text = \
                Constants.ER_CONTAINER_NAME_TAKEN
        elif self.selected_config.position_taken(container_position):
            self.popup.error.text = Constants.ER_POSITION_TAKEN
        else:
            self.popup.dismiss()
            self.selected_config.add_containers(container_name, int(container_position))
            self.init()

    def change_container_position(self, new_position):
        if len(new_position) == 0:
            self.popup.error.text = Constants.ER_POSITION_EMPTY
        elif new_position == str(self.selected_container.position):
            self.popup.dismiss()
        elif self.selected_config.position_taken(new_position):
            self.popup.error.text = Constants.ER_POSITION_TAKEN
        else:
            self.popup.dismiss()
            self.selected_container.set_position(int(new_position))
            self.selected_config.save()
            self.update_list_details()

    def delete_container(self):
        self.selected_config.delete_container(self.selected_container.name)
        self.init()

    def delete_config(self):
        self.popup.dismiss()
        self.selected_config.delete()
        self._parent.show_config_list()

    def open_new_container_popup(self):
        self.popup = NewContainerPopup()
        self.popup.set_parent(self)
        self.popup.open()

    def open_delete_config_popup(self):
        self.popup = DeleteConfigPopup()
        self.popup.set_parent(self)
        self.popup.open()

    # Container option buttons
    def open_position_popup(self, instance):
        self.popup = ChangePositionPopup()
        self.popup.set_parent(self)
        self.popup.init(self.selected_container.position)
        self.popup.open()

    def open_delete_container_popup(self, instance):
        self.popup = DeleteContainerPopup()
        self.popup.set_parent(self)
        self.popup.open()

    def back_to_container_list(self, instance):
        self.container_options.clear_widgets()
        self.init()

    def add_container_options(self):
        self.container_options.clear_widgets()
        change_position = Button(text=Constants.STR_CHANGE_POSITION, size_hint=(.25,
                                                                                1),
                                 background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        change_position.bind(on_press=self.open_position_popup)

        delete_container = Button(text=Constants.STR_DELETE, size_hint=(.25, 1),
                                  background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        delete_container.bind(on_press=self.open_delete_container_popup)

        back_button = Button(text=Constants.STR_BACK, size_hint=(.25, 1),
                             background_color=(46 / 255, 45 / 255, 45 / 255, 1))
        back_button.bind(on_press=self.back_to_container_list)

        self.container_options.add_widget(back_button)
        self.container_options.add_widget(change_position)
        self.container_options.add_widget(delete_container)

    def show_container_details(self, container):
        self.selected_container = container
        self.update_list_details()
        self.scrollview.scroll_y = 1
        self.add_container_options()
        self.layout.clear_widgets()
        self.scrollview.clear_widgets()

        _tree = TreeView(hide_root=True)
        counter = 0
        for c in self._parent.categories.find():
            node = PartTreeNode(text=c['Name'], source=None)
            n = _tree.add_node(node)
            child = PartTreeNode(text="partBlank", source=None)
            node.set_tree(_tree, n, c['Parts'], child)
            node.set__parent(self)
            if self.container_contains_category(c['Parts']):
                node.checkbox.active = True
            _tree.add_node(child, n)
            counter += 1
        print(str(counter))
        self.layout.height = counter * dp(55)
        self.layout.add_widget(_tree)
        self.scrollview.add_widget(self.layout)

    def update_list_details(self):
        self.list_name.text = self.selected_container.name + " (" + str(
            len(self.selected_container.parts)) + ") " + " position: " + str(self.selected_container.position)

    def resize(self, height):
        self.layout.height += height

    def get_parts(self):
        return self.selected_container.parts

    def add_parts(self, parts):
        for b in parts:
            self.selected_container.add_part(b)
        self.update_list_details()
        self.selected_config.save()

    def remove_parts(self, bricks):
        for b in bricks:
            self.selected_container.remove_part(b)
        self.update_list_details()
        self.selected_config.save()

    def container_contains_category(self, parts):
        for part in parts:
            if not self.selected_container.contains_part(part['part_num']):
                return False
        return True
