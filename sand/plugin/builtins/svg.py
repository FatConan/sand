import os

from jinja2 import TemplateNotFound
from pyhocon import ConfigFactory
from sand.plugin import SandPlugin
from sand.entities import RenderEntity

# The SVG renderer is designed to read a specification in the form of HOCON from one file and render it using a
# templated jinja2 SVG template to a final form. Typically this means that an svg template is defined in a
# template field in the HOCON and then any other replacement variables are declared alongside it. The drive of this was to
# provide an easy way to, for example, recolour SVGs to that skinning and theming can be done on the fly.
class SvgResource(RenderEntity):
    def __init__(self, site, target, source=None, config=None, **kwargs):
        super().__init__(site, source, target, **kwargs)
        if config is None:
            self.config = ConfigFactory.parse_file(self.source_path)
        else:
            self.config = config

    def to_dict(self, environment):
        return {"DATA": self.config}

    def render(self, environment, compress=True, **kwargs):
        try:
            os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
            with open(self.target_path, "w") as target_file:
                output = environment.get_template(self.config["template"]).render(self.to_dict(self.config))

                if compress:
                    output = self.site.minify(output)

                target_file.write(output)
        except TemplateNotFound as tnf:
            print("Requested template (%s) not found, skipping" % tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, cannot render SVG for (%s)' % self.source_path)
            else:
                raise


class Plugin(SandPlugin):
    def __init__(self):
        pass

    def configure(self, site_data, site):
        #The only thing the plugin does is register the new resource renderer
        site.register_resource_renderer("svg", SvgResource)
