from tornado.httpclient import HTTPError

from weather.exceptions import KNOWN_ERRORS
from weather.services.base_factory import BaseDefaultFactory
from weather.views import ApiJsonHandler
from http import HTTPStatus


class ApiWeatherDetail(ApiJsonHandler):
    version = 'v1'

    async def get(self):
        """
        ---
        tags:
          - Weather Location Place List
        summary: Get weathers
        description: 'Get weathers'
        operationId: getWeather
        parameters:
          - name: target
            in: query
            description: target field
            required: true
            schema:
              enum: [id, name_station]
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
            instance = BaseDefaultFactory.get_instance(carrier='weather_detail')
            response = await instance.process(params=await instance.agreement(request=self.request))
            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)


class ApiWeatherEdit(ApiJsonHandler):
    version = 'v1'

    async def get(self, weather_id):
        """
        ---
        tags:
          - Weather Location Place
        summary: Get specific weather location place
        description: 'Get specific weather location place'
        operationId: getWeatherId
        parameters:
          - name: weather_id
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
            instance = BaseDefaultFactory.get_instance(carrier='weather')
            await instance.agreement(request=self.request)

            response = await instance.process(params={'id': weather_id}, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)

    async def put(self, weather_id):
        """
        ---
        tags:
          - Weather Location Place
        summary: Update specific weather location place
        description: Update specific weather location place
        operationId: UpdateWeather
        parameters:
          - name: weather_id
            in: path
            description: id to update weather
            required: true
            schema:
              type: integer
              format: int64
        requestBody:
          description: payload to update weather
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WeatherModel'
          required: true
        responses:
            '200':
              description: update specific of weather
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
            instance = BaseDefaultFactory.get_instance(carrier='weather')
            params = await instance.agreement(request=self.request, name_station=True)

            params.update({'id': weather_id})
            response = await instance.process(params=params, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)

    async def delete(self, weather_id):
        """
        ---
        tags:
          - Weather Location Place
        summary: Delete specific weather location place
        description: Delete specific weather location place
        operationId: DeleteWeather
        parameters:
          - name: weather_id
            in: path
            description: id to delete weather
            required: true
            schema:
              type: integer
              format: int64
        responses:
         '200':
           description: delete specific of weather
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
            instance = BaseDefaultFactory.get_instance(carrier='weather')
            params = await instance.agreement(request=self.request)

            params.update({'id': weather_id})
            response = await instance.process(params=params, method=self.request.method)

            self.success(code=HTTPStatus.OK.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)


class ApiWeatherAdd(ApiJsonHandler):
    version = 'v1'

    async def post(self):
        """
        ---
        tags:
          - Weather Location Place
        summary: Add weather location location
        description: Add weather location location
        operationId: AddWeather
        requestBody:
          description: payload to add weather location
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WeatherModel'
          required: true
        responses:
          '201':
            description: create specific of weather
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
            instance = BaseDefaultFactory.get_instance(carrier='weather')
            params = await instance.agreement(
                request=self.request, name_station=True, latitude=True, longitude=True, location='json')

            response = await instance.process(params=params, method=self.request.method)
            self.success(code=HTTPStatus.CREATED.value, message=response)
        except HTTPError as error:
            self.error(code=error.code, message=error.message)
        except KNOWN_ERRORS as error:
            self.error(code=error.code, message=error.message)
