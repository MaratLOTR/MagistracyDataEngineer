from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

from models import City, WeatherForecast, WeatherConditions

API_KEY = ''  # Замените на ваш ключ
DATABASE_URL = "postgresql://admin:admin@localhost:5432/weather_db"  # Это для примера, можно заменить на вашу базу данных
LAT = 57.1522  # Широта Тюмени
LON = 65.5272  # Долгота Тюмени
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&units=metric&lang=ru&appid={API_KEY}" # Нужно заполнить

def extract_data() -> dict:
    # Формируем URL запроса для One Call API 3.0 (только ежедневный прогноз)
    weather_url = WEATHER_URL
    weather_data = requests.get(weather_url).json()
    return weather_data


def transform_data(raw_data: dict) -> dict:
    transformed = {
        'city': {
            'id': raw_data['city']['id'],
            'name': raw_data['city']['name'],
            'country': raw_data['city']['country'],
            'lat': Decimal(raw_data['city']['coord']['lat']).quantize(Decimal('0.0001')),
            'lon': Decimal(raw_data['city']['coord']['lon']).quantize(Decimal('0.0001')),
            'population': raw_data['city'].get('population'),
            'timezone': raw_data['city'].get('timezone')
        },
        'forecasts': []
    }

    for item in raw_data['list']:
        # Основной прогноз
        forecast = {
            'dt': item['dt'],
            'city_id': raw_data['city']['id'],
            'temp': Decimal(str(item['main']['temp'])).quantize(Decimal('0.01')),
            'feels_like': Decimal(str(item['main']['feels_like'])).quantize(Decimal('0.01')),
            'pressure': item['main'].get('pressure'),
            'humidity': item['main'].get('humidity'),
            'wind_speed': Decimal(str(item['wind']['speed'])).quantize(Decimal('0.01')) if 'speed' in item[
                'wind'] else None
        }

        # Погодные условия
        weather = item['weather'][0]
        conditions = {
            'dt': item['dt'],
            'main_condition': weather['main'],
            'description': weather['description'],
            'clouds': item['clouds']['all'],
            'pop': Decimal(str(item.get('pop', 0))).quantize(Decimal('0.00')),
            'rain_3h': Decimal(str(item['rain']['3h'])).quantize(Decimal('0.00')) if 'rain' in item else None,
            'snow_3h': Decimal(str(item['snow']['3h'])).quantize(Decimal('0.00')) if 'snow' in item else None
        }

        forecast['conditions'] = conditions
        transformed['forecasts'].append(forecast)

    return transformed

def load(transformed_data: dict) -> None:
    # Предположим, что у вас уже настроен engine и session


    # Создание подключения к базе данных
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    city = session.get(City, transformed_data['city']['id'])
    if not city:
        city = City(**transformed_data['city'])
        session.add(city)
        session.flush()  # Получаем ID для связей

    # Подготавливаем данные для вставки

    forecasts = []
    conditions = []

    for forecast in transformed_data['forecasts']:
        # Разделяем данные прогноза и условий
        cond_data = forecast.pop('conditions')

        # Создаем объекты ORM
        forecasts.append(WeatherForecast(**forecast))
        conditions.append(WeatherConditions(**cond_data))

    # Пакетная вставка
    session.add_all(forecasts)
    session.add_all(conditions)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


if __name__ == '__main__':
    data = extract_data()
    data = transform_data(data)
    load(data)
