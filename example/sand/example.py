class Plugin:
    def configure(self, site_data, site):
        pass

    #Called during the parsing phase of the processing
    def parse(self, site_data, site):
        pass

    @staticmethod
    def nl2br(value):
        return value.replace("\n", "<br />")

    def add_render_context(self, page, environment, data):
        environment.filters["nl2br"] = self.nl2br
