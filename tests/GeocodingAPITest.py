# import googlemaps
import os
from dotenv import load_dotenv
import numpy as np
import requests
import json

load_dotenv()
GEOCODING_APIKEY=os.getenv('GEOCODING_APIKEY', None)


# def get_geocoding(location):
#     gmaps = googlemaps.Client(key=GEOCODING_APIKEY)
#     # Geocoding an address
#     #geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#     geocode_result = gmaps.geocode(location)

#     location=geocode_result[0]["geometry"]["location"]
#     result= np.array([location["lat"],location["lng"]])
    
#     return result

# gmaps = googlemaps.Client(key=GEOCODING_APIKEY)
# #     # Geocoding an address
# #geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# geocode_result = gmaps.geocode("loction")
# print(geocode_result)

def get_geocoding(location):
	url = f'https://maps.googleapis.com/maps/api/geocode/json'
	parameters = {
		'address': location,
		'components': 'country:SG',
        # 'region':"sg",
		'key': GEOCODING_APIKEY
	}
	response = requests.get(url, params = parameters)
	if response.status_code == 200:
		data = json.loads(response.text)
		if (data["status"]=="OK") & (data["results"][0]["formatted_address"]!="Singapore"):
			geocoding=data["results"][0]["geometry"]["location"]
			result=np.array([geocoding["lat"],geocoding["lng"]])
			return result
		else:
			print("Invalid query")
			return 1
	else:
		print('Request failed with status code:', response.status_code)
		return 1
	
def get_reverseGeocoding(coordinates):
	url = f'https://maps.googleapis.com/maps/api/geocode/json'
	formatted_string = '{},{}'.format(coordinates[0], coordinates[1])
	parameters = {
		'latlng': formatted_string,
		'key': GEOCODING_APIKEY
	}
	response = requests.get(url, params = parameters)
	if response.status_code == 200:
		data = json.loads(response.text)
		if data["status"]=="OK" :
			result=data["results"][0]["formatted_address"]
			return result
		else:
			print("Invalid query")
			return 1
	else:
		print('Request failed with status code:', response.status_code)
		return 0

if __name__ == "__main__":
	# test=get_geocoding("shanghai")
	# coordinates=np.array([1.2966426, 103.7763939])  # nus
	coordinates=np.array([1.36288, 103.86575])
	test=get_reverseGeocoding(coordinates)
	print(test)