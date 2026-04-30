import os

from jinja2 import Environment

from sand.entities.pages.basic_content_entity import BaseContentEntity

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from sand.config.site import Site

class RawContent(BaseContentEntity):
    def __init__(self, site:"Site", target:str, source:str=None, config:dict=None, **kwargs):
        super().__init__(site, target, source, **kwargs)
        self.page_data = {}
        #The content as read from the page file

        if config is not None and isinstance(config, dict):
            self.page_data.update(config)

        target_url_parts = self.target_url_parse(self.target)
        self.target_url = target_url_parts.target_url
        self.target_url_parts = target_url_parts.target_url_parts

        self.raw_content = self.load_raw_content(self.source_path, self.page_data)

    def render(self, environment:Environment, **kwargs):
        self._debug()
        os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)

        content = ""
        if self.raw_content is not None:
            content = self.raw_content

        with open(self.target_path, "w") as target_file:
            target_file.write(content)

