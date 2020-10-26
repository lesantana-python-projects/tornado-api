from tornado.httpclient import HTTPError

from weather.services.weather_service import WeatherService
from weather.views import ApiJsonHandler
from http import HTTPStatus


class ApiWeatherDetail(ApiJsonHandler):
    version = 'v1'

    async def get(self):
        """
        ---
        tags:
        - Weather
        summary: Get weathers
        description: 'Get weathers'
        produces:
        - application/json
        parameters:
        -   name: target
            in: query
            description: target field
            enum: [id, name_station]
            required: true
            type: string
        -   name: value
            in: query
            description: Value to search in target field
            required: true
            type: string
        -   name: page
            in: query
            description: page to select
            required: true
            type: string
        -   name: page_size
            in: query
            description: quantity of items
            required: true
            type: string
        responses:
            200:
              description: list of weather
              schema:
                $ref: '#/definitions/WeatherModelSuccess'
            500:
              description: Errors
              schema:
                $ref: '#/definitions/WeatherModelError'

        """
        try:
            instance = WeatherService(request=self.request)
            response = await instance.process()
            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
