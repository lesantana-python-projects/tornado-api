from tornado.httpclient import HTTPError

from weather.exceptions import KNOWN_ERRORS
from weather.services.base_factory import BaseDefaultFactory
from weather.views import ApiJsonHandler
from http import HTTPStatus


class ApiWeatherDataDetail(ApiJsonHandler):
    version = 'v1'

    async def get(self):
        """
        ---
        tags:
          - Weather Data List
        summary: Get weathers
        description: 'Get weathers'
        operationId: getWeather
        parameters:
          - name: target
            in: query
            description: target field
            required: true
            schema:
              enum: [id, date, hour, precipitation, dry_bulb_temperature, wet_bulb_temperature, high_temperature,
            low_temperature, relative_humidity, relative_humidity_avg, pressure, sea_pressure, wind_direction,
            wind_speed_avg, cloud_cover, evaporation, name_station]
              type: string
          - name: value
            in: query
            description: value to search in target field
            required: true
            schema:
              type: string
          - name: page
            in: query
            description: page to initial select
            required: true
            schema:
              type: string
          - name: page_size
            in: query
            description: quantity of items
            required: true
            schema:
              type: string
        responses:
            '200':
              description: list of weather
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ArrayOfModel'
            'errors':
              description: response errors
              content:
               application/json:
                schema:
                  $ref: '#/components/schemas/ArrayOfModel'
        """
        try:
            instance = BaseDefaultFactory.get_instance(carrier='weather_data_detail')
            response = await instance.process(params=await instance.agreement(request=self.request))
            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)


class ApiWeatherDataEdit(ApiJsonHandler):
    version = 'v1'

    async def get(self, weather_data_id):
        """
        ---
        tags:
          - Weather Data
        summary: Get specific weather data
        description: 'Get specific weather data'
        operationId: getWeatherData
        parameters:
          - name: weather_data_id
            in: path
            description: weather place id
            required: true
            schema:
              type: integer
        responses:
            '200':
              description: get specific of weather
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ArrayOfModel'
            'errors':
              description: response errors
              content:
               application/json:
                schema:
                  $ref: '#/components/schemas/ArrayOfModel'
        """
        try:
            instance = BaseDefaultFactory.get_instance(carrier='weather-data')
            await instance.agreement(request=self.request)

            response = await instance.process(params={'id': weather_data_id}, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)

    async def put(self, weather_data_id):
        """
        ---
        tags:
          - Weather Data
        summary: Update specific weather data
        description: Update specific weather data
        operationId: UpdateWeatherData
        parameters:
          - name: weather_data_id
            in: path
            description: id to update weather data
            required: true
            schema:
              type: integer
              format: int64
        requestBody:
          description: payload to update weather data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WeatherDataModel'
          required: true
        responses:
            '200':
              description: update specific of weather data
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ArrayOfModel'
            'errors':
              description: response errors
              content:
               application/json:
                schema:
                  $ref: '#/components/schemas/ArrayOfModel'
        """
        try:
            instance = BaseDefaultFactory.get_instance(carrier='weather-data')
            params = await instance.agreement(
                request=self.request)

            params.update({'id': weather_data_id})
            response = await instance.process(params=params, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)

    async def delete(self, weather_data_id):
        """
            ---
            tags:
              - Weather Data
            summary: Delete specific weather data
            description: Delete specific weather data
            operationId: DeleteWeatherData
            parameters:
              - name: weather_data_id
                in: path
                description: id to delete weather data
                required: true
                schema:
                  type: integer
                  format: int64
            responses:
             '200':
               description: delete specific of weather data
               content:
                 application/json:
                   schema:
                     $ref: '#/components/schemas/ArrayOfModel'
             'errors':
               description: response errors
               content:
                application/json:
                 schema:
                   $ref: '#/components/schemas/ArrayOfModel'
            """
        try:
            instance = BaseDefaultFactory.get_instance(carrier='weather-data')
            params = await instance.agreement(request=self.request)

            params.update({'id': weather_data_id})
            response = await instance.process(params=params, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)


class ApiWeatherDataAdd(ApiJsonHandler):
    version = 'v1'

    async def post(self):
        """
        ---
        tags:
          - Weather Data
        summary: Add weather data
        description: Add weather data
        operationId: AddWeatherData
        requestBody:
          description: payload to add weather data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WeatherDataModel'
          required: true
        responses:
          '201':
            description: create specific of weather data
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ArrayOfModel'
          'errors':
            description: response errors
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/ArrayOfModel'
        """
        try:
            instance = BaseDefaultFactory.get_instance(carrier='weather-data')
            params = await instance.agreement(
                request=self.request, date=True, hour=True, weather_id=True, location='json')

            response = await instance.process(params=params, method=self.request.method)
            self.success(code=HTTPStatus.CREATED.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)
