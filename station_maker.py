from kivy_garden.mapview import MapMarkerPopup
from locationpopout import LocationPopUp
from database_connector import DBConnection

class StationMarker(MapMarkerPopup):

    # Open StationWindow Page
    # source = "assets/image/bolt.png"
    station_data = []

    def on_release(self):

        menu = LocationPopUp(self.station_data)
        menu.size_hint = [.95, .9]
        menu.open()
