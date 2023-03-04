import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy_garden.mapview import MapView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
# Classes to inherit
from database_connector import DBConnection
from station_maker import StationMarker
from send_email import SendEmail
from search_stations import SearchPopup
# Remove after testing to get the dynamic view
Window.size = (300, 500)  # Using the kivy.core.window set up the dynamic screen size


# Define Main Page
class MainWindow(Screen):
    pass

# Define Map Page
class MapWindow(Screen, MapView, DBConnection):

    get_station_timer = None
    search_menu = None
    station_name = []

    # Return the size of the window so the map can dynamically resize and center on the specified position
    def get_size(self):
        return Window.size

    def center_on_gps_location(self):
        # Get the lon and center values from the function arguments
        self.lat = 51.759445
        self.lon = 19.657216
        self.zoom = 15

    def centers_map(self):
        self.lat = 51.759445
        self.lon = 19.457216
        self.zoom = 10

    # safeguard for user scrolling too much the position of the
    # markers will not be updated constantly just every 1 second
    def set_station_markers(self):
        try:
            self.get_station_timer.cancel()
        except:
            pass

        self.get_station_timer = Clock.schedule_once(self.get_stations, 1)

    def get_stations(self, *args):
        # Get reference to main app and the database cursor
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        self.c.execute(
            f"SELECT * FROM stations_ev WHERE LAT > {min_lon} AND LAT < {max_lon} AND LON > {min_lat} AND LON < {max_lat}")
        stations = self.c.fetchall()
        # print(len(stations))
        for station in stations:
            name = station[1]
            if name in self.station_name:
                continue
            else:
                self.sql_add_stations_to_map(station)

    def sql_add_stations_to_map(self, station):

        # print(len(station))
        lat, lon = station[23], station[24]
        marker = StationMarker(lat=lat, lon=lon)

        marker.station_data = station
        self.add_widget(marker)

        name = station[1]

        self.station_name.append(name)

    def search_stations(self):

        search_menu = SearchPopup()
        search_menu.open()


# Define About Page DELETE WHEN DONE!!!!!!!!!
class StationWindow(Screen, DBConnection):

    def get_name(self):
        i = 2
        self.c.execute(f"SELECT * FROM stations_ev WHERE id = {i}")
        text = self.c.fetchone()
        self.ids.calc_input.text = f'{text[1]}'
        return text


# Define About Page
class AboutWindow(Screen):
    def show_contact_details(self):
        popup = Popup(
            title='Feel free to contact us via email if you have any questions:\n\nEV.lodz.help@gmail.com',
            background_color=(0, 1, 0, 1),
            separator_color=(0, 0, 0, 0),
            # opacity=0.5,
            title_align='center',
            size_hint=(0.7, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        popup.open()


# Define Search Station Page
class SearchStation(Screen):
    def refresh(self):
        self.ids.text_field_error.text = " "


# Define Request Page
class NewStationWindow(Screen, SendEmail):

    def refresh(self):
        self.ids.spinner_id.text = "Pick Query"
        self.ids.full_name.text = " "
        self.ids.email.text = " "
        self.ids.additional_notes.text = " "

    def popup_invalid_submit(self, popup_text, move_popup):
        popup = Popup(title=f'{popup_text}',
                      background_color=(1, 0, 0, 1),
                      # opacity=0.5,
                      overlay_color=(0, 0, 0, 0),
                      title_align='center',
                      separator_color=(1, 0, 0, 1),
                      size_hint=(0.7, 0.12),
                      pos_hint={'center_x': 0.5, 'center_y': move_popup})
        popup.open()

    def popup_valid_submit(self):
        popup = Popup(title='Email send successfully',
                      background_color=(0, 1, 0, 1),
                      # opacity=0.5,
                      overlay_color=(0, 0, 0, 0),
                      title_align='center',
                      separator_color=(0, 1, 0, 1),
                      size_hint=(0.7, 0.12),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        popup.open()

    def check_input(self, name, user_email, selected, additional_n):
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        regex_full_name = r'^[a-zA-Z]{4,}(?: [a-zA-Z]+){0,2}$'
        valid_name_text = 'Invalid full name provided.'
        valid_email_text = 'Invalid email address.'
        valid_choice_spinner = 'Please pick your query.'
        valid_additional_text = 'Additional notes empty.'
        check_table = []
        check_table_correct = ['OK', 'OK', 'OK', 'OK']

        # Create notifications
        if re.fullmatch(regex_full_name, name):
            check_table.append('OK')
        else:
            self.popup_invalid_submit(valid_name_text, 0.8)
        if re.fullmatch(regex_email, user_email):
            check_table.append('OK')
        else:
            self.popup_invalid_submit(valid_email_text, 0.66)
        if selected != 'Pick Query':
            check_table.append('OK')
        else:
            self.popup_invalid_submit(valid_choice_spinner, 0.52)
        if additional_n != '':
            check_table.append('OK')
        else:
            self.popup_invalid_submit(valid_additional_text, 0.38)

        # Check if the notifications are correct
        if check_table == check_table_correct:
            print('OK')
            return True
        else:
            print('Wrong')
            return False

    def send_email_button(self):
        name = self.ids.full_name.text
        user_email = self.ids.email.text
        selected = self.ids.spinner_id.text
        additional_n = self.ids.additional_notes.text

        if self.check_input(name, user_email, selected, additional_n):
            self.popup_valid_submit()
            self.set_up_connection(name, user_email, selected, additional_n)
        else:
            print('not ok')


# Main ScreenManager function that controls the change of the screen
class WindowManager(ScreenManager):
    pass


# Main class that will build the application
# Builder is for the .kv file to load as the Kivy Graphic Design
class MainApp(MDApp):

    def build(self):
        self.title = "Test app"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        return Builder.load_file('EV_app.kv')


MainApp().run()
