import tornado.web

from weather.views.api.v1.api_weather import ApiWeatherDetail, ApiWeatherEdit, ApiWeatherAdd
from weather.views.api.v1.api_weather_data import ApiWeatherDataDetail, ApiWeatherDataEdit, ApiWeatherDataAdd
from weather.views.healthcheck import HealthcheckApi

routes = [
    tornado.web.url(r'/api/healthcheck', HealthcheckApi),
    tornado.web.url(r'/api/{version}/weather/list'.format(version=ApiWeatherDetail.version), ApiWeatherDetail),
    tornado.web.url(r'/api/{version}/weather'.format(version=ApiWeatherAdd.version), ApiWeatherAdd),
    tornado.web.url(r'/api/{version}/weather/(?P<weather_id>[a-zA-Z0-9]+)'.format(
        version=ApiWeatherEdit.version), ApiWeatherEdit),
    tornado.web.url(r'/api/{version}/weather-data/list'.format(version=ApiWeatherDataDetail.version),
                    ApiWeatherDataDetail),
    tornado.web.url(r'/api/{version}/weather-data'.format(version=ApiWeatherDataAdd.version), ApiWeatherDataAdd),
    tornado.web.url(r'/api/{version}/weather-data/(?P<weather_data_id>[a-zA-Z0-9]+)'.format(
        version=ApiWeatherDataEdit.version), ApiWeatherDataEdit),
]
