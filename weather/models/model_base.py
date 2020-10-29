from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from weather.models import DBDriver
from sqlalchemy.exc import (IntegrityError)

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    KNOWN_ERROR_SQLALCHEMY = {'friendly_message': 'Database error contact system admin, this action was logged.',
                              'known_errors': (IntegrityError,)}

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def orm(self):
        return DBDriver()
