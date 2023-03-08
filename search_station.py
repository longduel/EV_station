from kivy.uix.recycleview import RecycleView
import sqlite3

class RV(RecycleView):

    try:
        connection = sqlite3.connect('EV_Station_Data.db')
        print("Search Page DB Connection Established")
    except ConnectionError as exc:
        raise RuntimeError('Failed to open database') from exc

        # Creating cursor for executing statements
    c = connection.cursor()

    c.execute(f"SELECT * FROM stations_ev")
    station_name = []
    stations = c.fetchall()
    for station in stations:
        name = station[1]
        station_name.append(name)

    def on_kv_post(self, base_widget):
        self.init_data()

    def init_data(self):
        # initialize the data for the recycleview
        self.data = [{'text': f'{i}'} for i in self.station_name]

    def search_rv(self, text):

        if not text:
            self.init_data()
        else:
            self.data = [x for x in self.data if text.upper() in x['text'].upper()]
