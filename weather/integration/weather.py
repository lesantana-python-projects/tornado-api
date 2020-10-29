import logging

from marshmallow import validate
from webargs import fields
from webargs.tornadoparser import parser

from weather.integration import MixinBase
from weather.models.weather import Weather
from weather.services import ServiceBase

from weather.useful_tools.controller_util import weather_response, default_exception_error

logger = logging.getLogger(__name__)


class WeatherController(MixinBase, ServiceBase):
    carrier = 'weather'

    def __init__(self):
        self.model = Weather()

    async def agreement(self, request, **kwargs):
        agreement = {"latitude": fields.Float(required=kwargs.get('latitude', False)),
                     "longitude": fields.Float(required=kwargs.get('longitude', False)),
                     "name_station": fields.Str(
                         required=kwargs.get('name_station', False), validate=validate.Length(min=1))}

        params = parser.parse(agreement, request, location=(kwargs.get('location', 'json')))
        return params

    def __get_object_weather(self, **kwargs):
        return self.model.orm.db_session.query(Weather).filter_by(id=int(kwargs.get('id')))

    async def method_get(self, **kwargs):
        query = self.__get_object_weather(**kwargs)

        result = query.first()
        response = {}
        if result:
            response.update(weather_response(result))

        self.model.orm.remove_session()
        return response

    async def method_put(self, **kwargs):
        weather = self.__get_object_weather(**kwargs)

        try:
            weather.update(kwargs)
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        result = weather_response(weather.first())
        self.model.orm.object_commit(weather.first())
        self.model.orm.remove_session()

        return result

    async def method_delete(self, **kwargs):
        weather = self.__get_object_weather(**kwargs)
        try:
            self.model.orm.delete_object(weather.first())
            self.model.orm.remove_session()
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        return 'object deleted successfully'

    async def method_post(self, **kwargs):
        try:
            weather_post = Weather(**kwargs)
            self.model.orm.object_commit(weather_post)
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        return 'object created successfully'

    async def process(self, params, **kwargs):
        return await self._run_process(params, **kwargs)
