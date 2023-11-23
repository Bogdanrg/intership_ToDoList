from analytical_service.services import AnalyticalServices


class IndexRegistryBase(type):
    INDEX_METHODS_REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        for key, value in attrs.items():
            if callable(value):
                cls.INDEX_METHODS_REGISTRY[f"{key}_{attrs['index_name']}"] = value
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.INDEX_METHODS_REGISTRY)


class BaseRegisteredIndexClass(metaclass=IndexRegistryBase):
    index_name: str = None

    @staticmethod
    def search(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def add(*args, **kwargs):
        raise NotImplementedError()


class PhoneIndex(BaseRegisteredIndexClass):
    index_name = 'phone'

    @staticmethod
    def search(data: dict):
        await AnalyticalServices.search_phone_document(data)

    @staticmethod
    def add(data: dict):
        await AnalyticalServices.create_phone_document(data)


class FoodIndex(BaseRegisteredIndexClass):
    index_name = 'food'

    @staticmethod
    def search(data: dict):
        await AnalyticalServices.search_food_document(data)

    @staticmethod
    def add(data):
        await AnalyticalServices.create_food_document(data)
