from sqlalchemy import Column, Integer, String, DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    # Определение полей таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String(2), nullable=False)
    lat = Column(DECIMAL(8, 4), nullable=False)
    lon = Column(DECIMAL(8, 4), nullable=False)
    population = Column(Integer, nullable=True)
    timezone = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name}, country={self.country}, lat={self.lat}, lon={self.lon}, population={self.population}, timezone={self.timezone})>"


class WeatherForecast(Base):
    __tablename__ = 'weather_forecast'

    # Определение полей таблицы
    dt = Column(BigInteger, primary_key=True)  # Временная метка (UNIX timestamp)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)  # Ссылка на город (City.id)
    temp = Column(DECIMAL(5, 2), nullable=False)  # Температура (°C)
    feels_like = Column(DECIMAL(5, 2), nullable=False)  # Ощущаемая температура (°C)
    pressure = Column(Integer, nullable=True)  # Атмосферное давление (hPa)
    humidity = Column(Integer, nullable=True)  # Влажность (%)
    wind_speed = Column(DECIMAL(5, 2), nullable=True)  # Скорость ветра (м/с)

    # Определяем связь с таблицей City (многие к одному)
    city = relationship('City', backref='weather_forecasts')

    def __repr__(self):
        return (f"<WeatherForecast(dt={self.dt}, city_id={self.city_id}, temp={self.temp}, "
                f"feels_like={self.feels_like}, pressure={self.pressure}, humidity={self.humidity}, "
                f"wind_speed={self.wind_speed})>")


class WeatherConditions(Base):
    __tablename__ = 'weather_conditions'

    # Определение полей таблицы
    dt = Column(BigInteger, ForeignKey('weather_forecast.dt'), primary_key=True)  # Ссылка на прогноз (WeatherForecast.dt)
    main_condition = Column(String(255), nullable=False)  # Основное состояние (например, "Rain")
    description = Column(String(250), nullable=True)  # Детальное описание (например, "небольшой дождь")
    clouds = Column(Integer, nullable=True)  # Облачность (%)
    pop = Column(DECIMAL(3, 2), nullable=True)  # Вероятность осадков (0..1)
    rain_3h = Column(DECIMAL(5, 2), nullable=True)  # Объем дождя за 3 часа (мм)
    snow_3h = Column(DECIMAL(5, 2), nullable=True)  # Объем снега за 3 часа (мм)

    # Определяем связь с таблицей WeatherForecast (один к одному)
    weather_forecast = relationship('WeatherForecast', backref='weather_condition', uselist=False)
