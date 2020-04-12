import requests
import json
from flask import Flask, request, Response
from flask_sslify import SSLify

token = 'lalala'

app = Flask(__name__)
sslify = SSLify(app)

def write_json(data, filename = 'response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_message(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    return chat_id, text


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    d = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=d)
    return r


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, text = get_message(msg)

        if text == '/start' or text == '/help':
            send_message(chat_id, 'Введите нужный город')
            return Response('Ok', status=200)
        else:
            weather = get_weather_data(text)
            send_message(chat_id, weather)
            return Response('Ok', status=200)
    else:
        return '<h2> ЗАРАБОТАЛО <h2>'


def get_weather_data(city):
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city,
             'appid': '11c0d3dc6093f7442898ee49d2430d20',
             'units': 'metric', 'lang': 'ru'}

    data = requests.get(url, params).json()
    cod = (data['cod'])

    if cod == 200:
        temp = round(data['main']['temp'])
        descr = str(data['weather'][0]['description'])
        wind = round(data['wind']['speed'])
        answer = str(temp) + '°C, ' + descr + ', ветер ' + str(wind) + 'м/с'
        return(answer)
    else:
        return('Такой город точно есть?')



def main():
    print('bla-bla')
   # URL = 'https://api.telegram.org/bot1168156058:AAF_gW9RbsKEV4dyUvzIwqqEZaBsqXuHwHc/setWebhook?url=https://nastyaobrezkova.pythonanywhere.com/'


if __name__ == '__main__':
    app.run(debug=True)