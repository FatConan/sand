import glob
import os
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sand.entities.resources.resource_selector import ResourceSelector
from sand.plugin import SandPlugin


class Plugin(SandPlugin):
    def __init__(self):
        self.wildcard_re = re.compile("([^\*]*)\*(\..+)")

    def process_wildcards(self, entities, site):
        processed_entities = []

        for entity in entities:
            source = entity.get("source", "")
            target = entity.get("target", "")
            source_match = self.wildcard_re.match(source)
            target_match = self.wildcard_re.match(target)

            if source_match and target_match:
                listed_sources = glob.glob(os.path.abspath(os.path.join(site.root, source)))
                for list_source in listed_sources:
                    pre, post = source_match.groups()
                    filename = os.path.split(list_source)[-1].replace(post, "")

                    replace_target = target.replace("*", filename)
                    replace_source = source.replace("*", filename)

                    entity_copy = entity.copy()
                    entity_copy["source"] = replace_source
                    entity_copy["target"] = replace_target
                    processed_entities.append(entity_copy)
            elif source_match or target_match:
                print("Badly formed source and target pairing, %s and %s", (source, target))
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
        site.resources = [ResourceSelector.select(site, **resource) for resource in processed_resources]
