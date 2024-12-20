from sand.entities.resources.lessresource import LessResource
from sand.entities.resources.resource import PlainResource
from sand.entities.resources.scssresource import ScssResource


class ResourceSelector:
    selection_options = {
        'less': LessResource,
        'scss': ScssResource
    }

    @classmethod
    def select(cls, *args, **kwargs):
        resource_type = kwargs.pop("resource_type", None)
        renderer = cls.selection_options.get(resource_type, PlainResource)
        return renderer(*args, **kwargs)

