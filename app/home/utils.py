import numpy as np
import requests
import json
from app.config import GEOCODING_APIKEY
# from dotenv import load_dotenv

# # load_dotenv()

# GEOCODING_APIKEY=os.getenv('GEOCODING_APIKEY', None)
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
		return 0
	
