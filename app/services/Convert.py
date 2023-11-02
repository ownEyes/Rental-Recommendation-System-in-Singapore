from flask import current_app
import requests
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import KDTree
from haversine import haversine, Unit
from sklearn.preprocessing import OneHotEncoder, RobustScaler, LabelEncoder
import numpy as np
import re
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


def get_geocoding(region, postcode):
    GEOCODING_APIKEY = current_app.config['GEOCODING_APIKEY']
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
            return [1.352083, 103.819836]
    else:
        print('Request failed with status code:', response.status_code)
        return [1.352083, 103.819836]


def amenities_to_vector(amenities_list):
    reference_list = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen',
                      'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
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

    df = current_app.data_manager.get_mrts_df(
        ['latitude', 'longitude', 'name', 'stop_id'])
    coords = df[['latitude', 'longitude']].values
    tree = KDTree(coords, leafsize=2)

    point = np.array([geocoding])

    _, index = tree.query(point, k=1)
    nearest_station = df.iloc[index[0]]
    distance_km = haversine(
        geocoding, (nearest_station.loc['latitude'], nearest_station.loc['longitude']), unit=Unit.KILOMETERS)
    return distance_km, nearest_station


def cal_mall_dis(geocoding):
    df = current_app.data_manager.get_malls_df(
        ['latitude', 'longitude', 'name', 'formatted_address'])
    coords = df[['latitude', 'longitude']].values
    tree = KDTree(coords, leafsize=2)

    point = np.array([geocoding])

    _, index = tree.query(point, k=1)
    nearest_mall = df.iloc[index[0]]

    distance_km = haversine(
        geocoding, (nearest_mall.loc['latitude'], nearest_mall.loc['longitude']), unit=Unit.KILOMETERS)
    return distance_km, nearest_mall


def get_house_data(input, price):
    desired_pricediff = 50
    inverse_desired_pricediff = 1/desired_pricediff
    input['price'] = inverse_desired_pricediff
    # input['price'] = price
    input_dict = [input]
    input_df = pd.DataFrame(input_dict)
    # input_df = input_df.drop(
    #     ['distance_to_mrt', 'closest_mall_distance'], axis=1)

    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen',
                         'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    # data_cols = ['HouseID'] +['neighbourhood_group_cleansed','latitude', 'longitude', 'room_type', 'minimum_months', 'maximum_months','distance_to_mrt','closest_mall_distance','accommodates']+amenities_columns + ['total_bedrooms','total_beds','total_baths','bath_type']
    data_cols = ['HouseID'] + ['price', 'neighbourhood_group_cleansed', 'latitude', 'longitude', 'room_type', 'minimum_months',
                               'maximum_months', 'accommodates', 'distance_to_mrt', 'closest_mall_distance']+amenities_columns + ['total_bedrooms', 'total_beds', 'total_baths', 'bath_type']
    data = current_app.data_manager.get_houses_df(data_cols)
    data = data.replace({True: 1, False: 0})
    data['price'] = abs(data['price']-price)
    data['price'] = 1/(data['price'] + 1e-5)
    # data = data[data['neighbourhood_group_cleansed'] ==
    #             input_df['neighbourhood_group_cleansed'].iloc[0]]

    # data = data.drop(['neighbourhood_group_cleansed'], axis=1)
    # input_df = input_df.drop(['neighbourhood_group_cleansed'], axis=1)

    label_encoder = LabelEncoder()
    data['bath_type'] = label_encoder.fit_transform(data['bath_type'])
    input_df['bath_type'] = label_encoder.transform(input_df['bath_type'])

    data = data.drop(['bath_type'], axis=1)
    input_df = input_df.drop(['bath_type'], axis=1)

    data = data.reset_index(drop=True)

    encoder = OneHotEncoder(sparse=False)
    onehot = encoder.fit_transform(
        data[['neighbourhood_group_cleansed', 'room_type']])

    data_dropped = data.drop(
        columns=['neighbourhood_group_cleansed', 'room_type'])
    onehot_df = pd.DataFrame(
        onehot, columns=encoder.get_feature_names_out(['neighbourhood_group_cleansed', 'room_type']))
    onehot_df = onehot_df.reset_index(drop=True)
    final_data = pd.concat([data_dropped, onehot_df], axis=1)

    onehot_input = encoder.transform(
        input_df[['neighbourhood_group_cleansed', 'room_type']])
    onehot_input_df = pd.DataFrame(
        onehot_input, columns=encoder.get_feature_names_out(['neighbourhood_group_cleansed', 'room_type']))
    input_df_dropped = input_df.drop(
        columns=['neighbourhood_group_cleansed', 'room_type'])
    final_input_df = pd.concat([input_df_dropped, onehot_input_df], axis=1)

    # onehot = encoder.fit_transform(
    #     data[['room_type', 'bath_type']])
    # data_dropped = data.drop(
    #     columns=['room_type', 'bath_type'])
    # onehot_df = pd.DataFrame(onehot, columns=encoder.get_feature_names_out(
    #     ['room_type', 'bath_type']))
    # onehot_df = onehot_df.reset_index(drop=True)
    # final_data = pd.concat([data_dropped, onehot_df], axis=1)

    # onehot_input = encoder.transform(
    #     input_df[['room_type', 'bath_type']])
    # onehot_input_df = pd.DataFrame(onehot_input, columns=encoder.get_feature_names_out(
    #     ['room_type', 'bath_type']))

    columns_to_scale = ['price', 'latitude', 'longitude',
                        'minimum_months', 'maximum_months', 'accommodates', 'distance_to_mrt', 'closest_mall_distance', 'total_bedrooms', 'total_beds', 'total_baths']

