from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def fetch_weather(api_key, location):
    url = f'http://api.weatherbit.io/v2.0/current?city={location}&key={api_key}&units=M'
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        data = weather_data['data'][0]
        description = data['weather']['description']
        temperature = data['temp']
        humidity = data['rh']
        visibility = data.get('vis', 'N/A')
        wind_speed_kmh = data['wind_spd']
        wind_speed_knots = wind_speed_kmh * 0.539957
        wind_dir = data['wind_dir']
        pressure = data['pres']
        uv_index = data.get('uv', 'N/A')
        clouds = data['clouds']
        feels_like = data.get('app_temp', 'N/A')

        weather_info = {
            'description': description,
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': humidity,
            'visibility': visibility,
            'wind_speed_knots': round(wind_speed_knots, 2),
            'wind_dir': wind_dir,
            'pressure': pressure,
            'clouds': clouds,
            'uv_index': uv_index
        }

        return weather_info
    else:
        return "Error: Unable to fetch weather data."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    api_key = '46b4681891584da3b66a4dae2d11748b'
    weather_info = fetch_weather(api_key, location)
    return render_template('weather.html', weather_info=weather_info, location=location)


if __name__ == '__main__':
    app.run(debug=True)
