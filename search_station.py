from kivy.uix.recycleview import RecycleView
from database_connector import DBConnection
from kivymd.uix.stationdetails import ListMDDialogSearch

class SearchPopupMenu(ListMDDialogSearch, RecycleView, DBConnection):

    station_name = []
    title = 'Search by Address'
    text_button_ok = 'Search'
    def __init__(self):
        super().__init__()
        self.size_hint = [.9, .2]
        self.pos_hint = {"center_x": 0.5, "center_y": 0.75}

class RV(RecycleView, ListMDDialogSearch):

    def on_kv_post(self, base_widget):
        self.init_data()

    def init_data(self):
        # initialize the data for the recycleview
        self.c.execute(f"SELECT * FROM stations_ev")
        stations = self.c.fetchall()
        for station in stations:
            name = station[1]
            self.station_name.append(name)
        self.data = [{'text': f'{i}'} for i in self.station_name]

    def search_rv(self, text):
        if not text:
            self.init_data()
        else:
            self.data = [x for x in self.data if text.upper() in x['text'].upper()]