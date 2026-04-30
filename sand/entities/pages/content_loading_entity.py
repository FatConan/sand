import os
import pathlib
from typing import Union, AnyStr, List, Dict, Tuple
from pathlib2 import PurePosixPath


class TargetUrlParts:
    def __init__(self, target_url:Union[PurePosixPath, None], target_url_parts:Union[Tuple[AnyStr, AnyStr], None]):
        self.target_url = target_url
        self.target_url_parts = target_url_parts

    @staticmethod
    def blank():
        return TargetUrlParts(None, None)

class ContentLoadingEntity:
    @staticmethod
    def load_raw_content(source_path:AnyStr, page_data:Dict) -> Union[AnyStr|None]:
        raw_content = None

        if source_path is not None:
            try:
                raw_content = open(source_path, "r").read()
            except FileNotFoundError:
                pass
        else:
            raw_content = page_data.get("static_content", "")

        return raw_content

    @staticmethod
    def target_url_parse(target:AnyStr):
        if target is not None:
            target_url = pathlib.PurePosixPath("/", target)
            target_url_parts = os.path.split(target_url)
            return TargetUrlParts(target_url, target_url_parts)
        return TargetUrlParts.blank()