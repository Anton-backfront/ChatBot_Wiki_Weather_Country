import requests
from datetime import datetime
from configs import TOKEN_weather

parameters = {
    'appid': TOKEN_weather,
    'units': 'metric',
    'lang': 'ru'
}

def get_weather_any_city(city):


    if city.lower() == '/stop':
        return ("Вы вышли из раздела Weather")
    else:
        parameters['q'] = city
        try:

            data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()
            city_name = data['name']
            temp = data['main']['temp']
            wind = data['wind']['speed']
            timezone = data['timezone']
            humidity = data['main']['humidity']
            sunrise = datetime.utcfromtimestamp(int(data['sys']['sunrise']) + int(timezone)).strftime('%H-%M')
            sunset = datetime.utcfromtimestamp(int(data['sys']['sunset']) + int(timezone)).strftime('%H-%M')
            description = data['weather'][0]['description']
            condition = data['weather'][0]['main']
            return (f'''В городе {city_name} сейчас {description}
Температура: {round(temp)} °C
Скорость ветра: {wind} м/с
Рассвет: {sunrise}
Закат: {sunset}
Влажность: {humidity} %
Состояние: {condition}''', temp, condition)

        except:
            return ('Вы ввели не корректный город, попробуйте снова', None, None)
