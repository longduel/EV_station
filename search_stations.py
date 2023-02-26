from kivymd.uix.stationdetails import MDInputDialog
from database_connector import DBConnection
from kivy.uix.recycleview import RecycleView

class SearchPopup(MDInputDialog, DBConnection):
    title = 'Search by Address'
    text_button_ok = 'Search'
    station_name = []

    def __init__(self):
        super().__init__()
        self.size_hint = [.9, .3]
        self.events_callback = self.callback

    def take_lon_lat(self):
        self.c.execute(f"SELECT * FROM stations_ev")
        stations = self.c.fetchall()
        for station in stations:
            name = station[1]
            self.station_name.append(name)
        print(self.station_name)

    def callback(self, *args):
        self.take_lon_lat()


class RV(RecycleView):
    def on_kv_post(self, base_widget):
        self.init_data()

    def init_data(self):
        # initialize the data for the recycleview
        self.data = [{'text': f'{i}'} for i in range(1000)]

    def search_rv(self, text):
        if not text:
            self.init_data()
        else:
            self.data = [x for x in self.data if text in x['text']]
