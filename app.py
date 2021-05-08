import requests
import json

from flask import Flask
from flask import request

import keys

app = Flask(__name__)

def GetWeather(zipcode):
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={keys.weather_api_key}"
    print(url)

    response = requests.get(url)
    print(response.json())

    temp = round(1.8 * (response.json()['main']['temp'] - 273) + 32, 1)
    print(temp)


@app.route('/askwayne', methods = ['POST'])
def slash_command():
    text = request.form.getlist('text')
    print(text)
    arguments = text[0].split(' ')
    print(arguments[0])
    print(arguments[1])
    if arguments[0].lower() == "weather":
        zip = arguments[1]
        GetWeather(zip)
    return 'text'



app.run(host='0.0.0.0', port=5005)

# api key 1a4f49e7b89b318dd4588b95707876ef
