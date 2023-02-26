from kivymd.uix.stationdetails import ListMDDialogLocations
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp

class TouristAttraction(FloatLayout):
    pass

class SearchTourist(ListMDDialogLocations):
    title = 'Search by Address'
    categories = ['Restaurant', 'Pub', 'Cinema']

    def __init__(self):
        super().__init__()
        self.size_hint = [0.9, 0.8]

    def drop_down(self):
        self.menu_drop = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "height": dp(60),
                "on_release": lambda x=f"{i}": self.menu_callback(x)
                # "text": "Ex 1",
                # "on_release": lambda x = "Example 1": self.test1(x),
            } for i in self.categories
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.menu_,
            items=self.menu_drop,
            position="bottom",
            width_mult=4,
            background_color=(0, 0, 1, 1),
            radius=[24, 0, 24, 0],
            elevation=4,
        )

        self.menu.open()

    def menu_callback(self, x):
        self.ids.menu_.text = x
        self.ids.help_info.text = ''
        customwidget = TouristAttraction()
        self.ids.container.add_widget(customwidget)
        self.menu.dismiss()