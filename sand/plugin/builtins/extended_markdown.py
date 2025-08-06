from sand.plugin import SandPlugin

from .specialmarkdown.CodeBlocks import BoxExtension


class Plugin(SandPlugin):
    def configure(self, site_data, site):
        config_options = site_data.get("extended_markdown", {})
        # Here we're going to change the way code is rendered
        BoxExtension(config_options).extendMarkdown(site.renderer)