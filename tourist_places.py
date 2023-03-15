import requests
import base64
from datetime import datetime
# Class created for sorting through the Google API call

class TouristPlaces:

    def create_info_about_places(self, j):

        def display_opening_hours_based_on_day(argument):
            # When using strftime('%w') to get the deciaml of the day it is starting
            # from Sunday as 0 and ends at Saturday as 6
            match argument:
                case '0':
                    open_hours_day = j['current_opening_hours']['weekday_text'][6]
                    return open_hours_day
                case '1':
                    open_hours_day = j['current_opening_hours']['weekday_text'][0]
                    return open_hours_day
                case '2':
                    open_hours_day = j['current_opening_hours']['weekday_text'][1]
                    return open_hours_day
                case '3':
                    open_hours_day = j['current_opening_hours']['weekday_text'][2]
                    return open_hours_day
                case '4':
                    open_hours_day = j['current_opening_hours']['weekday_text'][3]
                    return open_hours_day
                case '5':
                    open_hours_day = j['current_opening_hours']['weekday_text'][4]
                    return open_hours_day
                case '6':
                    open_hours_day = j['current_opening_hours']['weekday_text'][5]
                    return open_hours_day
                case default:
                    open_hours_day = 'Cannot find data for specific today opening hours.'
                    return open_hours_day

        # Create and clear the table at each iteration
        place_info = []

        # Extract boolean to check if the place is open right now or not
        try:
            is_it_open = j['current_opening_hours']['open_now']
            place_info.append(is_it_open)
        except KeyError:
            place_info.append('No information about availability.')

        # Extract Name of the place
        try:
            name = j['name']
            place_info.append(name)
        except KeyError:
            place_info.append('No place name found.')

        # Extract open time of the place
        try:
            check_what_day = datetime.now().date()
            formatted_day_number = check_what_day.strftime('%w')
            opening_hours_on_day = display_opening_hours_based_on_day(formatted_day_number)
            place_info.append(opening_hours_on_day)
        except KeyError:
            place_info.append('No information about availability today.')

        # Extract address
        try:
            address = j['formatted_address']
            place_info.append(address)
        except KeyError:
            place_info.append('No address name found.')

        # Extract quick summary if there is one or first review of the user
        try:
            place_summary = j['editorial_summary']['overview']
            place_info.append(place_summary)
        except KeyError:
            try:
                author_name_review = f"Review by:{j['reviews'][0]['author_name']}, {j['reviews'][0]['text']}"
                place_info.append(author_name_review)
            except KeyError:
                place_info.append('No place summary found')

        # Extract contact number
        try:
            contact_number = j['formatted_phone_number']
            place_info.append(contact_number)
        except KeyError:
            place_info.append('No contact number')

        # Extract URL for Google Maps button
        try:
            map_url = j['url']
            place_info.append(map_url)
        except KeyError:
            place_info.append('No url for location found.')

        # print(place_info)
        return place_info

    def top_three_places_id(self, category_choice, lat, lon):

        # open the sample file used
        file = open('store.txt')
        # read the content of the file opened
        content = file.readlines()
        google_places_api_key = base64.b64decode(content[2]).decode("utf-8")
        # Category processing lower case and change empty space to underscore for the url
        category_choice = category_choice.lower()
        category_choice = category_choice.replace(' ', '_')
        print(category_choice)
        # place_type = input('Please provide the type of place:')
        # Send the API request and get the response data
        print(category_choice)
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&type={category_choice}&radius=1000&rankby=prominence&key={google_places_api_key}"
        response = requests.get(url)

        response_json = response.json()

        if 'results' in response_json:
            places = response_json['results']
            sorted_places = sorted(places, key=lambda place: place.get('rating', 0) if 'rating' in place else 0,
                                   reverse=True)
            # Take the top 3 results
            top_places = sorted_places[:3]
            # Create array to only store places_id after sort
            top_place_ids = [place.get('place_id') for place in top_places]
            return top_place_ids
        else:
            print('No results found.')

    def check_place_details(self, place_id):

        # open the sample file used
        file = open('store.txt')
        # read the content of the file opened
        content = file.readlines()
        google_places_api_key = base64.b64decode(content[2]).decode("utf-8")
        # Print all fields for each of the top 3 places
        print(f"\nDetails for top place {place_id}")
        URL = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={google_places_api_key}"
        response = requests.get(URL)
        details = response.json()['result']
        return details
