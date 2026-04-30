from abc import ABC
from jinja2 import Environment
from typing import TYPE_CHECKING, Union, Dict

if TYPE_CHECKING:
    from sand.config.site import Site
    from sand.entities.pages import Page, RawContent

class SandPlugin(ABC):
    """An abstract base class for plugin classes to the Sand engine. """

    def configure(self, site_data:Dict, site:"Site"):
        """
        This method should be overridden to provide any context-specific configuration that
        the plugin might require, or to configure the site or site_data with requirements
        for the plugin itself. Called during initial setup of the site once all the plugin instances have
        been created.

        :param site_data: the configuration dictionary for the current site
        :param site: the current site
        """
        pass

    def parse(self, site_data:Dict, site:"Site"):
        """

        :param site_data:
        :param site:
        :return:S
        """
        pass

    def add_render_context(self, page:Union["Page", "RawContent"], environment:Environment, data:"Site"):
        """

        :param page:
        :param environment:
        :param data:
        :return:
        """
        pass

