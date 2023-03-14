import os
import requests
import base64
from kivymd.uix.stationdetails import ListMDDialog
from tourist_location import SearchTourist
from full_screen_picture import Full_screen_picture


class LocationPopUp(ListMDDialog):
    picture_locations = ()

    def __init__(self, station_data):
        super().__init__()
        self.size_hint = [1, 1]

        # slicing the first element in the tuple that is the int kivy is only accepting the str
        station_data = station_data[1:]

        # Take lat and lon for the reference in the Tourist search window
        self.lat = station_data[22]
        self.lon = station_data[23]

        # Set all the fields of market data
        headers = "Name,Availability,Picture_Dir,Address,Service_contact,Type2,CCS,CHAdeMO,Type2_Voltage,CCS_Voltage,CHAdeMO_Voltage,Type2_num_plugs,CCS_num_plugs,CHAdeMO_num_plugs,Real_time_plug_in_availability,Parking_Slots,Operation_Hours,Price_Parking,Instruction_of_use,Play_Store_Icon,Play_Store_App,Additional_info"
        headers = headers.split(',')

        picture_headers = "Picture_1,Picture_2,Picture_3"
        picture_headers = picture_headers.split(',')

        # Read location of pictures and then put them into the station Carousel widget
        path = "assets//station_photo//1"
        picture_dir = os.listdir(station_data[2])

        try:
            picture_1 = f'{station_data[2]}//{picture_dir[0]}'
            picture_2 = f'{station_data[2]}//{picture_dir[1]}'
            picture_3 = f'{station_data[2]}//{picture_dir[2]}'

            self.picture_locations = (picture_1, picture_2, picture_3)

        except IndexError:
            picture_1 = "assets//image//No_photo.png"
            picture_2 = "assets//image//No_photo.png"
            picture_3 = "assets//image//No_photo.png"

            self.picture_locations = (picture_1, picture_2, picture_3)
            print('Lest pictures than 3')

        if station_data[14] != 'NO':
            temp_station_data = list(station_data)
            how_many_available = self.plugs_availability_rt(temp_station_data)
            station_data = tuple(how_many_available)

        for i in range(len(headers)):
            attribute_name = headers[i]
            attribute_value = station_data[i]
            #print(attribute_name + " " + attribute_value)
            setattr(self, attribute_name, attribute_value)

        for i in range(len(picture_headers)):
            attribute_picture_name = picture_headers[i]
            attribute_pictures_value = self.picture_locations[i]
            setattr(self, attribute_picture_name, attribute_pictures_value)

    def tourist_search(self):
        tourist_menu = SearchTourist(self.lat, self.lon)
        tourist_menu.open()

    def full_view_picture(self):
        picture_menu = Full_screen_picture(self.picture_locations)
        picture_menu.open()

    def plugs_availability_rt(self, one_station_table):

        try:
            # make original to return if there is an issue with the API
            backup_station_data = one_station_table
            # take ID for the API call from the station record
            ID = one_station_table[14]
            # open the sample file used
            file = open('store.txt')
            # read the content of the file opened
            content = file.readlines()
            # decode KPI key
            TomTom_api_key = base64.b64decode(content[1]).decode("utf-8")
            URL = f"https://api.tomtom.com/search/2/chargingAvailability.json?key={TomTom_api_key}&chargingAvailability={ID}"
            r = requests.get(url=URL)
            data = r.json()
            # check every type of plug
            self.check_live_type2(data, one_station_table)
            self.check_live_ccs(data, one_station_table)
            self.check_live_chademo(data, one_station_table)

            return one_station_table

        except IndexError:
            return backup_station_data
            print("Issue with indexing")

        except RuntimeError:
            return backup_station_data
            print("Issues with API")

    def check_live_type2(self, json_exctract, station):

        try:
            type2_plug_total = json_exctract['connectors'][0]['total']
            type2_plug_available = json_exctract['connectors'][0]['availability']['current']['available']
            plug_availability_formatted = f'{type2_plug_available}/{type2_plug_total}'
            station[11] = plug_availability_formatted
        except IndexError:
            pass

    def check_live_ccs(self, json_exctract, station):

        try:
            css_plug_total = json_exctract['connectors'][2]['total']
            css_plug_available = json_exctract['connectors'][2]['availability']['current']['available']
            plug_availability_formatted = f'{css_plug_available}/{css_plug_total}'
            station[12] = plug_availability_formatted
        except IndexError:
            pass

    def check_live_chademo(self, json_exctract, station):

        try:
            chademo_plug_total = json_exctract['connectors'][1]['total']
            chademo_plug_available = json_exctract['connectors'][1]['availability']['current']['available']
            plug_availability_formatted = f'{chademo_plug_available}/{chademo_plug_total}'
            station[13] = plug_availability_formatted
        except IndexError:
            pass
