from entities.render_entity import RenderEntity
import os

from jinja2.exceptions import TemplateNotFound


class Page(RenderEntity):
    def __init__(self, site, source, target, page_type=None, config={}): #itle=None, template=None, page_type=None):
        super().__init__(site, source, target)
        self.page_type = page_type
        self.page_data = {}
        self.page_data.update(config)

        self.source_path = os.path.abspath(os.path.join(self.site.root, self.source))
        self.target_path = os.path.abspath(os.path.join(self.site.output_root, self.target))
        self.target_url = os.path.abspath(os.path.join("/", self.target))
        self.target_url_parts = os.path.split(self.target_url)

        self.raw_content = open(self.source_path, "r").read()
        self.content = None
        self.convert_to_template_html()

    def to_dict(self, environment):
        data =  {
            'GLOBALS': {
                'site': self.site,
                'site_root': self.site.root,
                'output_root': self.site.output_root,
            },

            'DATA': self.page_data,

            'page_type': self.page_type,
            'source': self.source,
            'target': self.target,
            'source_path': self.source_path,
            'target_path': self.target_path,
            'target_url': self.target_url,
            'target_url_parts': self.target_url_parts,
        }
        if self.page_data.get("jinja_pass", False):
            data["content"] = environment.from_string(self.raw_content).render(data)
        else:
            data["content"] = self.raw_content
        return data

    def data(self, key, default=None, conversion=lambda x: x):
        return conversion(self.page_data.get(key, default))

    def convert_to_template_html(self):
        # First render out the markdown and collection the YAML data
        self.raw_content = self.site.renderer.convert(self.raw_content)
        for key, value in self.site.renderer.Meta.items():
            if isinstance(value, list) and len(value) == 1:
                self.page_data[key] = value[0]
            else:
                self.page_data[key] = value

    def render(self, environment):
        print("Render %s" % self)

        try:
            os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
            with open(self.target_path, "w") as target_file:
                target_file.write(
                    environment.get_template(self.page_data["template"]).render(self.to_dict(environment))
                )
        except TemplateNotFound as tnf:
            print("Requested template (%s) not found, skipping" % tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, rendering markdown only')
                os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
                with open(self.target_path, "w") as target_file:
                    target_file.write(
                        self.to_dict(environment)["content"]
                    )

            else:
                raise
