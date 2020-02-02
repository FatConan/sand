from entities.resources.lessresource import LessResource
from entities.resources.resource import PlainResource


class ResourceSelector:
    selection_options = {
        'less': LessResource
    }

    @classmethod
    def select(cls, *args, **kwargs):
        renderer = cls.selection_options.get(kwargs.get("resource_type"), PlainResource)
        return renderer(*args, **kwargs)

