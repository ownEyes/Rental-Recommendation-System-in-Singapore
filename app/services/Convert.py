from flask import current_app
import requests
import pandas as pd
from sklearn.neighbors import KDTree
from sklearn.preprocessing import OneHotEncoder
import numpy as np


def get_geocoding(region,postcode):
        GEOCODING_APIKEY=current_app.config['GEOCODING_APIKEY']
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        parameters = {
            'address': region+", Singapore"+postcode,
            'components': 'country:SG',
            'key': GEOCODING_APIKEY
        }
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and data["results"][0]["formatted_address"] != "Singapore":
                geocoding = data["results"][0]["geometry"]["location"]
                return [geocoding["lat"], geocoding["lng"]]
            else:
                print("Invalid query")
                return [1.352083,103.819836]
        else:
            print('Request failed with status code:', response.status_code)
            return [1.352083,103.819836]
        
def amenities_to_vector(amenities_list):
    reference_list = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    vector = [0] * len(reference_list)
    amenity_mapping = {
        'microwave': 'Microwave',
        'pets': 'Pets',
        'backyard': 'Backyard',
        'oven': 'Oven',
        'stoven': 'stove'
    }
    for amenities in amenities_list:
        for amenity in amenities:
            standardized_amenity = amenity_mapping.get(amenity, amenity)
            if standardized_amenity in reference_list:
                vector[reference_list.index(standardized_amenity)] = 1
    return vector

def cal_mrt_dis(geocoding):
    
    df = current_app.data_manager.get_mrts_df(['latitude','longitude','name','stop_id'])
    coords = df[['Latitude', 'Longitude']].values
    tree = KDTree(coords, leaf_size=2, metric='haversine')
    point = np.array([geocoding])
    distances, indices = tree.query(point, k=2)
    distances_km = distances * 6371
    nearest_stations = df.iloc[indices[0]]
    return distances_km,nearest_stations

def cal_mall_dis(geocoding):
    df = current_app.data_manager.get_malls_df(['latitude','longitude','name','formatted_address'])
    coords = df[['Latitude', 'Longitude']].values
    tree = KDTree(coords, leaf_size=2, metric='haversine')
    point = np.array([geocoding])
    distances, indices = tree.query(point, k=2)
    distances_km = distances * 6371
    nearest_malls = df.iloc[indices[0]]
    return distances_km,nearest_malls
    

def get_house_data(input):
    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    data_cols = ['HouseID'] +['neighbourhood_group_cleansed','latitude', 'longitude', 'room_type', 'minimum_months', 'maximum_months','distance_to_mrt','closest_mall_distance','accommodates']+amenities_columns + ['total_bedrooms','total_beds','total_baths','bath_type']
    data = current_app.data_manager.get_houses_df(data_cols)
    data = data.replace({True: 1, False: 0})
    encoder = OneHotEncoder(sparse=False)
    onehot = encoder.fit_transform(data[['neighbourhood_group_cleansed','room_type','bath_type']])
    data_dropped = data.drop(columns=['neighbourhood_group_cleansed', 'room_type', 'bath_type'])
    onehot_df = pd.DataFrame(onehot, columns=encoder.get_feature_names(['neighbourhood_group_cleansed', 'room_type', 'bath_type']))
    final_data = pd.concat([data_dropped, onehot_df], axis=1)
    
    input_dict = [input]  
    input_df = pd.DataFrame(input_dict)

    onehot_input = encoder.transform(input_df[['neighbourhood_group_cleansed', 'room_type', 'bath_type']])
    onehot_input_df = pd.DataFrame(onehot_input, columns=encoder.get_feature_names(['neighbourhood_group_cleansed', 'room_type', 'bath_type']))

    input_df_dropped = input_df.drop(columns=['neighbourhood_group_cleansed', 'room_type', 'bath_type'])

    final_input_df = pd.concat([input_df_dropped, onehot_input_df], axis=1)
    return final_data,final_input_df.values

def vector_to_amenities(vector):
    categories = [
        ['aircon', 'BBQ', 'gym'],  
        ['pool', 'dryer', 'Wifi'],  
        ['kitchen', 'Backyard', 'TV', 'refrigerator'], 
        ['Microwave', 'Oven', 'Pets', 'stove', 'fan'] 
    ]
    
    amenities_list = [[] for _ in range(4)]
    flat_categories = [item for sublist in categories for item in sublist]
    
    for i, value in enumerate(vector):
        if value == 1:
            for j, category in enumerate(categories):
                if flat_categories[i] in category:
                    amenities_list[j].append(flat_categories[i])
                    break
                
    return amenities_list

def df_to_amenities(raw):
    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    amenities_values = [getattr(raw, col) for col in amenities_columns]
    amenities_list = vector_to_amenities(amenities_values)
    return amenities_list

def house_to_draw(row_num,raw):
    amenities_list=df_to_amenities(raw)
    s1=[str(getattr(raw, 'HouseName')),
        str(getattr(raw, 'details')),
        str(getattr(raw, 'neighbourhood_group_cleansed')),
        str(getattr(raw, 'accommodates'))+'accommodate',
        str(getattr(raw, 'room_type')),
        str(amenities_list[0]),
        str(amenities_list[1]),
        str(amenities_list[2]),
        str(amenities_list[3]),
        "S$ "+ str(getattr(raw, 'price'))+ "/month",
        str(int(getattr(raw, 'distance_to_mrt')*1000)) + "m to " + str(getattr(raw, 'closest_mrt_name')),
        str(int(getattr(raw, 'closest_mall_distance')*1000)) + "m to " + str(getattr(raw, 'closest_mall_name')) + "(" + str(getattr(raw, 'closest_mall_address')) + ")",
        getattr(raw, 'latitude'),
        getattr(raw, 'longitude')
        ]
    return s1