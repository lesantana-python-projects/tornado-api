# coding: utf-8


from sqlalchemy import Column, Integer, Numeric, Date, Sequence, ForeignKey

from weather.configs import config
from weather.models.model_base import ModelBase
from weather.models.weather import Weather


class WeatherData(ModelBase):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    date = Column(Date)
    hour = Column(Integer)
    precipitation = Column(Numeric)
    dry_bulb_temperature = Column(Numeric)
    wet_bulb_temperature = Column(Numeric)
    high_temperature = Column(Numeric)
    low_temperature = Column(Numeric)
    relative_humidity = Column(Numeric)
    relative_humidity_avg = Column(Numeric)
    pressure = Column(Numeric)
    sea_pressure = Column(Numeric)
    wind_direction = Column(Numeric)
    wind_speed_avg = Column(Numeric)
    cloud_cover = Column(Numeric)
    evaporation = Column(Numeric)

    weather_id = Column(Integer, ForeignKey(Weather.id))
    __table_args__ = ({'schema': config.SQL_SCHEMA})

    @property
    def get_table_name(self):
        return self.__tablename__

    @property
    def get_schema_name(self):
        return self.__table_args__.get('schema', '')
