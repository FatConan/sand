import os
import pathlib

from sand.entities import RenderEntity

class TargetUrlParts:
    def __init__(self, target_url, target_url_parts):
        self.target_url = target_url
        self.target_url_parts = target_url_parts

    @classmethod
    def blank(cls):
        return TargetUrlParts(None, [])

class ContentLoadingEntity:
    def load_raw_content(self, source_path, page_data):
        raw_content = None

        if source_path is not None:
            try:
                raw_content = open(source_path, "r").read()
            except FileNotFoundError:
                pass
        else:
            raw_content = page_data.get("static_content", "")

        return raw_content

    def target_url_parse(self, target):
        if target is not None:
            target_url = pathlib.PurePosixPath("/", target)
            target_url_parts = os.path.split(target_url)
            return TargetUrlParts(target_url, target_url_parts)
        return TargetUrlParts.blank()