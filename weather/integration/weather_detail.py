import logging

from tornado.httpclient import HTTPError
from http import HTTPStatus
from weather.integration import MixinDetail
from weather.models.weather import Weather
from sqlalchemy import func

from weather.services import ServiceBase
from weather.services.paginator import paginate

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

        result = paginate(condition[target], page, size)
        model.orm.remove_session()
        return result

    async def result_mount(self, obj):
        """ result mount """
        return {'id': obj.id, 'name_station': str(obj.name_station),
                'latitude': str(obj.latitude), 'longitude': str(obj.longitude)}

    async def process(self, params):
        return await self._run_process(params)
