from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, DecimalField, BooleanField,SubmitField,SelectMultipleField, ValidationError
from wtforms.validators import InputRequired

class SurveyForm(FlaskForm):
    minprice = DecimalField('Min. Price', validators=[InputRequired()])
    maxprice = DecimalField('Max. Price', validators=[InputRequired()])
    importance_p = StringField('Importance for Price')  # 使用星星评分插件，改为StringField
    location = StringField('Location', validators=[InputRequired()])
    importance_l = StringField('Importance for Location')
    roomtype = SelectField('Roomtype', choices=[('EntireHome/apt', 'Entire home/apt'),
                                                ('HotelRoom', 'Hotel room'),
                                                ('PrivateRoom', 'Private room'),
                                                ('SharedRoom', 'Shared room')],
                           validators=[InputRequired()])
    importance_t = StringField('Importance for Roomtype')
    checkin = DateField('Checkin Date', format='%Y-%m-%d', validators=[InputRequired()])
    checkout = DateField('Checkout Date', format='%Y-%m-%d', validators=[InputRequired()])
    importance_d=StringField('Importance for Date')
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
    submit = SubmitField('Submit')

    def validate_checkout(self, field):
        if self.checkin.data and field.data:
            day_difference = (field.data - self.checkin.data).days
            if day_difference <= 92:
                raise ValidationError('Checkout date must be at least 93 days after checkin date.')