class SandPlugin:
    def configure(self, site_data, site):
        """
        This method should be overridden to provide any context-specific configuration that
        the plugin might require, or to configure the site or site_data with requirements
        for the plugin itself. Called during initial setup of the site once all the plugin instances have
        been created.

        :param site_data: the configuration dictionary for the current site
        :param site: the current site
        :return:
        """
        pass

    def parse(self, site_data, site):

        pass

    def add_render_context(self, page, environment, data):
        pass

