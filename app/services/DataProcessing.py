import numpy as np
import pandas as pd
import re
from dataclasses import dataclass, asdict
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer

from flask import current_app
from app.home.forms import SurveyForm, FormData, Rental
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径，单位为公里
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d

def form_to_vecs(form_data):
    # 获取表单数据
    desired_price_min = form_data.minprice
    desired_price_max = form_data.maxprice
    desired_roomtype = form_data.roomtype
    desired_month = form_data.desired_month
    desired_latitude, desired_longitude = form_data.location
    form_data.convert_amenities_to_input()
    user_amenities_input = form_data.vector
    weights = form_data.get_normalized_weights()
    
    # 计算期望价格
    desired_price = (desired_price_min + desired_price_max) / 2

    # 初始化列名
    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    selected_amenities = [amenities_columns[i] for i, val in enumerate(user_amenities_input) if val == 1]
    roomtype_col = "room_type_" + desired_roomtype
    data_cols = ['HouseID'] + selected_amenities + ['latitude', 'longitude', 'room_type', 'price', 'minimum_months', 'maximum_months']

    # 从数据库获取数据
    data = current_app.data_manager.get_houses_df(data_cols)
    data = data.replace({True: 1, False: 0})

    # 过滤数据
    filtered_data = data[(data['maximum_months'] >= desired_month) & (data['minimum_months'] <= desired_month)]

    # One-hot编码房间类型
    encoder = OneHotEncoder(sparse=False)
    onehot = encoder.fit_transform(filtered_data[['room_type']])
    onehot_df = pd.DataFrame(onehot, columns=encoder.get_feature_names_out(['room_type']))
    filtered_data = pd.concat([filtered_data.reset_index(drop=True), onehot_df.reset_index(drop=True)], axis=1)


    price_scaler = RobustScaler()
    distance_scaler = RobustScaler()
    # 计算距离

    weight_distance = 2
    inverse_weight_distance=1/(weight_distance + 1e-5)  # 加一个小的常数防止除以0
    filtered_data['distance'] = haversine_distance(desired_latitude, desired_longitude, filtered_data['latitude'], filtered_data['longitude'])
    filtered_data['inverse_distance'] = 1 / (filtered_data['distance'] + 1e-5)
    filtered_data['similarity_distance'] = distance_scaler.fit_transform(filtered_data['inverse_distance'].values.reshape(-1, 1))
    similarity_weight_distance=distance_scaler.transform(np.array(inverse_weight_distance).reshape(-1, 1))[0, 0]
    

    # max_base_pricediff = desired_price_max - desired_price_min  
    max_base_pricediff=200
    weight_pricediff = max_base_pricediff * (1 - weights['price'])
    inverse_weight_pricediff=1/weight_pricediff  
    

    # 计算价格差异
    filtered_data['price_difference'] = abs(filtered_data['price'] - desired_price)
    filtered_data['reciprocal_price_difference'] = 1 / (filtered_data['price_difference'] + 1e-5)
    filtered_data['normalized_reciprocal_price_difference'] = price_scaler.fit_transform(filtered_data['reciprocal_price_difference'].values.reshape(-1, 1))
    similarity_weight_pricediff=price_scaler.transform(np.array(inverse_weight_pricediff).reshape(-1, 1))[0, 0]


    # 计算权重
    amenities_weights = [weights['amenities'] / len(selected_amenities)] * len(selected_amenities)
    room_type_weight_per_feature = weights['room_type'] / len([roomtype_col])
    weight_vector = amenities_weights  + [weights['distance']] + [room_type_weight_per_feature] + [weights['price']]

    # 构建用户向量
    user_room_type = [1 if roomtype == roomtype_col else -1 for roomtype in [roomtype_col]]
    user_vector_w = np.array([1] * len(selected_amenities) + [similarity_weight_distance] + user_room_type + [similarity_weight_pricediff])

    # 构建数据向量
    vector_cols = selected_amenities + ['similarity_distance'] + [roomtype_col] + ['normalized_reciprocal_price_difference', 'HouseID']
    data_vector = filtered_data[vector_cols]

    return weight_vector, user_vector_w, data_vector

def df_to_am(df):
    categories = {
        'public_facilities': ['BBQ', 'gym', 'pool', 'Backyard'],
        'cooking_facilities': ['kitchen', 'refrigerator', 'Microwave', 'Oven', 'stove'],
        'interior_facilities': ['conditioning', 'dryer', 'Wifi', 'TV', 'fan'],
        'other_needs': ['Pets']
    }

    # 初始化结果字典
    result_dict = {category: [] for category in categories}

    # 遍历每一行
    for index, row in df.iterrows():
        # 遍历每个设施分类
        for category, facilities in categories.items():
            # 遍历分类中的每个设施
            for facility in facilities:
                # 如果设施的值为1，添加到结果字典中
                if row[facility] == 1:
                    result_dict[category].append(facility)
    return result_dict


