from sand.entities import RenderEntity
from sand.entities.pages.content_loading_entity import ContentLoadingEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sand.config.site import Site

class BaseContentEntity(RenderEntity, ContentLoadingEntity):
    raw_content = None