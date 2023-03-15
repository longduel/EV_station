from kivy.uix.recycleview import RecycleView
import sqlite3
# Class created for purpose of creating search window with all the stations available ohn local database


class RV(RecycleView):

    try:
        connection = sqlite3.connect('EV_Station_Data.db')
        print("Search Page DB Connection Established")
    except ConnectionError as exc:
        raise RuntimeError('Failed to open database') from exc

    # Creating cursor for executing statements
    c = connection.cursor()

    # Taking all the station names
    c.execute(f"SELECT * FROM stations_ev")
    station_name = []
    stations = c.fetchall()
    for station in stations:
        name = station[1]
        station_name.append(name)

    # Create buttons on the list with station names
    def on_kv_post(self, base_widget):
        self.init_data()

    # Initialize the data for the recycleview
    def init_data(self):
        self.data = [{'text': f'{i}'} for i in self.station_name]

    # Search based on the text input
    def search_rv(self, text):

        if not text:
            self.init_data()
        else:
            self.data = [x for x in self.data if text.upper() in x['text'].upper()]
