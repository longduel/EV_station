import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy_garden.mapview import MapView
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import ScreenManager, Screen
# Classes to inherit
from database_connector import DBConnection
from station_maker import StationMarker
from send_email import SendEmail

# Remove after testing to get the dynamic view
# Using the kivy.core.window set up the dynamic screen size
Window.size = (300, 500)


# Define Main Page
class MainWindow(Screen):
    pass


class SearchWindow(Screen):
    pass


# Define Button that is on the search list and will return the lat and lon to the map widget
class SelectedButton(MDFlatButton):

    def safe_name_of_search(self):

        # Clear the file
        with open("transfer.txt", "w"):
            pass
        # Write the search to the file
        with open("transfer.txt", "w", encoding="utf-8") as file:
            file.write(self.text)


# Define Map Page
class MapWindow(Screen, MapView, DBConnection):

    get_station_timer = None
    search_menu = None
    station_name = []

    # Return the size of the window so the map can dynamically resize and center on the specified position
    def get_size(self):
        return Window.size

    def set_up_gps(self):

        home_gps_blinker = self.ids.blinker
        home_gps_blinker.blink()

    """
    # Implementation for GPS device tracking
    # Request permissions on Android
        has_centered_map = False
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    from plyer import gps
                    gps.configure(on_location=self.update_blinker_position, on_status=self.on_auth_status)
                    gps.start(minTime=1000, minDistance=1)
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)
    def update_blinker_position(self, *args, **kwargs):
        # For testing purposes
        my_lat = 51.759445
        my_lon = 19.657216
        # Uncomment when ready and the app will be deployed
        #my_lat = kwargs['lat']
        #my_lon = kwargs['lon']
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position
        home_gps_blinker = self.ids.blinker
        home_gps_blinker.lat = my_lat
        home_gps_blinker.lon = my_lon

        # Center map on gps
        if not self.has_centered_map:
            self.lat = my_lat
            self.lon = my_lon
            self.zoom = 16
            self.has_centered_map = True

        MDApp.get_running_app().current_lat = my_lat
        MDApp.get_running_app().current_lon = my_lon

    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            print("Open gps access popup")
            try:
                self.open_gps_access_popup()
            except:
                print("error")
                pass

    def open_gps_access_popup(self):
        if not self.dialog:
            self.dialog = "STOP"
            Clock.schedule_once(self.run_dialog, 2)

    def run_dialog(self, *args):
        self.dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly",
                               size_hint=(0.5, 0.5))
        self.dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        self.dialog.open()
        self.dialog = None
    """
    def center_map_search(self):

        with open("transfer.txt", "r",  encoding="utf-8") as file:
            line = file.readline()

        if line == '':
            self.lat = 51.759445
            self.lon = 19.457216
            self.zoom = 11
        else:
            # Clear the file
            with open("transfer.txt", "w"):
                pass
            cursor = DBConnection()
            cursor.c.execute(f"SELECT * FROM stations_ev WHERE Name LIKE '%{line}%'")
            station = cursor.c.fetchall()
            self.lan_from_the_search = station[0][23]
            self.lon_from_the_search = station[0][24]

            self.lat = self.lan_from_the_search
            self.lon = self.lon_from_the_search
            self.zoom = 18

    def center_on_gps_location(self):
        # Get the lon and center values from the function arguments
        self.lat = 51.7714654904895
        self.lon = 19.483443589832355
        self.zoom = 16

    def center_map(self):
        # Get the lon and center values from the function arguments
        self.lat = 51.759445
        self.lon = 19.437216
        self.zoom = 10


    # Safeguard for user scrolling too much the position of the
    # Markers will not be updated constantly just every 1 second
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

        for station in stations:
            name = station[1]
            if name in self.station_name:
                continue
            else:
                self.sql_add_stations_to_map(station)

    def sql_add_stations_to_map(self, station):

        lat, lon = station[23], station[24]
        marker = StationMarker(lat=lat, lon=lon)

        marker.station_data = station

        # Populate the map with markers
        # Loop through the logic that will make the marker different if the station  have live availability

        if station[15] == 'NO':
            marker.source = "assets/image/marker_station.png"
            self.add_widget(marker)
        elif station[2] == 'OFFLINE':
            marker.source = "assets/image/marker_offline.png"
            self.add_widget(marker)
        else:
            marker.source = "assets/image/marker_online.png"
            self.add_widget(marker)

        name = station[1]

        self.station_name.append(name)


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


# Define Request Page
class NewStationWindow(Screen, SendEmail):

    # Refresh every on every exit
    def refresh(self):
        self.ids.spinner_id.text = "Pick Query"
        self.ids.full_name.text = " "
        self.ids.email.text = " "
        self.ids.additional_notes.text = " "

    # Handling error popups
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

    # Clear the file
    with open("transfer.txt", "w"):
        pass

    def build(self):
        self.title = "Test app"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        return Builder.load_file('EV_app.kv')


MainApp().run()
