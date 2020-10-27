from tornado.httpclient import HTTPError
from weather.services.base_factory import BaseDefaultFactory
from weather.views import ApiJsonHandler
from http import HTTPStatus


class ApiWeatherDataDetail(ApiJsonHandler):
    version = 'v1'

    async def get(self):
        """
        ---
        tags:
        - Weather Data
        summary: Get weathers
        description: 'Get weathers'
        produces:
        - application/json
        parameters:
        -   name: target
            in: query
            description: target field
            enum: [id, date, hour, precipitation, dry_bulb_temperature, wet_bulb_temperature, high_temperature,
            low_temperature, relative_humidity, relative_humidity_avg, pressure, sea_pressure, wind_direction,
            wind_speed_avg, cloud_cover, evaporation, name_station]
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
            instance = BaseDefaultFactory.get_instance(carrier='weather_data_detail')
            response = await instance.process(params=await instance.agreement(request=self.request))
            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
