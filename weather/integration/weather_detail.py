import logging

from tornado.httpclient import HTTPError
from weather.integration import MixinDetail
from weather.models.weather import Weather
from sqlalchemy import func
from http import HTTPStatus

from weather.services import ServiceBase
from weather.services.paginator import paginate
from weather.useful_tools.controller_util import weather_response, default_exception_error

logger = logging.getLogger(__name__)


class WeatherDetail(MixinDetail, ServiceBase):
    carrier = 'weather_detail'

    async def query_mount(self, target, value, page, size):
        """ query mount Weather Detail """
        model = Weather()
        query = model.orm.db_session.query(
            Weather.id, Weather.name_station, Weather.latitude, Weather.longitude)

        condition = {
            "name_station": query.filter(func.lower(Weather.name_station).like("%{}%".format(value))),
            "id": query.filter_by(id=value),
        }

        if target not in condition:
            message = 'target "{}" not found in model Weather'.format(target)
            logger.error(message)
            raise HTTPError(code=HTTPStatus.BAD_REQUEST.value, message=message)

        result = {}
        try:
            result = paginate(condition[target], page, size)
        except model.KNOWN_ERROR_SQLALCHEMY.get('known_errors') as error:
            default_exception_error(model=model, error=error)

        model.orm.remove_session()
        return result

    async def result_mount(self, obj):
        """ result mount """
        return weather_response(obj)

    async def process(self, params, **kwargs):
        return await self._run_process(params)
