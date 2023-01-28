from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.treeview import TreeViewNode
from kivy.uix.image import AsyncImage

from Widgets.Popups import ImagePopup


class PartNode(BoxLayout):

    def __init__(self, **kwargs):
        self.text = kwargs.pop('text', 'None')
        self.source = kwargs.pop('source', 'None')
        super(PartNode, self).__init__(**kwargs)

        self.height = dp(55)
        self.child_table = []
        self.image = None
        self._parent = None
        self.parent_category = None
        if self.source is not None:
            self.image = AsyncImage(source=self.source)
            self.image.bind(on_touch_down=self.show_image)

        # make the parts of the node
        self.lbl = Label(text=self.text, size_hint_x=0.45)
        self.checkbox = CheckBox(size_hint=(.55, 1), color=(1, 1, 1, 3.5))
        self.checkbox.bind(on_press=lambda instance: self.select_all_children())
        self.empty = BoxLayout()

        # add the parts to the BoxLayout
        self.add_widget(BoxLayout(size_hint=(.25, 1)))
        self.add_widget(self.lbl)
        if self.source is not None:
            self.add_widget(self.image)
        self.add_widget(self.checkbox)
        self.add_widget(self.empty)

    def show_image(self, widget, touch):
        popup = ImagePopup()
        popup.init(self.source)
        popup.open()

    def set_checkbox(self, active):
        self.checkbox.active = active

    def select_all_children(self):
        parts = []
        if len(self.child_table) == 0:
            self.init()
        for ch in self.child_table:
            ch.set_checkbox(self.checkbox.active)
            parts.append(ch.text)
        if self.checkbox.active:
            if len(self.child_table) == 0:
                parts.append(self.text)
                if self.parent_category.all_children_selected():
                    self.parent_category.set_checkbox(True)
            self._parent.add_parts(parts)
        else:
            if len(self.child_table) == 0:
                parts.append(self.text)
                self.parent_category.set_checkbox(False)
            self._parent.remove_parts(parts)

    def add___child(self, child):
        self.child_table.append(child)


class PartTreeElement(PartNode, TreeViewNode):
    def set__parent(self, parent):
        self._parent = parent

    def set_parent_category(self, parent_category):
        self.parent_category = parent_category

    def init(self):
        pass


class PartTreeNode(PartNode, TreeViewNode):
    def __init__(self, **kwargs):
        super(PartTreeNode, self).__init__(**kwargs)
        self.bind(is_open=self._expand)
        self.node = None
        self.tree = None
        self.parts = []
        self.blank = None

    def _expand(self, object, isOpen):
        if isOpen:
            if len(self.child_table) == 0:
                self.init()
            self.resize()
        else:
            self._parent.resize(-(len(self.child_table) * self.height))

    def set__parent(self, parent):
        self._parent = parent

    def set_tree(self, tree, node, parts, blank):
        self.tree = tree
        self.node = node
        self.parts = parts
        self.blank = blank

    def all_children_selected(self):
        for ch in self.child_table:
            if not ch.checkbox.active:
                return False
        return True

    def resize(self):
        self._parent.resize(len(self.child_table) * self.height)

    def init(self):
        self.tree.remove_node(self.blank)
        selected_parts = self._parent.get_parts()
        for part in self.parts:
            if part['print_of'] is None:
                child = PartTreeElement(text=part['part_num'], source=part['part_img_url'])
                child.set__parent(self._parent)
                child.set_parent_category(self)
                self.add___child(child)
                self.tree.add_node(child, self.node)
                if part['part_num'] in selected_parts:
                    child.checkbox.active = True
