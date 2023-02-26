from kivymd.uix.stationdetails import ListMDDialogLocations
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from tourist_places import TouristPlaces


class TouristAttraction(FloatLayout):
    def populate(self, x, lat, lon):
        # Initializa class
        process_class = TouristPlaces()

        # lat = '51.767172'
        # lon = '19.455423'
        # Get 3 top places and return an array with only the place_id
        place_id_array = process_class.top_three_places_id(x, lat, lon)
        try:
            # Get details about first place
            first_place_json = process_class.check_place_details(place_id_array[0])
            first_place_formated_details = process_class.create_info_about_places(first_place_json)
            # Name
            self.ids.first_pick.text = first_place_formated_details[1]
            # Check the open times
            self.ids.first_pick_1.text = first_place_formated_details[2]
            # Address
            self.ids.first_pick_2.text = first_place_formated_details[3]
            # Review or summary
            self.ids.first_pick_3.text = first_place_formated_details[4]
            # Contact number
            self.ids.first_pick_4.text = first_place_formated_details[5]
            # Google maps url link
            self.url_first_place = first_place_formated_details[6]

            # print(f"First place: {first_place_formated_details}")
        except IndexError:
            self.url_first_place = 'https://www.google.com/maps'
            print('No more places found')

        try:
            # Get details about second place
            second_place_json = process_class.check_place_details(place_id_array[1])
            second_place_formated_details = process_class.create_info_about_places(second_place_json)
            print(f"second place: {second_place_formated_details}")
            # Name
            self.ids.second_pick.text = second_place_formated_details[1]
            # Check the open times
            self.ids.second_pick_1.text = second_place_formated_details[2]
            # Address
            self.ids.second_pick_2.text = second_place_formated_details[3]
            # Review or summary
            self.ids.second_pick_3.text = second_place_formated_details[4]
            # Contact number
            self.ids.second_pick_4.text = second_place_formated_details[5]
            # Google maps url link
            self.url_second_place = second_place_formated_details[6]
        except IndexError:
            self.url_second_place = 'https://www.google.com/maps'
            print('No more places found')

        try:
            # Get details about third place
            third_place_json = process_class.check_place_details(place_id_array[2])
            third_place_formated_details = process_class.create_info_about_places(third_place_json)
            print(f"third place: {third_place_formated_details}")

            # Name
            self.ids.third_pick.text = third_place_formated_details[1]
            # Check the open times
            self.ids.third_pick_1.text = third_place_formated_details[2]
            # Address
            self.ids.third_pick_2.text = third_place_formated_details[3]
            # Review or summary
            self.ids.third_pick_3.text = third_place_formated_details[4]
            # Contact number
            self.ids.third_pick_4.text = third_place_formated_details[5]
            # Google maps url link
            self.url_third_place = third_place_formated_details[6]
        except IndexError:
            self.url_third_place = 'https://www.google.com/maps'
            print('No more places found')


class SearchTourist(ListMDDialogLocations):
    title = 'Search by Address'
    categories = ['Museum', 'Amusement Park', 'Cafe', 'Restaurant', 'Bar', 'Supermarket']

    def __init__(self, lat, lon):
        super().__init__()
        self.size_hint = [0.9, 0.8]
        self.place_lat = lat
        self.place_lon = lon
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
            background_color=(144 / 255.0, 238 / 255.0, 144 / 255.0, 1),
            radius=[24, 0, 24, 0],
            elevation=4,
        )

        self.menu.open()

    def menu_callback(self, type_of_place):
        self.ids.menu_.text = type_of_place
        self.ids.help_info.text = ''
        # Check if the widget is already created
        if self.ids.container.children:
            # If the widget already exists, remove the current one
            self.ids.container.remove_widget(self.ids.container.children[0])
        # Create a new widget
        customwidget = TouristAttraction()
        # Add the new widget to the container
        self.ids.container.add_widget(customwidget)
        customwidget.populate(type_of_place, self.place_lat, self.place_lon)
        self.menu.dismiss()
