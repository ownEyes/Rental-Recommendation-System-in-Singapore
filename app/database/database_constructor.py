from flask import Flask
# from flask_bcrypt import Bcrypt

import pandas as pd
import os
from models import db,Rating,RentalHouse,User,Poi

current_directory = os.path.dirname(os.path.abspath(__file__))
house_file_path= './final_data.csv'
user_file_path='./userInfo_hashed.csv'
poi_file_path='./poiInfo.csv'
rating_file_path='./ratingInfo.csv'
house_path = os.path.join(current_directory, house_file_path)
user_path=os.path.join(current_directory, user_file_path)
poi_path = os.path.join(current_directory, poi_file_path)
rating_path=os.path.join(current_directory, rating_file_path)
database_file_path = os.path.join(current_directory, 'database.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file_path
# bcrypt = Bcrypt(app)




if __name__ == '__main__':
    column_mapping_house = {
    'id': 'HouseID',
    'name': 'HouseName',
    'conditioning': 'aircon',
    # ...
    }
    # column_mapping_user = {
    # 'original_column_name_1': 'new_column_name_1',
    # 'original_column_name_2': 'new_column_name_2',
    # # ...
    # }
    # column_mapping_rating = {
    # 'original_column_name_1': 'new_column_name_1',
    # 'original_column_name_2': 'new_column_name_2',
    # # ...
    # }
    # column_mapping_poi = {
    # 'original_column_name_1': 'new_column_name_1',
    # 'original_column_name_2': 'new_column_name_2',
    # # ...
    # }

    with app.app_context():
        # db = current_app.extensions['sqlalchemy'].db
        db.init_app(app)
        db.drop_all()
        db.create_all()
        house= pd.read_csv(house_path)
        user= pd.read_csv(user_path)
        rating= pd.read_csv(rating_path)
        poi= pd.read_csv(poi_path)

        house = house.rename(columns=column_mapping_house)
        # user['password'] = user['password'].apply(lambda x: bcrypt.generate_password_hash(x).decode('utf-8'))
        # user.to_csv('./userInfo_hashed.csv', index=False)

        house.to_sql('RentalHouse', con=db.engine, if_exists='replace')
        user.to_sql('user', con=db.engine, if_exists='replace')
        rating.to_sql('rating', con=db.engine, if_exists='replace')
        poi.to_sql('poi', con=db.engine, if_exists='replace',index_label='POIid')
        print("-----------start query test:house-----------")
        house = RentalHouse.query.filter_by(HouseID=71609).first()
        print(house.HouseName) 
        print("-----------start query test:user-------------")
        user = User.query.filter_by(userID=1).first()
        print(user.userName) 
        print("-----------start query test:rating-----------")
        rating = Rating.query.filter_by(userID=1).first()
        print(rating.rating) 
        print("-----------start query test:poi-------------")
        poi = Poi.query.filter_by(POIid=1).first()
        print(poi.name) 