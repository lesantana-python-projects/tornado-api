from pandas import read_csv, notnull

from weather.models.weather import Weather
from weather.models.weather_data import WeatherData


def load_weather():
    weather = Weather()
    df = read_csv('../files/grid_weather.csv', sep=',', index_col='id',
                  usecols=['id', 'latitude', 'longitude', 'name_station'])
    df.to_sql(
        name=weather.get_table_name, con=weather.orm.db_engine, if_exists='append', schema=weather.get_schema_name)
    weather.orm.remove_session()


def load_weather_data():
    weather_data = WeatherData()
    df = read_csv('../files/grid_weather_data.csv', sep=',', index_col=None,
                  usecols=['id', 'date', 'hour', 'precipitation', 'dry_bulb_temperature', 'wet_bulb_temperature',
                           'high_temperature', 'low_temperature', 'relative_humidity', 'relative_humidity_avg',
                           'pressure', 'sea_pressure', 'wind_direction', 'wind_speed_avg', 'cloud_cover',
                           'evaporation'])
    df.rename(columns={'id': 'weather_id'}, inplace=True)
    df = df.astype(object).where(notnull(df), None)
    # df['id'] = df.apply(lambda x: df.index + 1, axis=1)

    df.to_sql(
        name=weather_data.get_table_name, con=weather_data.orm.db_engine,
        if_exists='append', index=False, schema=weather_data.get_schema_name)
    weather_data.orm.remove_session()


if __name__ == '__main__':
    # load_weather()
    load_weather_data()
