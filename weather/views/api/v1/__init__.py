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
class ArrayOfPostModel:
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
class WeatherModelError:
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
