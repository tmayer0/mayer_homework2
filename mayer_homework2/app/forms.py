from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CountryForm(FlaskForm):
    name = StringField('Country Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class CityForm(FlaskForm):
    name = StringField('City Name')
    region = StringField('Region')
    country = StringField('Country')
    submit = SubmitField('Filter')