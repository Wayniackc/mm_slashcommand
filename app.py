import requests
import json

from flask import Flask, Response, request, abort

import keys

app = Flask(__name__)


@app.route('/askwayne', methods = ['POST'])
def slash_command():
    # Make sure request comes from Mattermost
    if keys.mm_token != request.form.getlist('token')[0]:
        abort(403)

    text = request.form.getlist('text')
    arguments = text[0].split(' ')
    if arguments[0].lower() == "weather":
        zip = arguments[1]
        if len(zip) != 5:
            mm_response = Response(response="Please enter a 5-digit US zip code",
                status=400,
                mimetype="application/json")
            return mm_response
        mm_response = get_weather(zip)
        return mm_response


def get_weather(zipcode):
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={keys.weather_api_key}"

    response = requests.get(url)

    temp = round(1.8 * (response.json()['main']['temp'] - 273) + 32, 1)
    desc = response.json()['weather'][0]['description']
    weather_icon = response.json()['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"

    dic = {
        "response_type": "ephemeral",
        "text": f"The sky is showing {desc} with a current temperature of {temp}F.",
        "username": "AskWayne",
        "icon_url": icon_url
    }

    json_body = json.dumps(dic)

    mm_response = Response(response=json_body,
                    status=200,
                    mimetype="application/json")
    return mm_response


app.run(host='0.0.0.0', port=5005)