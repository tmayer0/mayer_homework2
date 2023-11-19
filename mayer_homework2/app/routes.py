from flask import Flask, render_template, request
from .models import City, Country
import requests
from .forms import CityForm, CountryForm
from main import app
from .database import db

def fetch_country_data():
    url = "http://geodb-free-service.wirefreethought.com/v1/geo/countries"

    headers = {
        "X-RapidAPI-Key": "5c3717507bmsh1607a8e6c0d423bp134073jsn117047e8db8c",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def fetch_city_data():
    url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities"
    headers = {
        "X-RapidAPI-Key": "5c3717507bmsh1607a8e6c0d423bp134073jsn117047e8db8c",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    city_data = response.json()
    if 'data' not in city_data:
        print("No city data found")
        return {'data': []}
    return city_data


@app.route('/populate_db')
def populate_db():
    country_data = fetch_country_data()
    for country in country_data['data']:
        country_obj = Country(
            code=country['code'],
            name=country['name'],
            currencyCode=country['currencyCodes'][0] if country['currencyCodes'] else None,
        )
        db.session.add(country_obj)
    db.session.commit()

    city_data = fetch_city_data()
    if 'data' not in city_data:
        print("No city data found")
        return "Failed to populate database"
    for city in city_data['data']:
        city_obj = City(
            name=city['name'],
            region=city['region'],
            country=city['country'],
            latitude=city['latitude'],
            longitude=city['longitude'],
            population=city['population'],
        )
        db.session.add(city_obj)
    db.session.commit()
    return "Database populated successfully"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_countries', methods=['GET', 'POST'])
def search_countries():
    form = CountryForm()
    country = None
    if form.validate_on_submit():
        print("form data:", form.name.data)
        country = Country.query.filter_by(name=form.name.data).first()
        print("country:", country)
    return render_template('search_countries.html', form=form, country=country)

@app.route('/filter_cities', methods=['GET', 'POST'])
def filter_cities():
    form = CityForm()
    cities = []
    if form.validate_on_submit():
        cities = City.query
        if form.name.data:
            cities = cities.filter_by(name=form.name.data)
        if form.region.data:
            cities = cities.filter_by(region=form.region.data)
        if form.country.data:
            cities = cities.filter_by(country=form.country.data)
        cities = cities.all()
    return render_template('filter_cities.html', form=form, cities=cities)

@app.route('/show_cities')
def show_cities():
    cities = City.query.all()
    for city in cities:
        print(city.name)
    return "Cities printed to console"