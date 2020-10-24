from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

from weather.models import DBDriver

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def orm(self):
        return DBDriver()
