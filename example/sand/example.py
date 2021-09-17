class Plugin:
    def configure(self, site_data, site):
        pass

    #Called during the parsing phase of the processing
    def parse(self, site_data, site):
        pass

    def nl2br(self, value):
        return value.replace("\n", "<br />")

    def add_render_context(self, page, environment, data):
        environment.filters["nl2br"] = self.nl2br
