from mock import mock

from tests.unit.weather import BaseTests
from weather.models import DBDriver
from weather.services import Singleton


class TestDbDriver(BaseTests):
    def setUp(self):
        Singleton.drop()

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    def test_get_db_session(self, mock_create_engine, mock_scoped_session):
        db_driver = DBDriver()
        db_driver.db_session
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_scoped_session.called)

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    def test_get_db_engine(self, mock_create_engine, mock_scoped_session):
        db_driver = DBDriver()
        db_driver.db_engine
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_scoped_session.called)

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    @mock.patch('weather.models.sessionmaker')
    def test_object_commit_success(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = DBDriver()
        db_driver.object_commit(object)
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.db_session.flush.called)
        self.assertTrue(db_driver.db_session.commit.called)

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    @mock.patch('weather.models.sessionmaker')
    def test_object_commit_exception(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = DBDriver()
        message_error = 'not flush'
        db_driver.db_session.flush.side_effect = Exception(message_error)
        with self.assertRaises(Exception) as context:
            db_driver.object_commit(object)
        self.assertEqual(context.exception.args[0], message_error)
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.db_session.flush.called)
        self.assertTrue(db_driver.db_session.expunge_all.called)
        self.assertTrue(db_driver.db_session.rollback.called)

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    @mock.patch('weather.models.sessionmaker')
    def test_remove_session(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = DBDriver()
        db_driver.remove_session()
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.db_session.remove.called)

    @mock.patch('weather.models.scoped_session')
    @mock.patch('weather.models.create_engine')
    @mock.patch('weather.models.sessionmaker')
    def test_delete_object(self, mock_sessionmaker, mock_scoped_session, mock_create_engine):
        db_driver = DBDriver()
        db_driver.delete_object(object)

        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)
        self.assertTrue(db_driver.db_session.delete.called)
