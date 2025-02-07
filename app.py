from flask import Flask, render_template, request
import json
import subprocess

app = Flask(__name__)


def fetch_weather(location):
    """Call fetch_data.py to update data.json with weather data for the given location"""
    try:
        # Run fetch_data.py with the location as an argument
        subprocess.run(['python', 'fetch_data.py', location], check=True)

        # Read the updated data.json
        with open('data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    if not location:
        return "Error: Location not provided.", 400

    weather_info = fetch_weather(location)

    if weather_info:
        return render_template('weather.html',
                               weather_info=weather_info,
                               location=location)
    else:
        return "Error: Unable to fetch weather data. Please check your API key or the API endpoint.", 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)