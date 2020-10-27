import tornado

from weather.views.api.v1.api_weather import ApiWeatherDetail
from weather.views.api.v1.api_weather_data import ApiWeatherDataDetail
from weather.views.healthcheck import HealthcheckApi

routes = [
    tornado.web.url(r'/api/healthcheck', HealthcheckApi),
    tornado.web.url(r'/api/{version}/weather'.format(version=ApiWeatherDetail.version), ApiWeatherDetail),
    tornado.web.url(r'/api/{version}/weather-data'.format(version=ApiWeatherDataDetail.version), ApiWeatherDataDetail)
]
