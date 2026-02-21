from abc import ABC, abstractmethod

class SandPlugin(ABC):
    """An abstract base class for plugin classes to the Sand engine. """

    def configure(self, site_data, site):
        """
        This method should be overridden to provide any context-specific configuration that
        the plugin might require, or to configure the site or site_data with requirements
        for the plugin itself. Called during initial setup of the site once all the plugin instances have
        been created.

        :param site_data: the configuration dictionary for the current site
        :param site: the current site
        """
        pass

    def parse(self, site_data, site):
        """

        :param site_data:
        :param site:
        :return:
        """
        pass

    def add_render_context(self, page, environment, data):
        """

        :param page:
        :param environment:
        :param data:
        :return:
        """
        pass

