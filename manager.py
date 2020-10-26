import sys
import sqlalchemy

from pandas import read_csv, notnull
from weather.configs import config
from weather.models.model_base import ModelBase

orm = ModelBase()


def load_weather():
    from weather.models.weather_data import Weather
    print('---- Initial Load Weather ----')
    weather = Weather()
    df = read_csv('files/grid_weather.csv', sep=',', index_col='id',
                  usecols=['id', 'latitude', 'longitude', 'name_station'])
    df.to_sql(
        name=weather.get_table_name, con=weather.orm.db_engine, if_exists='append',
        schema=weather.get_schema_name, method='multi')
    weather.orm.remove_session()
    print('---- Finish Load Weather ----')


def load_weather_data():
    from weather.models.weather_data import WeatherData
    print('---- Initial Load WeatherData ----')
    weather_data = WeatherData()
    df = read_csv('files/grid_weather_data.csv', sep=',', index_col=None,
                  usecols=['id', 'date', 'hour', 'precipitation', 'dry_bulb_temperature', 'wet_bulb_temperature',
                           'high_temperature', 'low_temperature', 'relative_humidity', 'relative_humidity_avg',
                           'pressure', 'sea_pressure', 'wind_direction', 'wind_speed_avg', 'cloud_cover',
                           'evaporation'])
    df.rename(columns={'id': 'weather_id'}, inplace=True)
    df = df.astype(object).where(notnull(df), None)

    df.to_sql(
        name=weather_data.get_table_name, con=weather_data.orm.db_engine,
        if_exists='append', index=False, schema=weather_data.get_schema_name, method='multi')
    weather_data.orm.remove_session()
    print('---- Finish Load WeatherData ----')


def migrate_database():
    """Migrate Database."""
    import weather.models.weather
    import weather.models.weather_data
    conn = ModelBase().orm.db_engine.connect()

    if not conn.dialect.has_schema(conn, config.SQL_SCHEMA):
        ModelBase().orm.db_engine.execute(sqlalchemy.schema.CreateSchema(config.SQL_SCHEMA))
    ModelBase.metadata.create_all(bind=orm.orm.db_engine, checkfirst=True)


if __name__ == '__main__':
    args = sys.argv[1:]

    if 'migrate' in list(args):
        migrate_database()

    if 'content' in list(args):
        load_weather()
        load_weather_data()
