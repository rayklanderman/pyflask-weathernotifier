from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api_key = '16fe26b542aa77552cdc68a442e0c5e5'
geocode_base_url = "http://api.openweathermap.org/geo/1.0/direct?"
one_call_base_url = "https://api.openweathermap.org/data/3.0/onecall?"

# Root route
@app.route('/')
def home():
    return "Welcome to the Weather Notifier!"

# Weather route
@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    try:
        # Get coordinates from the city name
        geocode_url = f"{geocode_base_url}q={location}&appid={api_key}"
        response = requests.get(geocode_url)
        location_data = response.json()

        if not location_data:
            return jsonify({'error': 'City not found'}), 404

        lat = location_data[0]['lat']
        lon = location_data[0]['lon']

        # Get weather data using the One Call API
        weather_url = f"{one_call_base_url}lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(weather_url)
        weather_data = response.json()

        # Extracting relevant data
        temp = weather_data['current']['temp'] - 273.15  # Converting temperature from Kelvin to Celsius
        pres = weather_data['current']['pressure']
        hum = weather_data['current']['humidity']
        weather_desc = weather_data['current']['weather'][0]['description']

        return jsonify({
            'temperature': temp,
            'atmospheric_pressure': pres,
            'humidity': hum,
            'description': weather_desc
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
