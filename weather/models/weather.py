# coding: utf-8
from sqlalchemy import Column, Integer, Numeric, String, Sequence

from weather.models.model_base import ModelBase


class Weather(ModelBase):
    __tablename__ = 'weather'
    __table_args__ = {'schema': 'gaivota'}

    id = Column(Integer, Sequence('sequence_weather'), primary_key=True)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    name_station = Column(String(255), nullable=False)

    @property
    def get_table_name(self):
        return self.__tablename__

    @property
    def get_schema_name(self):
        return self.__table_args__.get('schema', '')
