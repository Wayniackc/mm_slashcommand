import requests
import json

from flask import Flask, Response, request

import keys

app = Flask(__name__)

def get_weather(zipcode):
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={keys.weather_api_key}"
    #print(url)

    response = requests.get(url)
    #print(response.json())

    temp = round(1.8 * (response.json()['main']['temp'] - 273) + 32, 1)
    #print(temp)
    desc = response.json()['weather'][0]['description']
    #print(desc)
    weather_icon = response.json()['weather'][0]['icon']
    #print(weather_icon)
    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"
    #print(icon_url)

    dic = {
        "response_type": "ephemeral",
        "text": f"The sky is showing {desc} with a current temperature of {temp}F.",
        "username": "AskWayne",
        "icon_url": icon_url
    }
    #print(dic)

    json_body = json.dumps(dic)
    #print(json_body)

    #print(len(json_body))
    
    # mm_response = build_response(json_body)
    # print(mm_response)
    # return mm_response

    mm_response = Response(response=json_body,
                    status=200,
                    mimetype="application/json")
    return mm_response


def build_response(json_body):
    length = len(json_body)

    response = f"""
    HTTP/1.1 200 OK
    Content-Type: application/json
    Content-Length: {length}

    {json_body}
    """
    #print(response)
    return response


@app.route('/askwayne', methods = ['POST'])
def slash_command():
    # response = flask.Response()
    # response.headers["Content-Type"] = "application/json"
    text = request.form.getlist('text')
    print(text)
    arguments = text[0].split(' ')
    print(arguments[0])
    print(arguments[1])
    if arguments[0].lower() == "weather":
        zip = arguments[1]
        mm_response = get_weather(zip)
        return mm_response
        #return GetWeather(zip)
    #return 'text'
    #return response


app.run(host='0.0.0.0', port=5005)