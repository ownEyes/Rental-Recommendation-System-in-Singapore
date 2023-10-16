from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SurveyForm(FlaskForm):
    minprice = StringField("minprice")
    maxprice = StringField("maxprice")
    imp_p = StringField("importance_p")
    imp_l = StringField("importance_l")
    imp_d = StringField("importance_d")
    location = StringField("location")
    startdate = StringField("checkin")
    enddate = StringField("checkout")
    submit = SubmitField('Submit')