# Fit the scaler on final_data and transform both final_data and final_input_df
    scaler = RobustScaler()
    for col in columns_to_scale:
        final_data[col] = scaler.fit_transform(final_data[[col]])
        final_input_df[col] = scaler.transform(final_input_df[[col]])

    # encoder = OneHotEncoder(sparse=False)
    # onehot = encoder.fit_transform(
    #     data[['neighbourhood_group_cleansed', 'room_type', 'bath_type']])
    # data_dropped = data.drop(
    #     columns=['neighbourhood_group_cleansed', 'room_type', 'bath_type'])
    # onehot_df = pd.DataFrame(onehot, columns=encoder.get_feature_names_out(
    #     ['neighbourhood_group_cleansed', 'room_type', 'bath_type']))
    # final_data = pd.concat([data_dropped, onehot_df], axis=1)

    # onehot_input = encoder.transform(
    #     input_df[['neighbourhood_group_cleansed', 'room_type', 'bath_type']])
    # onehot_input_df = pd.DataFrame(onehot_input, columns=encoder.get_feature_names_out(
    #     ['neighbourhood_group_cleansed', 'room_type', 'bath_type']))

    # input_df_dropped = input_df.drop(
    #     columns=['neighbourhood_group_cleansed', 'room_type', 'bath_type'])

    # final_input_df = pd.concat([input_df_dropped, onehot_input_df], axis=1)
    return final_data, final_input_df


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
    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen',
                         'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    amenities_values = [getattr(raw, col) for col in amenities_columns]
    amenities_list = vector_to_amenities(amenities_values)
    return amenities_list


def house_to_draw(row_num, raw):
    amenities_list = df_to_amenities(raw)
    room_info = str(getattr(raw, 'details'))
    cleaned_room_info = re.sub(r'\?\?+', '. ', room_info)
    s1 = [str(getattr(raw, 'HouseName')),
          cleaned_room_info,
          str(getattr(raw, 'neighbourhood_group_cleansed')),
          str(getattr(raw, 'accommodates'))+'accommodate',
          str(getattr(raw, 'room_type')),
          amenities_list[0],
          amenities_list[1],
          amenities_list[2],
          amenities_list[3],
          "S$ " + str(getattr(raw, 'price')) + "/month",
          str(int(getattr(raw, 'distance_to_mrt')*1000)) +
          "m to " + str(getattr(raw, 'closest_mrt_name')),
          str(int(getattr(raw, 'closest_mall_distance')*1000)) + "m to " + str(getattr(raw,
                                                                                       'closest_mall_name')) + "(" + str(getattr(raw, 'closest_mall_address')) + ")",
          getattr(raw, 'latitude'),
          getattr(raw, 'longitude')
          ]
    return s1


