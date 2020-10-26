from tornado.httpclient import HTTPError
from webargs import fields, validate
from webargs.tornadoparser import parser
from http import HTTPStatus
from weather import config
from weather.models.weather import Weather
from sqlalchemy import func
from sqlalchemy_pagination import paginate


class WeatherService(object):

    def __init__(self, request):
        self.request = request
        self.agreement = {
            "target": fields.Str(validate=validate.Length(min=1), required=True),
            "value": fields.Str(validate=validate.Length(min=1), required=True),
            "page": fields.Int(default=0),
            "page_size": fields.Int(default=config.PAGE_SIZE)
        }

    async def process(self):
        params = parser.parse(self.agreement, self.request, location="query")
        target, value = str(params.get('target')).lower(), str(params.get('value')).lower()
        page, size = params.get('page'), params.get('page_size')

        model = Weather()
        query = model.orm.db_session.query(
            Weather.id, Weather.name_station, Weather.latitude, Weather.longitude)
        condition = {
            "name_station": query.filter(func.lower(Weather.name_station).like("%{}%".format(value))),
            "id": query.filter_by(id=value),
        }
        if target not in condition:
            raise HTTPError(code=HTTPStatus.BAD_REQUEST.value, message='target "{}" not found in model'.format(target))

        result = paginate(condition[target], page, size)

        grid_weathers = {'pageCount': result.pages, 'resultsCount': result.total,
                         'next_page': result.next_page, 'previous_page': result.previous_page, 'data': []}
        for obj in result.items:
            dict_weather = {'id': obj.id, 'name_station': str(obj.name_station),
                            'latitude': str(obj.latitude), 'longitude': str(obj.longitude)}

            grid_weathers['data'].append(dict_weather)

        model.orm.remove_session()
        return grid_weathers
