from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectMultipleField, FieldList, \
    validators, SelectField
from wtforms.validators import DataRequired, Length, ValidationError,Regexp

class LoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    # remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    # name = StringField('Name', validators=[DataRequired(), Length(min=1, max=20)])
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.'),
        Length(min=1, max=20, message='Username must be between 1 and 20 characters long.')
    ])
    email = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Signup')

