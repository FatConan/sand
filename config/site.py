from entities.page import Page
from entities.resource import PlainResource
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
import os
import glob


class Site(object):
    def __init__(self, root, data):
        self.markdown_renderer = markdown.Markdown(
            extensions=['markdown.extensions.meta', 'markdown.extensions.toc']
        )
        self.pages = []
        self.index = []
        self.root = root
        self.templates = []
        self.resources = []
        self.data = data
        self._parse(data)
        self.environment = Environment(
                loader=FileSystemLoader(self.templates),
                autoescape=select_autoescape(["html", "xml"])
        )

    def __repr__(self):
        return "SiteConfig(%r, %r)" % (self.root, self.data)

    def process_wildcards(self, entities):
        processed_entities = []
        for entity in entities:
            if "*" in entity.get("source", "") and "*" in entity.get("target", ""):
                source = entity.get("source", "")
                for list_source in glob.glob(os.path.abspath(os.path.join(self.root, entity.get("source")))):
                    ext = source.split("*")[-1]
                    filename = list_source.split("/")[-1].replace(ext, "")
                    replace_target = entity.get("target", "").replace("*", filename)
                    replace_source = entity.get("source", "").replace("*", filename)

                    entity_copy = entity.copy()
                    entity_copy["source"] = replace_source
                    entity_copy["target"] = replace_target

                    processed_entities.append(entity_copy)
            else:
                processed_entities.append(entity)

        return processed_entities

    def _parse(self, data):
        """Load pages to be generated"""
        try:
            processed_pages = self.process_wildcards(data["pages"])
            self.pages = [Page(self.markdown_renderer, self.root, **page) for page in processed_pages]
            self.templates = [os.path.join(self.root, template) for template in data["templates"]]
            self.resources = [PlainResource(self.root, **resource) for resource in data["resources"]]
        except KeyError as ke:
            if ke is 'templates':
                print("No templates found for %s" % (data["site"]))

    def render(self):
        """Render Markdown to HTML and extract YAML metadata"""
        for page in self.pages:
            page.render(self.environment)

        for resource in self.resources:
            resource.render(self.environment)



