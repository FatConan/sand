import glob
import os
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sand.plugin import SandPlugin
from sand.helpers.wildcard_processor import process_wildcards as helper_wildcard_processor

class Plugin(SandPlugin):
    def __init__(self):
        self.wildcard_re = re.compile(r"([^\*]*)\*([\.]{0,1}.*)")

    def process_wildcards(self, entities, site):
        processed_entities = []

        for entity in entities:
            source = entity.get("source", "")
            target = entity.get("target", "")
            replacements = helper_wildcard_processor(source, target, site)

            for replacement in replacements:
                if replacement.is_wild():
                    entity_copy = entity.copy()
                    entity_copy["source"] = replacement.source
                    entity_copy["target"] = replacement.target
                    entity_copy["wildcard_filename"] = replacement.wildcard_filename
                    processed_entities.append(entity_copy)
                else:
                    processed_entities.append(entity)
        return processed_entities

    def parse(self, site_data, site):
        """Load pages to be generated"""
        site.templates = [os.path.join(site.root, template) for template in site_data.get("templates", [])]
        for t in site.templates:
            print("Found template %s" % t)

        site.environment = Environment(
            loader=FileSystemLoader(site.templates),
            autoescape=select_autoescape(["html", "xml"])
        )

        site.overrides = site_data.get("overrides", {})

        processed_pages = self.process_wildcards(site_data.get("pages", []), site)
        for page_dict in processed_pages:
            site.add_page(page_dict)

        processed_resources = self.process_wildcards(site_data.get("resources", []), site)
        for resource_dict in processed_resources:
            site.add_resource(resource_dict)
