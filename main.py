from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

from models import City, WeatherForecast, WeatherConditions

API_KEY = ''  # Замените на ваш ключ
DATABASE_URL = "postgresql://admin:admin@localhost:5432/weather_db"  # Это для примера, можно заменить на вашу базу данных
LAT = 57.1522  # Широта Тюмени
LON = 65.5272  # Долгота Тюмени
WEATHER_URL = "" # Нужно заполнить

def extract_data() -> dict:
    """
    Извлекает сырые данные прогноза погоды из OpenWeatherMap API.

    Returns:
        dict: Словарь с сырыми данными прогноза погоды.

    Пример возвращаемых данных:
        {
            'cod': '200',
            'list': [
                {
                    'dt': 1744502400,
                    'main': {'temp': 2.39, 'feels_like': -1.52, ...},
                    'weather': [{'main': 'Clouds', 'description': 'небольшая облачность', ...}],
                    ...
                },
                ...
            ],
            'city': {
                'id': 1488754,
                'name': 'Тюмень',
                'coord': {'lat': 57.1522, 'lon': 65.5272},
                ...
            }
        }
    """
    pass


def transform_data(raw_data: dict) -> dict:
    """
       Трансформирует сырые данные погоды в структурированный формат для сохранения в БД.

       Args:
           raw_data (dict): Сырые данные из API OpenWeatherMap

       Returns:
           dict: Трансформированные данные с разделением на город и прогнозы

       Пример возвращаемых данных:
           {
               'city': {
                   'id': 1488754,
                   'name': 'Тюмень',
                   'lat': Decimal('57.1522'),
                   'lon': Decimal('65.5272'),
                   ...
               },
               'forecasts': [
                   {
                       'dt': 1744502400,
                       'temp': Decimal('2.39'),
                       'feels_like': Decimal('-1.52'),
                       'conditions': {
                           'main_condition': 'Clouds',
                           'description': 'небольшая облачность',
                           'rain_3h': None,
                           ...
                       }
                   },
                   ...
               ]
           }
       """
    pass

def load(transformed_data: dict) -> None:
    """
       Сохраняет трансформированные данные в базу данных используя SQLAlchemy модели.

       Args:
           transformed_data (dict): Трансформированные данные, содержащие информацию
                                  о городе и прогнозах погоды

       Returns:
           None

       Пример действия:
           Создает или обновляет записи в таблицах:
           - City (Города)
           - WeatherForecast (Прогнозы погоды)
           - WeatherConditions (Погодные условия)

           Например, сохраняет город Тюмень с координатами (57.1522, 65.5272)
           и 40 прогнозов погоды для него.
       """
    # Предположим, что у вас уже настроен engine и session


    # Создание подключения к базе данных
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()


if __name__ == '__main__':
    data = extract_data()
    print("extracted data", data)
    data = transform_data(data)
    print("transformed data", data)
    load(data)
