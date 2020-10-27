from tornado_swagger.model import register_swagger_model


@register_swagger_model
class WeatherModelSuccess:
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


@register_swagger_model
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
