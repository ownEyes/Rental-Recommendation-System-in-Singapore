from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, IntegerField, DateField, SelectField, DecimalField, BooleanField,SubmitField,SelectMultipleField, ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput
import datetime
from app.home.utils import *

from dataclasses import dataclass

@dataclass
class Rental:
    id: str
    title: str
    facility_type: str
    accommodation_info: str
    room_info: str
    public_facilities: list
    cooking_facilities: list
    interior_facilities: list
    other_needs: list
    price: str
    distance_to_mrt: str
    mall_info: str
    lat:float
    lng:float
    location_info: str
    location_href: str
    img_src: str

    def get_location_info(self):
        loc=get_reverseGeocoding([self.lat,self.lng])
        self.location_info=str(loc)
        return 

@dataclass
class FormData:
    minprice: int
    maxprice: int
    location: list
    checkin: datetime.date
    checkout: datetime.date
    p_rating:float
    l_rating:float
    t_rating:float
    a_rating:float
    roomtype: str
    desired_month: int
    public_facilities: list
    cooking_facilities: list
    interior_facilities: list
    other_needs: list
    vector: list

    def get_normalized_weights(self):
        total = float(self.p_rating) + float(self.l_rating) + float(self.t_rating) + float(self.a_rating)
        if total == 0:
            return {
                'price': 0.25,
                'room_type': 0.25,
                'distance': 0.25,
                'amenities': 0.25
            }
        return {
            'price': float(self.p_rating) / total,
            'room_type': float(self.t_rating) / total,
            'distance': float(self.l_rating) / total,
            'amenities': float(self.a_rating) / total
        }
    
    def amenities_to_vector(self,amenities_list):
        reference_list = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
        self.vector = [0] * len(reference_list)
        for amenities in amenities_list:
            for amenity in amenities:
                if amenity == "microwave":
                    amenity = "Microwave"
                elif amenity == "pets":
                    amenity = "Pets"
                elif amenity == "backyard":
                    amenity = "Backyard"
                elif amenity == "oven":
                    amenity = "Oven"
                elif amenity == "stoven":
                    amenity = "stove"
                if amenity in reference_list:
                    self.vector[reference_list.index(amenity)] = 1
        return self.vector

    def convert_amenities_to_input(self):

        # 将所有表单中的多选字段合并到一个列表中
        all_selected_amenities = [self.public_facilities , self.cooking_facilities , self.interior_facilities , self.other_needs]
        return self.amenities_to_vector(all_selected_amenities)



# class MultiCheckboxField(SelectMultipleField):
#     widget = ListWidget(prefix_label=False)
#     option_widget = CheckboxInput()

class SurveyForm(FlaskForm):
    minprice = StringField("minprice")
    maxprice = StringField("maxprice")
    location = StringField("location")
    checkin = StringField("checkin")
    checkout = StringField("checkout")
    p_rating = StringField("p_rating")
    l_rating = StringField("l_rating")
    t_rating = StringField("t_rating")
    a_rating = StringField("a_rating")
    roomtype = StringField("roomtype")
    #t_rating = StringField("importance_t")
    #day_diff = StringField("dayDifference")
    public_facilities = SelectMultipleField( 'public_facilities',
        choices=[('BBQ', 'BBQ'), ('gym', 'Gym'),('pool', 'Pool'),('backyard', 'Backyard')]
    )
    cooking_facilities = SelectMultipleField( 'cooking_facilities',
        choices=[('kitchen', 'Kitchen'),('refrigerator', 'Refrigerator'), ('microwave', 'Microwave'),('oven', 'Oven'),('stoven', 'Stoven')]
    )
    interior_facilities = SelectMultipleField( 'interior_facilities',
        choices=[('aircon', 'Aircon'), ('dryer', 'Dryer'),('Wifi', 'Wifi'),('TV', 'TV'),('fan', 'Fan')]
    )
    other_needs = SelectMultipleField( 'other_needs',choices=[('pets', 'Pets')])
    # kitchen_facilities = SelectMultipleField(
    #     'kitchen_facilities',
    #     choices=[('microwave', 'Microwave'), ('pot', 'Pot')]
    # )
    submit = SubmitField('Submit')