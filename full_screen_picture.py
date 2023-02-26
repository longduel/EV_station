from kivymd.uix.stationdetails import ListMDDialogFullPicture

class Full_screen_picture(ListMDDialogFullPicture):

    def __init__(self, picture_locations):
        super().__init__()
        self.size_hint = [0.85, 0.85]

        headers = "Picture_1,Picture_2,Picture_3"
        headers = headers.split(',')

        for i in range(len(headers)):
            attribute_name = headers[i]
            attribute_value = picture_locations[i]
            setattr(self, attribute_name, attribute_value)
