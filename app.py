import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('WEATHER_API_KEY')

# Helper to map weather to icon filename
ICON_MAP = {
    'Rain': 'rain.png',
    'Clear': 'sun.png',
    'Clouds': 'cloudy.png',
    'Thunderstorm': 'storm.png',
    'Drizzle': 'light rain.png',
    'Snow': 'snow.png',
    'Mist': 'cloudy.png',
    'Fog': 'cloudy.png',
    'Haze': 'cloudy.png',
    'Smoke': 'cloudy.png',
    'Dust': 'cloudy.png',
    'Sand': 'cloudy.png',
    'Ash': 'cloudy.png',
    'Squall': 'cloudy.png',
    'Tornado': 'storm.png',
}

def get_icon(weather_main):
    return ICON_MAP.get(weather_main, 'cloudy.png')


# Landing page
@app.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')

# Weather dashboard
@app.route('/app', methods=['GET'], endpoint='index')
def index():
    city = request.args.get('city', 'London')
    weather, forecast, trend, error = get_weather_data(city)
    return render_template('index.html', city=city, weather=weather, forecast=forecast, trend=trend, error=error)

def get_weather_data(city):
    # OpenWeatherMap API endpoints
    url_weather = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    
    weather = {}
    forecast = []
    trend = {'labels': [], 'highs': [], 'lows': []}
    error = None
    try:
        r = requests.get(url_weather)
        data = r.json()
        if r.status_code != 200 or 'main' not in data or 'weather' not in data:
            error = data.get('message', 'Could not fetch weather data.')
            # Provide dummy values to avoid template errors
            weather = {'temp': '-', 'desc': '-', 'main': '-', 'icon': 'cloudy.png', 'humidity': '-', 'pressure': '-', 'wind': '-', 'uv': '-', 'date': '-'}
            forecast = []
            trend = {'labels': [], 'highs': [], 'lows': []}
            return weather, forecast, trend, error
        weather = {
            'temp': round(data['main']['temp'], 1),
            'desc': data['weather'][0]['description'].title(),
            'main': data['weather'][0]['main'],
            'icon': get_icon(data['weather'][0]['main']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind': data['wind']['speed'],
            'uv': 5,  # Placeholder, OpenWeatherMap OneCall API needed for real UV
            'date': datetime.utcfromtimestamp(data['dt']).strftime('%A, %B %d'),
        }
        r2 = requests.get(url_forecast)
        data2 = r2.json()
        if r2.status_code != 200 or 'list' not in data2:
            error = data2.get('message', 'Could not fetch forecast data.')
            forecast = []
            trend = {'labels': [], 'highs': [], 'lows': []}
            return weather, forecast, trend, error
        # 5-day forecast, one per day (at 12:00)
        days = {}
        for entry in data2['list']:
            dt = datetime.utcfromtimestamp(entry['dt'])
            if dt.hour == 12 and len(days) < 7:
                day = dt.strftime('%a, %b %d')
                days[day] = {
                    'date': day,
                    'temp': round(entry['main']['temp']),
                    'main': entry['weather'][0]['main'],
                    'desc': entry['weather'][0]['description'].title(),
                    'icon': get_icon(entry['weather'][0]['main'])
                }
        forecast = list(days.values())
        # For chart: get high/low for each day
        highs, lows, labels = [], [], []
        for day, entries in group_by_day(data2['list']).items():
            temps = [e['main']['temp'] for e in entries]
            highs.append(round(max(temps)))
            lows.append(round(min(temps)))
            labels.append(datetime.utcfromtimestamp(entries[0]['dt']).strftime('%b %d'))
        trend = {'labels': labels, 'highs': highs, 'lows': lows}
    except Exception as e:
        print('Weather API error:', e)
        error = str(e)
        weather = {'temp': '-', 'desc': '-', 'main': '-', 'icon': 'cloudy.png', 'humidity': '-', 'pressure': '-', 'wind': '-', 'uv': '-', 'date': '-'}
        forecast = []
        trend = {'labels': [], 'highs': [], 'lows': []}
    return weather, forecast, trend, error

def group_by_day(entries):
    days = {}
    for entry in entries:
        dt = datetime.utcfromtimestamp(entry['dt'])
        day = dt.date()
        if day not in days:
            days[day] = []
        days[day].append(entry)
    return days

if __name__ == '__main__':
    app.run(debug=True)
