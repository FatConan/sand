import os

from jinja2 import Environment

from sand.entities import RenderEntity
from sand.entities.pages.content_loading_entity import ContentLoadingEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sand.config.site import Site

class TargetUrlParts:
    def __init__(self, target_url:str, target_url_parts:list[str]):
        self.target_url = target_url
        self.target_url_parts = target_url_parts

class RawContent(RenderEntity, ContentLoadingEntity):
    def __init__(self, site:"Site", target:str, source:str=None, config:dict=None, **kwargs):
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

    def render(self, environment:Environment, **kwargs):
        self._debug()
        os.makedirs(os.path.split(self.target_path)[0], exist_ok=True)
        with open(self.target_path, "w") as target_file:
            target_file.write(self.raw_content)

