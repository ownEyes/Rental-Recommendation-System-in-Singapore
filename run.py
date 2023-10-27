# find . -name "__pycache__" -exec rm -r {} + 当前目录及其所有子目录中查找并删除所有的 __pycache__ 目录

import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_minify  import Minify
from sys import exit
# from app.authentication.models import User
# from app.home.models import Rating, RentalHouse, Poi

from app.config import config_dict
from app import create_app, db
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer
from app.services.Recommender import Recommender

load_dotenv()
# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
# GEOCODING_APIKEY=os.getenv('GEOCODING_APIKEY', None)
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'
base_dir = os.path.abspath(os.path.dirname(__file__))
geojson_file_path = os.path.join(base_dir, "neighbourhoods.geojson")


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


try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
with app.app_context():
    app.data_manager = DataManager()
    poi_df= app.data_manager.get_pois_df(poi_columns+["name","formatted_address",'lat', 'lng'])
    app.map_drawer = MapDrawer(poi_df,geojson_file_path,semantic_groups,colors)
    app.recommender = Recommender()
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )


if __name__ == "__main__":
    app.run()
    
    