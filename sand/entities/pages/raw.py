from sand.entities import RenderEntity
import os
import pathlib


class RawContent(RenderEntity):
    def __init__(self, site, target, source=None, config=None, **kwargs):
        super().__init__(site, source, target, **kwargs)
        self.page_data = {}
        #The content as read from the page file
        self.raw_content = None

        if config is not None and isinstance(config, dict):
            self.page_data.update(config)

        if self.source is not None:
            self.source_path = os.path.abspath(os.path.join(self.site.root, self.source))
        else:
            self.source_path = None

        self.target_path = os.path.abspath(os.path.join(self.site.output_root, self.target))
        self.target_url = pathlib.PurePosixPath("/", self.target)
        self.target_url_parts = os.path.split(self.target_url)

        if self.source_path is not None:
            self.raw_content = open(self.source_path, "r").read()
        else:
            self.raw_content = self.page_data.get("static_content", "")

    def render(self, environment, **kwargs):
        print('Rendering raw for (%s)' % self.source_path)
        os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
        with open(self.target_path, "w") as target_file:
            target_file.write(self.raw_content)

