from entities.page import Page
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
import os
import glob
import shutil
import re
import uuid

from entities.resources.resource_selector import ResourceSelector


class Site(object):
    def __init__(self, root, site_data):
        self.wildcard_re = re.compile("([^\*]*)\*(\..+)")

        self.renderer = markdown.Markdown(
            extensions=['markdown.extensions.meta', 'markdown.extensions.toc']
        )
        self.pages = []
        self.page_reference = {}
        self.templates = []
        self.resources = []

        self.root = os.path.join(root, site_data.get("root"))

        output_relative = site_data.get("output_root", "output")
        if output_relative:
            self.output_root = os.path.join(self.root, output_relative)
        else:
            self.output_root = os.path.join(self.root, "output")

        self.uuid = uuid.uuid4()

        self.site_data = site_data
        self._parse(site_data)

    def __repr__(self):
        return "SiteConfig(%r, %r, %r)" % (self.root, self.output_root, self.site_data)

    def process_wildcards(self, entities):
        processed_entities = []

        for entity in entities:
            source = entity.get("source", "")
            target = entity.get("target", "")
            source_match = self.wildcard_re.match(source)
            target_match = self.wildcard_re.match(target)

            if source_match and target_match:
                listed_sources = glob.glob(os.path.abspath(os.path.join(self.root, source)))
                for list_source in listed_sources:
                    pre, post = source_match.groups()
                    filename = list_source.split("/")[-1].replace(post, "")

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

    def _parse(self, data):
        """Load pages to be generated"""
        self.templates = [os.path.join(self.root, template) for template in data.get("templates", [])]
        for t in self.templates:
            print("Found template %s" % t)

        self.environment = Environment(
            loader=FileSystemLoader(self.templates),
            autoescape=select_autoescape(["html", "xml"])
        )

        processed_pages = self.process_wildcards(data.get("pages", []))
        for page_dict in processed_pages:
            page = Page(self, **page_dict)
            self.pages.append(page)

            path, file = page.target_url_parts
            try:
                self.page_reference[path].append((file, page))
            except KeyError:
                self.page_reference[path] = [(file, page), ]

        self.resources = [ResourceSelector.select(self, **resource) for resource in data.get("resources", [])]

    def render(self):
        shutil.rmtree(os.path.abspath(self.output_root), ignore_errors=True)

        for page in self.pages:
            page.render(self.environment)

        for resource in self.resources:
            resource.render(self.environment)



