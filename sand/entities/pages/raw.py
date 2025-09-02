from sand.entities import RenderEntity
import os
import pathlib
from sand.entities.pages.content_loading_entity import ContentLoadingEntity


class RawContent(RenderEntity, ContentLoadingEntity):
    def __init__(self, site, target, source=None, config=None, **kwargs):
        super().__init__(site, target, source, **kwargs)
        self.page_data = {}
        #The content as read from the page file
        self.raw_content = None

        if config is not None and isinstance(config, dict):
            self.page_data.update(config)

        target_url_parts = self.target_url_parse(self.target)
        self.target_url = target_url_parts.target_url
        self.target_url_parts = target_url_parts.target_url_parts

        self.raw_content = self.load_raw_content(self.source_path, self.page_data)

    def render(self, environment, **kwargs):
        print('Rendering raw for (%s)' % self.source_path)
        os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
        with open(self.target_path, "w") as target_file:
            target_file.write(self.raw_content)

