from flask import Flask, render_template, request
import requests
import webbrowser
from threading import Timer

app = Flask(__name__)
API_KEY = '658f4f4e09a67436ce875564034a17e3'  # Replace with your actual OpenWeatherMap API key

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    forecast = []
    if request.method == 'POST':
        city = request.form.get('city')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        forecast_response = requests.get(forecast_url)

        if response.status_code == 200 and forecast_response.status_code == 200:
            data = response.json()
            forecast_data = forecast_response.json()

            weather = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed']
            }

            # Only next 7 entries (approx. next 21 hours in 3-hour intervals)
            forecast = [
                {
                    'time': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'icon': item['weather'][0]['icon'],
                    'desc': item['weather'][0]['description'].title()
                }
                for item in forecast_data['list'][:7]
            ]
        else:
            weather = {'error': 'City not found!'}

    return render_template('index.html', weather=weather, forecast=forecast)

if __name__ == '__main__':
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)

