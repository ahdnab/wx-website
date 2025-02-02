from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '46b4681891584da3b66a4dae2d11748b'

def fetch_weather(api_key, location):
    url = f'http://api.weatherbit.io/v2.0/current?city={location}&key={api_key}&units=M'

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Debug information (optional)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            weather_data = response.json().get('data', [{}])[0]

            # Extracting weather details...
            description = weather_data.get('weather', {}).get('description', 'N/A')
            temperature = weather_data.get('temp', 'N/A')
            feels_like = weather_data.get('app_temp', 'N/A')
            humidity = weather_data.get('rh', 'N/A')
            visibility_km = weather_data.get('vis', 'N/A')
            visibility_m = visibility_km * 1000 if isinstance(visibility_km, (int, float)) else 'N/A'
            wind_speed_kmh = weather_data.get('wind_spd', 0)
            wind_speed_knots = wind_speed_kmh * 0.539957
            wind_dir = weather_data.get('wind_dir', 'N/A')
            wind_gust_kmh = weather_data.get('wind_gust', 0)
            wind_gust_knots = wind_gust_kmh * 0.539957
            pressure = weather_data.get('pres', 'N/A')
            clouds = weather_data.get('clouds', 'N/A')
            uv_index = weather_data.get('uv', 'N/A')
            precipitation_mm = weather_data.get('precip', 0)
            precipitation = "None" if precipitation_mm == 0 else f"{precipitation_mm} mm"

            # Additional details (optional)
            sunrise = weather_data.get('sunrise', 'N/A')
            sunset = weather_data.get('sunset', 'N/A')
            weather_icon = weather_data.get('weather', {}).get('icon', '')

            weather_info = {
                'description': description,
                'temperature': temperature,
                'feels_like': feels_like,
                'humidity': humidity,
                'visibility': visibility_m,
                'wind_speed_knots': round(wind_speed_knots, 2),
                'wind_dir': wind_dir,
                'wind_gust_knots': round(wind_gust_knots, 2),
                'pressure': pressure,
                'clouds': clouds,
                'uv_index': uv_index,
                'precipitation': precipitation,
                'sunrise': sunrise,
                'sunset': sunset,
                'weather_icon': weather_icon
            }

            return weather_info
        else:
            return None
    except requests.exceptions.RequestException as e:
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

    weather_info = fetch_weather(API_KEY, location)

    if weather_info:
        return render_template('weather.html', weather_info=weather_info, location=location)
    else:
        return "Error: Unable to fetch weather data. Please check your API key or the API endpoint.", 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
