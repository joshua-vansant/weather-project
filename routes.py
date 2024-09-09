from flask import render_template, request, jsonify, redirect, url_for
from app import app
import os
import requests
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/')
@app.route('/weather/<city>')
def weather(city=None):
    if city is None:
        city = request.args.get('city')
        if city:
            return redirect(url_for('weather', city=city))
        else:
            return render_template('index.html')
    
    # Fetch weather data for the given city
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    
    if 'error' not in data:
        weather_data = {
            'city': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country'],
            'temperature': data['current']['temp_c'],
            'temperature_f': data['current']['temp_f'],
            'description': data['current']['condition']['text'],
            'icon': data['current']['condition']['icon'],
            'humidity': data['current']['humidity'],
            'wind_speed': data['current']['wind_kph'],
            'wind_direction': data['current']['wind_dir'],
            'pressure': data['current']['pressure_mb'],
            'feels_like': data['current']['feelslike_f'],
            'uv_index': data['current']['uv'],
            'visibility': data['current']['vis_km'],
            'last_updated': data['current']['last_updated']
        }
        return render_template('weather.html', weather=weather_data)
    else:
        return render_template('index.html', error='City not found')

@app.route('/forecast/')
@app.route('/forecast/<city>')
def forecast(city=None):
    if city is None:
        city = request.args.get('city')
        if city:
            return redirect(url_for('forecast', city=city))
        else:
            return render_template('index.html')

    # Fetch forecast data
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(url)
    data = response.json()
    for day in data['forecast']['forecastday']:
        day['date'] = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A, %B %d, %Y')
    if 'error' not in data:
        # print(data)
        weather_data = {
            'city': data['location']['name'],
            'region': data['location']['region'],
            'country': data['location']['country'],
            'forecast': data['forecast']['forecastday']
        }
        return render_template('forecast.html', weather=weather_data)
    else:
        return render_template('index.html', error='City not found')