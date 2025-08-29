import os
import pathlib
import warnings

from jinja2.exceptions import TemplateNotFound

from sand.entities import RenderEntity


class Page(RenderEntity):
    def __init__(self, site, target, source=None, config=None, **kwargs):
        super().__init__(site, source, target, **kwargs)
        self.page_data = {}
        #The content as read from the page file
        self.raw_content = None
        self.content = None

        if config is not None and isinstance(config, dict):
            self.page_data.update(config)

        self.target_url = pathlib.PurePosixPath("/", self.target)
        self.target_url_parts = os.path.split(self.target_url)

        if self.source_path is not None:
            self.raw_content = open(self.source_path, "r").read()
        else:
            self.raw_content = self.page_data.get("static_content", "")

        self.convert_to_template_html()

    def to_dict(self, environment):
        data = {
            'GLOBALS': {
                'site': self.site,
                'site_root': self.site.root,
                'output_root': self.site.output_root,
                'uuid': self.site.uuid,
                'overrides': self.site.overrides,
                'base_url': self.site.base_url
            },

            'DATA': self.page_data,

            'source': self.source,
            'target': self.target,
            'source_file': self.source_file,
            'target_file': self.target_file,
            'source_path': self.source_path,
            'target_path': self.target_path,
            'target_url': self.target_url,
            'target_url_parts': self.target_url_parts,
        }

        for plugin in self.site.plugins():
            plugin.add_render_context(self, environment, data)

        if self.page_data.get("jinja_pass", False):
            data["content"] = environment.from_string(self.content).render(data)
        else:
            data["content"] = self.content

        return data

    def data(self, key, default=None, conversion=lambda x: x):
        return conversion(self.page_data.get(key, default))

    def convert_to_template_html(self):
        # First render out the markdown and collection the YAML data
        self.site.renderer.reset()
        self.content = self.site.renderer.convert(self.raw_content)
        local_template_data = {}
        for key, value in self.site.renderer.Meta.items():
            if isinstance(value, list) and len(value) == 1:
                local_template_data[key] = value[0]
            else:
                local_template_data[key] = value
        self.page_data.update(local_template_data)

    def render(self, environment, compress=True, **kwargs):
        try:
            os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
            with open(self.target_path, "w") as target_file:
                output = environment.get_template(self.page_data["template"]).render(self.to_dict(environment))

                if compress:
                    output = self.site.minify(output)

                target_file.write(output)

        except TemplateNotFound as tnf:
            warnings.warn("Requested template (%s) not found, skipping" % tnf)

        except KeyError as ke:
            if str(ke) == '\'template\'':
                warnings.warn('Missing template, rendering markdown only for (%s)' % self.source_path)
                os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
                with open(self.target_path, "w") as target_file:
                    output = self.to_dict(environment)["content"]

                    if compress:
                        output = self.site.minify(output)

                    target_file.write(output)
            else:
                raise
