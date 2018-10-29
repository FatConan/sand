from entities.render_entity import RenderEntity
import os

from jinja2.exceptions import TemplateNotFound


class Page(RenderEntity):
    def __init__(self, md_renderer, site_root, output_root, source, target, page_type=None):
        super().__init__(site_root, output_root, source, target)
        self.page_type = page_type
        self.data = {}

        self.source_path = os.path.abspath(os.path.join(self.site_root, self.source))
        self.target_path = os.path.abspath(os.path.join(self.output_root, self.target))

        self.content = open(self.source_path, "r").read()
        self.renderer = md_renderer

    def to_dict(self):
        data =  {
            'site_root': self.site_root,
            'output_root': self.output_root,
            'page_type': self.page_type,
            'source': self.source,
            'target': self.target,
            'source_path': self.source_path,
            'target_path': self.target_path,
            'content': self.content,
        }
        data.update(self.data)
        return data

    def convert_to_template_html(self):
        self.content = self.renderer.convert(self.content)
        for key, value in self.renderer.Meta.items():
            if isinstance(value, list) and len(value) == 1:
                self.data[key] = value[0]
            else:
                self.data[key] = value

    def render(self, environment):
        print("Render %s" % self)

        self.convert_to_template_html()

        try:
            os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
            with open(self.target_path, "w") as target_file:
                target_file.write(
                    environment.get_template(self.data["template"]).render(self.to_dict())
                )
        except TemplateNotFound as tnf:
            print("Requested template (%s) not found, skipping" % tnf)
        except KeyError as ke:
            if str(ke) == '\'template\'':
                print('Missing template, rendering markdown only')
                environment.from_string(self.content).render(self.to_dict())
            else:
                raise