def vector_to_amenities(vector):
    categories = [
        ['aircon', 'BBQ', 'gym'],  # 第一类设施
        ['pool', 'dryer', 'Wifi'],  # 第二类设施
        ['kitchen', 'Backyard', 'TV', 'refrigerator'],  # 第三类设施
        ['Microwave', 'Oven', 'Pets', 'stove', 'fan']  # 第四类设施
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

def df_to_display(row_num,raw):
    amenities_list=df_to_amenities(raw)
    room_info = str(getattr(raw, 'details'))
    cleaned_room_info = re.sub(r'\?\?+', '. ', room_info)
    rental=Rental(
        id=str(getattr(raw, 'HouseID')),
        title=str(getattr(raw, 'HouseName')),
        facility_type=str(getattr(raw, 'room_type')),
        accommodation_info=str(getattr(raw, 'accommodates'))+" accommodate",
        room_info=cleaned_room_info,
        public_facilities=amenities_list[0],
        cooking_facilities=amenities_list[1],
        interior_facilities=amenities_list[2],
        other_needs=amenities_list[3],
        price="S$ "+ str(getattr(raw, 'price'))+ "/month",
        distance_to_mrt=str(int(getattr(raw, 'distance_to_mrt')*1000)) + "m to " + str(getattr(raw, 'closest_mrt_name')),
        mall_info=str(int(getattr(raw, 'closest_mall_distance')*1000)) + "m to " + str(getattr(raw, 'closest_mall_name')) + "(" + str(getattr(raw, 'closest_mall_address')) + ")",
        lat=str(getattr(raw, 'latitude')),
        lng=str(getattr(raw, 'longitude')),
        location_info=None,
        location_href="./map/" + str((row_num)),
        img_src=str(getattr(raw, 'picture_url'))
    )
    rental.get_location_info()
    rental_dic=asdict(rental)
    return rental_dic

class drawerConfig:
    poi_columns = ['store', 'food', 'health', 'restaurant', 'hospital', 'lodging', 'finance', 'cafe', 'convenience_store', 
               'clothing_store', 'atm', 'shopping_mall', 'grocery_or_supermarket', 'home_goods_store', 'school', 
               'bakery', 'beauty_salon', 'transit_station', 'place_of_worship', 'pharmacy', 'meal_takeaway', 
               'furniture_store', 'tourist_attraction', 'secondary_school', 'supermarket', 'doctor', 'shoe_store', 
               'dentist', 'jewelry_store', 'church', 'bank', 'primary_school', 'electronics_store', 'gym', 'spa', 
               'car_repair', 'pet_store', 'bus_station', 'university', 'park', 'general_contractor', 'subway_station', 
               'real_estate_agency', 'florist', 'hair_care', 'department_store', 'hardware_store', 'car_dealer', 
               'veterinary_care', 'travel_agency', 'bicycle_store', 'book_store', 'laundry', 'plumber', 
               'meal_delivery', 'lawyer', 'parking', 'mosque', 'physiotherapist', 'art_gallery', 'insurance_agency', 
               'bar', 'museum', 'storage', 'movie_theater', 'moving_company', 'liquor_store', 'gas_station', 
               'electrician', 'car_rental', 'locksmith', 'car_wash', 'post_office', 'embassy', 'night_club', 
               'fire_station', 'amusement_park', 'library', 'hindu_temple', 'local_government_office', 
               'funeral_home', 'bowling_alley', 'cemetery', 'aquarium', 'roofing_contractor', 'stadium', 'painter', 
               'courthouse', 'drugstore', 'campground', 'accounting', 'airport', 'zoo', 'casino', 'synagogue', 
               'premise', 'taxi_stand', 'police', 'light_rail_station', 'city_hall', 'train_station', 
               'natural_feature', 'subpremise']
    semantic_groups = {
        'store_group': ['store', 'shopping_mall', 'grocery_or_supermarket', 'convenience_store', 'clothing_store', 'home_goods_store', 'electronics_store', 'department_store', 'furniture_store'],
        'food_group': ['food', 'restaurant', 'cafe', 'bakery', 'meal_takeaway'],
        'health_group': ['health', 'hospital', 'pharmacy', 'doctor', 'dentist', 'physiotherapist'],
        'finance_group': ['finance', 'atm', 'bank', 'insurance_agency'],
        'education_group': ['school', 'secondary_school', 'primary_school', 'university'],
        'transportation_group': ['transit_station', 'bus_station', 'subway_station', 'taxi_stand', 'train_station', 'light_rail_station'],
        'entertainment_group': ['movie_theater', 'amusement_park', 'bowling_alley', 'casino', 'night_club'],
        'culture_group': ['museum', 'art_gallery', 'library', 'hindu_temple', 'church', 'mosque', 'synagogue'],
        'recreation_group': ['park', 'gym', 'spa', 'stadium', 'zoo', 'aquarium'],
        'services_group': ['laundry', 'plumber', 'lawyer', 'post_office', 'car_wash', 'embassy', 'police', 'funeral_home', 'moving_company']
    }


    colors = ['#8B0000', '#DC143C', '#FF7F50', '#CD5C5C', '#FA8072', '#FF8C00', '#FFD700', '#A52A2A', '#FF6347', '#FFA07A']