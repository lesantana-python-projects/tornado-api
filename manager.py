import sys

from weather.models.model_base import ModelBase

orm = ModelBase()


def migrate_database():
    """Migrate Database."""
    import weather.models.weather
    import weather.models.weather_data
    ModelBase.metadata.create_all(bind=orm.orm.db_engine, checkfirst=True)


if __name__ == '__main__':
    args = sys.argv[1:]

    if 'migrate' in list(args):
        migrate_database()
