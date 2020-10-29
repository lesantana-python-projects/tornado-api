from abc import ABCMeta, abstractmethod


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @staticmethod
    def drop():
        """Drop the instance (for testing purposes)"""
        Singleton._instances = {}


class ServiceHTTPCommon(metaclass=ABCMeta):
    @abstractmethod
    def method_get(self, **kwargs):
        raise NotImplementedError("Implement me")

    @abstractmethod
    def method_put(self, **kwargs):
        raise NotImplementedError("Implement me")


class ServiceBaseDetail(metaclass=ABCMeta):
    @abstractmethod
    def query_mount(self, target, value, page, size):
        raise NotImplementedError("Implement me")

    @abstractmethod
    def result_mount(self, obj):
        raise NotImplementedError("Implement me")


class ServiceBase(metaclass=ABCMeta):

    @abstractmethod
    def process(self, params, **kwargs):
        raise NotImplementedError("Implement me")

    @abstractmethod
    def agreement(self, request):
        raise NotImplementedError("Implement me")
