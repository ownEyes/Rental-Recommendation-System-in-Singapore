from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField

class SurveyForm(FlaskForm):
    minprice = StringField("minprice")
    maxprice = StringField("maxprice")
    roomtype = StringField("roomtype")
    location = StringField("location")

    checkin = StringField("checkin")
    checkout = StringField("checkout")
    p_rating = StringField("p_rating")
    l_rating = StringField("l_rating")
    d_rating = StringField("d_rating")
    public_facilities = SelectMultipleField( 'public_facilities',
        choices=[('BBQ', 'BBQ'), ('gym', 'Gym'),('pool', 'Pool'),('backyard', 'Backyard')]
    )
    cooking_facilities = SelectMultipleField( 'cooking_facilities',
        choices=[('refrigerator', 'Refrigerator'), ('microwave', 'Microwave'),('oven', 'Oven'),('stoven', 'Stoven')]
    )
    interior_facilities = SelectMultipleField( 'interior_facilities',
        choices=[('aircon', 'Aircon'), ('dryer', 'Dryer'),('Wifi', 'Wifi'),('TV', 'TV'),('fan', 'Fan')]
    )
    other_needs = SelectMultipleField( 'other_needs',choices=[('pets', 'Pets')])
    # kitchen_facilities = SelectMultipleField(
    submit = SubmitField('Submit')