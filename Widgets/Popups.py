from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class NewBrickPopup(Popup):
    def __init__(self, **kwargs):
        super(NewBrickPopup, self).__init__(**kwargs)
        self._parent = None
        self.selectedCategory = None
        self.selectedSubCategory = None
        self.categoryButton = Button(text='Select category', size_hint=(.6, .5), height=60,
                                     pos_hint={'x': .2, 'y': .25})
        self.categoryDropdown = DropDown()
        self.subCategoryButton = Button(text='Select sub category', size_hint=(.6, .5), height=60,
                                        pos_hint={'x': .2, 'y': .25})
        self.subCategoryDropdown = DropDown()

    def set_parent(self, parent):
        self._parent = parent

    def init(self):
        self.init_category()
        self.init_sub_category()

    def select_category(self, instance, category):
        self.categoryButton.text = category
        self.selectedCategory = category

    def select_sub_category(self, instance, sub_category):
        self.subCategoryButton.text = sub_category
        self.selectedSubCategory = sub_category

    def init_category(self):
        self.category.clear_widgets()
        self.categoryDropdown.clear_widgets()

        self.categoryButton.bind(on_release=self.categoryDropdown.open)
        self.categoryDropdown.bind(on_select=lambda instance, x: self.select_category(instance, x))
        self.category.add_widget(self.categoryButton)

        for i in range(10):  # get brick categories
            btn = Button(text='Category % d' % i, size_hint_y=None, height=40)  # Label?
            btn.bind(on_release=lambda btn: self.categoryDropdown.select(btn.text))
            self.categoryDropdown.add_widget(btn)

    def init_sub_category(self):
        self.subCategory.clear_widgets()
        self.subCategoryDropdown.clear_widgets()

        self.subCategoryButton.bind(on_release=self.subCategoryDropdown.open)
        self.subCategoryDropdown.bind(on_select=lambda instance, x: self.select_sub_category(instance, x))
        self.subCategory.add_widget(self.subCategoryButton)

        for i in range(10):  # get sub categories
            btn = Button(text='421', size_hint_y=None, height=40)  # Label?
            btn.bind(on_release=lambda btn: self.subCategoryDropdown.select(btn.text))
            self.subCategoryDropdown.add_widget(btn)

        btn = Button(text='1', size_hint_y=None, height=40)  # Label?
        btn.bind(on_release=lambda btn: self.subCategoryDropdown.select(btn.text))
        self.subCategoryDropdown.add_widget(btn)

        btn = Button(text='2', size_hint_y=None, height=40)  # Label?
        btn.bind(on_release=lambda btn: self.subCategoryDropdown.select(btn.text))
        self.subCategoryDropdown.add_widget(btn)

        btn = Button(text='3', size_hint_y=None, height=40)  # Label?
        btn.bind(on_release=lambda btn: self.subCategoryDropdown.select(btn.text))
        self.subCategoryDropdown.add_widget(btn)

        btn = Button(text='4', size_hint_y=None, height=40)  # Label?
        btn.bind(on_release=lambda btn: self.subCategoryDropdown.select(btn.text))
        self.subCategoryDropdown.add_widget(btn)

    def save_new_brick(self):
        if self.selectedSubCategory is None:
            self.error.text = "Select the correct category"
        else:
            self.dismiss()
            self._parent.add_new_brick(self.subCategoryButton.text)


class DeleteBrickPopup(Popup):
    def __init__(self, **kwargs):
        super(DeleteBrickPopup, self).__init__(**kwargs)
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def delete_brick(self):
        self.dismiss()
        self._parent.delete_brick()


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
            self.error.text = "Name can not be empty"
        elif len(self.position.text) == 0:
            self.error.text = "Position can not be empty"
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
