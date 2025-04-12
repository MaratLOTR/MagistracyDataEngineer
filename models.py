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
