import os
import requests
import base64
from kivymd.uix.stationdetails import ListMDDialog
from tourist_location import SearchTourist
from full_screen_picture import Full_screen_picture
from kivy.network.urlrequest import UrlRequest


class LocationPopUp(ListMDDialog):
    picture_locations = ()

    def __init__(self, station_data):
        super().__init__()
        self.size_hint = [1, 1]

        # slicing the first element in the tuple that is the int kivy is only accepting the str
        station_data = station_data[1:]

        # Set all the fields of market data
        headers = "Name,Availability,Picture_Dir,Address,Service_contact,Type2,CCS,CHAdeMO,Type2_Voltage,CCS_Voltage,CHAdeMO_Voltage,Type2_num_plugs,CCS_num_plugs,CHAdeMO_num_plugs,Real_time_plug_in_availability,Parking_Slots,Operation_Hours,Price_Parking,Instruction_of_use,Play_Store_Icon,Play_Store_App,Additional_info"
        headers = headers.split(',')

        picture_headers = "Picture_1,Picture_2,Picture_3"
        picture_headers = picture_headers.split(',')

        # Read location of pictures and then put them into the station Carousel widget
        path = "assets//station_photo//1"
        picture_dir = os.listdir(station_data[2])

        picture_1 = f'{station_data[2]}//{picture_dir[0]}'
        picture_2 = f'{station_data[2]}//{picture_dir[1]}'
        picture_3 = f'{station_data[2]}//{picture_dir[2]}'

        self.picture_locations = (picture_1, picture_2, picture_3)

        if station_data[14] != 'NO':
            how_many_available = self.plugs_availability_rt(station_data[14], station_data[11])
            temp_station_data = list(station_data)
            temp_station_data[11] = how_many_available
            station_data = tuple(temp_station_data)

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
        tourist_menu = SearchTourist()
        tourist_menu.open()

    def full_view_picture(self):
        picture_menu = Full_screen_picture(self.picture_locations)
        picture_menu.open()

    def plugs_availability_rt(self, ID, all_plugs):

        try:
            # open the sample file used
            file = open('store.txt')
            # read the content of the file opened
            content = file.readlines()
            TomTom_api_key = base64.b64decode(content[1]).decode("utf-8")
            URL = f"https://api.tomtom.com/search/2/chargingAvailability.json?key={TomTom_api_key}&chargingAvailability={ID}"
            r = requests.get(url=URL)
            data = r.json()
            plug_live = data['connectors'][0]['availability']['current']['available']
            plugs_availability_formatted = f'{plug_live}/{all_plugs}'
            return plugs_availability_formatted
        except RuntimeError:
            print("Issues with API")

