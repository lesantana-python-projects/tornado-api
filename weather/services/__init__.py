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


class ServiceBaseDetail(metaclass=ABCMeta):
    @abstractmethod
    async def query_mount(self, target, value, page, size):
        raise NotImplementedError("Implement me")

    @abstractmethod
    async def result_mount(self, obj):
        raise NotImplementedError("Implement me")


class ServiceBase(metaclass=ABCMeta):

    @abstractmethod
    async def process(self, params):
        raise NotImplementedError("Implement me")

    @abstractmethod
    async def agreement(self, request):
        raise NotImplementedError("Implement me")
