from loguru import logger
from abc import ABC
import os
from typing import TYPE_CHECKING, Union, AnyStr

if TYPE_CHECKING:
    from sand.config.site import Site

class RenderEntity(ABC):
    # Originally this was site, source, target, ... which made sense at the time, however it has become
    # clear that there are frequent use cases where the source may be None, in which case it makes sense
    # to swap them so that we can override __init__ in subclasses to make source optional
    def __init__(self, site:"Site", target:Union[AnyStr, None], source:Union[AnyStr, None], **kwargs):
        self.site = site
        self.source = source
        self.target = target

        self.source_file = self.extract_filename(self.source)
        self.target_file = self.extract_filename(self.target)

        self.source_path = self.default_path(self.source)
        self.target_path = self.default_path(self.target, is_output=True)

        self.target_url = None
        self.target_url_parts = []


    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.source, self.target)

    def _debug(self):
        logger.debug(f"Rendering: {self.__class__.__name__} -> {self.source_file} to {self.target_file}")

    def validate(self):
        """
        Perform a check to see if there's sufficient information to render the entity. In the base class
        we'll simply check that a target is defined, which is about as cursory as we can get.

        :return: A boolean indicating whether the entity meets the requirements to be rendered
        """

        return self.target is not None and self.target != ""

    @staticmethod
    def as_dict():
        return {}

    @staticmethod
    def extract_filename(path:Union[AnyStr, None]) -> Union[AnyStr, None]:
        """
        Extract the filename form the provided path

        :param path: The file path
        :return: The truncated filename or None if the provided path is None
        """

        filename = None

        if path is not None:
            try:
                filename = os.path.split(path)[-1]
            except IndexError:
               filename = path

        return filename

    def default_path(self, path:Union[AnyStr, None], is_output:bool=False) -> Union[AnyStr, None]:
        root = self.site.root

        if is_output:
            root = self.site.output_root

        if path is not None and path != "":
            return os.path.abspath(os.path.join(root, path))

        return None

    def render(self, environment, **kwargs):
        logger.warning("No-op renderer selected, please check your configuration")