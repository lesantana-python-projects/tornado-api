from tornado_swagger.components import components


@components.schemas.register
class WeatherRequest:
    """
    ---
    type: object
    description: Weather model representation
    properties:
        message:
            type: object
        status:
            type: string
    """


@components.schemas.register
class ArrayOfModel:
    """
    ---
    type: object
    description: Weather model representation
    properties:
        message:
            type: object
        status:
            type: string
    """


@components.schemas.register
class ModelError:
    """
    ---
    type: object
    description: Weather Errors
    properties:
        message:
            type: string
            description: The user ID.
        status:
            type: string
    """


@components.schemas.register
class WeatherModel(object):
    """
    ---
    type: object
    description: Weather model representation
    properties:
        name_station:
            type: string
        latitude:
            type: number
        longitude:
            type: number
    """


@components.schemas.register
class WeatherDataModel(object):
    """
    ---
    type: object
    description: Weather model representation
    properties:
        date:
            type: string
        hour:
            type: integer
        precipitation:
            type: number
        dry_bulb_temperature:
            type: number
        wet_bulb_temperature:
            type: number
        high_temperature:
            type: number
        low_temperature:
            type: number
        relative_humidity:
            type: number
        relative_humidity_avg:
            type: number
        pressure:
            type: number
        sea_pressure:
            type: number
        wind_direction:
            type: number
        wind_speed_avg:
            type: number
        cloud_cover:
            type: number
        evaporation:
            type: number
        weather_id:
            type: integer
    """
