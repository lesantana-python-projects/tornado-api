from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from weather.configs import config
from weather.services import Singleton


class DBDriver(metaclass=Singleton):
    """Class the of access database connect."""

    def __init__(self):
        self.__engine = create_engine(
            'postgresql://{user}:{pwd}@{host}/{db}'.format(
                user=config.SQL_USER, pwd=config.SQL_PWD, host=config.SQL_HOST, db=config.SQL_DB),
            convert_unicode=True,
            pool_size=config.SQL_POOL_SIZE,
            pool_pre_ping=True, echo=False)

        self.__db_session = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=True))

    @property
    def db_session(self):
        """Property db_session."""
        return self.__db_session

    @property
    def db_engine(self):
        """Property engine."""
        return self.__engine

    def __commit(self):
        """Commit in Database"""
        try:
            self.db_session.flush()
            self.db_session.commit()
        except Exception as error:
            self.db_session.rollback()
            self.db_session.expunge_all()
            raise error

    def object_commit(self, p_object):
        """Add object of the database."""
        self.db_session.add(p_object)
        self.__commit()

    def delete_object(self, p_object):
        """Delete object of the database."""
        self.db_session.delete(p_object)
        self.__commit()

    def remove_session(self):
        """remove session sql"""
        self.__db_session.remove()