def find_similar(data, user_preference):
    user_preference.rename(columns={'conditioning': 'aircon'}, inplace=True)
    cols = user_preference.columns.tolist()
    data_filtered = data[cols]

    nbrs = NearestNeighbors(
        n_neighbors=10, algorithm='ball_tree').fit(data_filtered)
    distances, indices = nbrs.kneighbors(user_preference)

    similar_house_ids = data.iloc[indices[0]]["HouseID"].tolist()

    return similar_house_ids


def get_average(average_df):
    df_calendar = average_df.groupby('date')[["price"]].sum()
    df_calendar['mean'] = average_df.groupby('date')[["price"]].mean()
    df_calendar.columns = ['Total', 'Avg']
    df_calendar_copy = df_calendar.copy()

    df_calendar_copy['date'] = df_calendar_copy.index
    df_calendar_copy = df_calendar_copy[['date', 'Avg']]
    df_calendar_copy.columns = ['ds', 'y']
    df_calendar_copy['y'] = np.log(df_calendar_copy['y'])

    # convert ds to datetime type
    df_calendar_copy['ds'] = pd.to_datetime(df_calendar_copy['ds'])
    df_calendar_copy = df_calendar_copy[(df_calendar_copy['ds'] > df_calendar_copy['ds'].min()) & (
        df_calendar_copy['ds'] < df_calendar_copy['ds'].max())]
    return df_calendar_copy


def get_curves(df_calendar, forecast_df, price_list, price):
    df_calendar['y'] = np.exp(df_calendar['y'])
    df_calendar['ds'] = pd.to_datetime(df_calendar['ds'])
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])

    df_calendar['days'] = (df_calendar['ds'] -
                           df_calendar['ds'].min()) / np.timedelta64(1, 'D')
    forecast_df['days'] = (
        forecast_df['ds'] - df_calendar['ds'].max()) / np.timedelta64(1, 'D')  # 更新这里

    adjusted_forecasts = []
    differences = []

    for house_prices in price_list:
        house_prices['date'] = pd.to_datetime(house_prices['date'])
        house_prices['days'] = (
            house_prices['date'] - df_calendar['ds'].min()) / np.timedelta64(1, 'D')

        distance, path = fastdtw(df_calendar[['days', 'y']].values, house_prices[[
                                 'days', 'price']].values, dist=euclidean)

        diffs = [house_prices.iloc[index_house].price -
                 df_calendar.iloc[index_avg].y for index_avg, index_house in path]
        median_difference = np.median(diffs)
        differences.append(median_difference)

        adjusted_forecast = forecast_df.copy()
        for col in ['yhat1', 'yhat1 10.0%', 'yhat1 90.0%']:
            adjusted_forecast[col] = adjusted_forecast[col] + median_difference
        adjusted_forecasts.append(adjusted_forecast)

    overall_median_difference = np.median(differences)

    overall_adjusted_forecast = forecast_df.copy()
    for col in ['yhat1', 'yhat1 10.0%', 'yhat1 90.0%']:
        overall_adjusted_forecast[col] = overall_adjusted_forecast[col] + \
            overall_median_difference
    scale_factor = price / overall_adjusted_forecast['yhat1'].iloc[0]

    for col in ['yhat1', 'yhat1 10.0%', 'yhat1 90.0%']:
        overall_adjusted_forecast[col] = (
            overall_adjusted_forecast[col] - overall_adjusted_forecast['yhat1'].iloc[0]) * scale_factor + price

    return adjusted_forecasts, overall_adjusted_forecast
