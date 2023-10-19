from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path= './processed_data_merged_final_v2.csv'
file_path = os.path.join(current_directory, csv_file_path)
database_file_path = os.path.join(current_directory, 'database.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file_path
db = SQLAlchemy(app)

class RentalHouse(db.Model):
    HouseID = db.Column(db.Integer, primary_key=True, nullable=False)
    HouseName = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=False)
    neighbourhood_cleansed = db.Column(db.Text, nullable=False)
    neighbourhood_group_cleansed = db.Column(db.Text, nullable=False)
    picture_url = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.Text, nullable=False)
    accommodates= db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_months = db.Column(db.Integer, nullable=False)
    maximum_months = db.Column(db.Integer, nullable=False)
    distance_to_mrt = db.Column(db.Float, nullable=False)
    closest_mrt_name = db.Column(db.Text, nullable=False)
    closest_mrt_stop_id = db.Column(db.Text, nullable=False)
    closest_mall_distance = db.Column(db.Float, nullable=False)
    closest_mall_name = db.Column(db.Text, nullable=False)
    closest_mall_address = db.Column(db.Text, nullable=False)
    aircon = db.Column(db.Boolean, nullable=False)
    BBQ = db.Column(db.Boolean, nullable=False)
    gym = db.Column(db.Boolean, nullable=False)
    pool = db.Column(db.Boolean, nullable=False)
    dryer = db.Column(db.Boolean, nullable=False)
    Wifi = db.Column(db.Boolean, nullable=False)
    kitchen = db.Column(db.Boolean, nullable=False)
    Backyard = db.Column(db.Boolean, nullable=False)
    TV = db.Column(db.Boolean, nullable=False)
    refrigerator = db.Column(db.Boolean, nullable=False)
    Microwave = db.Column(db.Boolean, nullable=False)
    Oven = db.Column(db.Boolean, nullable=False)
    Pets = db.Column(db.Boolean, nullable=False)
    stove = db.Column(db.Boolean, nullable=False)
    fan = db.Column(db.Boolean, nullable=False)


if __name__ == '__main__':
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        raw= pd.read_csv(file_path)
        for index, row in raw.iterrows():
            rentalHouse=RentalHouse(
                HouseID=row['id'],
                HouseName=row['name'],
                details=row['details'],
                neighbourhood_cleansed=row['neighbourhood_cleansed'],
                neighbourhood_group_cleansed=row['neighbourhood_group_cleansed'],
                picture_url=row['picture_url'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                room_type=row['room_type'],
                accommodates=row['accommodates'],
                price=row['price'],
                minimum_months=row['minimum_months'],
                maximum_months=row['maximum_months'],
                distance_to_mrt=row['distance_to_mrt'],
                closest_mrt_name=row['closest_mrt_name'],
                closest_mrt_stop_id=row['closest_mrt_stop_id'],
                closest_mall_distance=row['closest_mall_distance'],
                closest_mall_name=row['closest_mall_name'],
                closest_mall_address=row['closest_mall_address'],
                aircon=row['conditioning'],
                BBQ=row['BBQ'],
                gym=row['gym'],
                pool=row['pool'],
                dryer=row['dryer'],
                Wifi=row['Wifi'],
                kitchen=row['kitchen'],
                Backyard=row['Backyard'],
                TV=row['TV'],
                refrigerator=row['refrigerator'],
                Microwave=row['Microwave'],
                Oven=row['Oven'],
                Pets=row['Pets'],
                stove=row['stove'],
                fan=row['fan']
            )
            db.session.add(rentalHouse)
            db.session.commit()