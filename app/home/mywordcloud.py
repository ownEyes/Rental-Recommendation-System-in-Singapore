from wordcloud import WordCloud
import matplotlib.pyplot as plt
#feature_imp = {'Location': 0.21485669732300028, 'Minimum period': -0.4832147346542469, 'Maximum period': -0.015584135649260792, 'Mrt': -0.04119973117622499, 'Mall': 0.09622524217094093, 'Accommodates': 0.682097138166826, 'Conditioning': 0.005418593790544541, 'Bbq': 0.2210620519352466, 'Gym': 0.23843037100665487, 'Pool': 0.08131756917715567, 'Dryer': 0.017161377330244972, 'Wifi': -0.003320314039870306, 'Kitchen': -0.07301817283408996, 'Backyard': -0.01616454379298572, 'Tv': -0.4368900869035097, 'Refrigerator': -0.048522494107858576, 'Microwave': 0.003776434599936475, 'Oven': 0.059762998437909096, 'Pets': 0.1525213763275123, 'Stove': -0.04658261183978682, 'Fan': -0.077655391174246, 'Bedrooms': -0.07459597108874912, 'Beds': -0.14051546364915976, 'Baths': 0.07425329783287091, 'Entire home/apt': -0.6614814344380671, 'Hotel room': -0.00017763418748305772, 'Private room': -0.39112872527569287, 'Shared room': 0.01837978247254603, 'shared bath': 0.19828407706195764}

def process_feature_imp(feature_imp):
    new_data = {}
    data_bath = ['bath_type_Private', 'bath_type_Shared']
    max_value = 0
    max_key = ''
    for key in data_bath:
        if key in feature_imp and feature_imp[key] > max_value:
            max_value = feature_imp[key]
            max_key = key

    new_bath_key = max_key.replace('bath_type_', '') + ' bath'

    # 处理 'latitude' 和 'longitude' 键
    if 'latitude' in feature_imp and 'longitude' in feature_imp:
        if feature_imp['latitude'] > feature_imp['longitude']:
            new_key = 'location'
            new_data[new_key] = feature_imp['latitude']
        else:
            new_key = 'location'
            new_data[new_key] = feature_imp['longitude']

    for key, value in feature_imp.items():
        if key not in data_bath and key != 'latitude' and key != 'longitude':
            if key.startswith('total_'):
                key = key.replace('total_', '')
            elif key.startswith('room_type_'):
                key = key.replace('room_type_', '')
            elif key == 'distance_to_mrt':
                key = 'MRT'
            elif key == 'closest_mall_distance':
                key = 'Mall'
            elif key == 'minimum_months':
                key = 'Minimum period'
            elif key == 'maximum_months':
                key = 'Maximum period'
            new_data[key] = value

    keys_to_remove = ['neighbourhood_group_cleansed_West Region', 'neighbourhood_group_cleansed_North-East Region',
                      'neighbourhood_group_cleansed_North Region', 'neighbourhood_group_cleansed_East Region',
                      'neighbourhood_group_cleansed_Central Region']

    for key in keys_to_remove:
        if key in new_data:
            deleted_value = new_data.pop(key)

    new_data = {k.capitalize(): v for k, v in new_data.items()}
    new_data[new_bath_key] = max_value

    return new_data
#new = process_feature_imp(feature_imp)



# 生成词云图，自定义字体大小
def generate_wordcloud(feature_importance,path):
    filtered_feature_importance = {key: value for key, value in feature_importance.items() if value > 0}
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=None)
    wordcloud.generate_from_frequencies({k: v for k, v in filtered_feature_importance.items()})
    wordcloud.to_file(path)
