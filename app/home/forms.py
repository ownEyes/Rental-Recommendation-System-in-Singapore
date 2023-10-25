from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, DecimalField, BooleanField,SubmitField,SelectMultipleField, ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput
import datetime

from dataclasses import dataclass

@dataclass
class FormData:
    minprice: int
    maxprice: int
    importance_p: float
    location: list
    importance_l: float
    roomtype: str
    importance_t: float
    checkin: datetime.date
    checkout: datetime.date
    importance_d: str
    desired_month: int
    public_facilities: list
    cooking_facilities: list
    interior_facilities: list
    other_needs: list


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

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
    importance_d = StringField('Importance for Date')
    public_facilities = MultiCheckboxField('Public Facilities', choices=[('BBQ', 'BBQ'), ('gym', 'Gym'), ('pool', 'Pool'), ('backyard', 'Backyard')])
    cooking_facilities = MultiCheckboxField('Cooking Facilities', choices=[('refrigerator', 'Refrigerator'), ('microwave', 'Microwave'), ('oven', 'Oven'), ('stoven', 'Stoven')])
    interior_facilities = MultiCheckboxField('Interior Facilities', choices=[('aircon', 'Aircon'), ('dryer', 'Dryer'), ('Wifi', 'Wifi'), ('TV', 'TV'), ('fan', 'Fan')])
    other_needs = MultiCheckboxField('Other Needs', choices=[('pets', 'Pets')])
    submit = SubmitField('Submit')

    def validate_checkout(self, field):
        if self.checkin.data and field.data:
            day_difference = (field.data - self.checkin.data).days
            if day_difference <= 92:
                raise ValidationError('Checkout date must be at least 93 days after checkin date.')