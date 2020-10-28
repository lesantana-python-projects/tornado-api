import logging
from http import HTTPStatus
from tornado.httpclient import HTTPError

from weather.integration import MixinDetail
from weather.integration.weather_data_detail import WeatherDataDetail
from weather.integration.weather_detail import WeatherDetail
from weather.services import ServiceBase

__all__ = ['BaseDefaultFactory', 'WeatherDetail', 'WeatherDataDetail']

LIST_ABSTRACTS = [ServiceBase, MixinDetail]
logger = logging.getLogger(__name__)


class BaseDefaultFactory:
    @staticmethod
    def get_instance(carrier):

        for abstracts_classes in LIST_ABSTRACTS:
            for klass in abstracts_classes.__subclasses__():
                if carrier.lower() == klass.carrier:
                    return klass()
        message = 'instance not found {}'.format(carrier)
        logger.exception(message)
        raise HTTPError(code=HTTPStatus.NOT_FOUND.value, message=message)
