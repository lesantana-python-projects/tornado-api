import logging

from marshmallow import validate
from webargs import fields
from webargs.tornadoparser import parser
from weather.integration import MixinBase
from weather.models.weather import Weather
from weather.models.weather_data import WeatherData
from weather.services import ServiceBase
from weather.useful_tools.controller_util import weather_data_response, default_exception_error

logger = logging.getLogger(__name__)


class WeatherDataController(MixinBase, ServiceBase):
    carrier = 'weather-data'

    def __init__(self):
        self.model = WeatherData()

    async def agreement(self, request, **kwargs):

        agreement_v1 = {
            "date": fields.Str(required=kwargs.get('date', False), validate=validate.Length(min=1)),
            "hour": fields.Int(required=kwargs.get('hour', False)),
            "precipitation": fields.Float(required=kwargs.get('precipitation', False)),
            "dry_bulb_temperature": fields.Float(required=kwargs.get('dry_bulb_temperature', False)),
            "wet_bulb_temperature": fields.Float(required=kwargs.get('wet_bulb_temperature', False)),
            "high_temperature": fields.Float(required=kwargs.get('high_temperature', False)),
            "low_temperature": fields.Float(required=kwargs.get('low_temperature', False)),
            "relative_humidity": fields.Float(required=kwargs.get('relative_humidity', False)),
            "relative_humidity_avg": fields.Float(required=kwargs.get('relative_humidity_avg', False)),
            "pressure": fields.Float(required=kwargs.get('pressure', False)),
            "sea_pressure": fields.Float(required=kwargs.get('sea_pressure', False)),
            "wind_direction": fields.Float(required=kwargs.get('wind_direction', False)),
            "wind_speed_avg": fields.Float(required=kwargs.get('wind_speed_avg', False)),
            "cloud_cover": fields.Float(required=kwargs.get('cloud_cover', False)),
            "evaporation": fields.Float(required=kwargs.get('evaporation', False)),
            "weather_id": fields.Float(required=kwargs.get('weather_id', False), validate=lambda p: p > 0)}

        params = parser.parse(agreement_v1, request, location=(kwargs.get('location', 'json')))

        return params

    async def _get_object_weather_data(self, **kwargs):
        return self.model.orm.db_session.query(WeatherData).filter_by(id=int(kwargs.get('id')))

    async def _get_object_weather_data_join(self, **kwargs):
        return self.model.orm.db_session.query(WeatherData, Weather).join(Weather).filter(
            WeatherData.id == int(kwargs.get('id')))

    async def method_get(self, **kwargs):
        query = await self._get_object_weather_data_join(**kwargs)

        result = query.first()
        response = {}
        if result:
            response.update(weather_data_response(result))

        self.model.orm.remove_session()
        return response

    async def method_put(self, **kwargs):
        weather_data = await self._get_object_weather_data(**kwargs)

        try:
            weather_data.update(kwargs)
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        data_updated = await self._get_object_weather_data_join(**kwargs)
        self.model.orm.object_commit(weather_data.first())

        result = weather_data_response(data_updated.first())
        self.model.orm.remove_session()

        return result

    async def method_delete(self, **kwargs):
        weather_data = await self._get_object_weather_data(**kwargs)
        try:
            self.model.orm.delete_object(weather_data.first())
            self.model.orm.remove_session()
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        return 'object deleted successfully'

    async def method_post(self, **kwargs):
        try:
            weather_data_post = WeatherData(**kwargs)
            self.model.orm.object_commit(weather_data_post)
        except self.model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=self.model, error=error)

        return 'object created successfully'

    async def process(self, params, **kwargs):
        return await self._run_process(params, **kwargs)
