from sand.plugin import SandPlugin

from .specialmarkdown.CodeBlocks import BoxExtension


class Plugin(SandPlugin):
    def configure(self, site_data, site):
        # Here we're going to change the way code is rendered
        BoxExtension().extendMarkdown(site.renderer)