from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, IntegerField, DateField, SelectField, DecimalField, BooleanField,SubmitField,SelectMultipleField, ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput
import datetime

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