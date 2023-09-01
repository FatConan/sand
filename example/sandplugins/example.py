from sand.plugin import SandPlugin


class Plugin(SandPlugin):
    @staticmethod
    def nl2br(value):
        return value.replace("\n", "<br />")

    def add_render_context(self, page, environment, data):
        environment.filters["nl2br"] = self.nl2br
