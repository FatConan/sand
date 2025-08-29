import importlib
import os
import shutil
import sys
import uuid
import warnings
import htmlmin
import markdown
from jinja2 import environment

from sand.config.default.site_data_processor import Plugin as DefaultPlugin
from sand.entities.pages.__init__ import *
from sand.entities.resources.__init__ import *
from sand.entities.__init__ import RenderEntity as DefaultRenderEntity
from sand.helpers.progress import Progress

#Define some string constants
RESOURCES = "resources"
PAGES = "pages"
PLUGINS = "plugins"
PLUGINS_MODULE = "sandplugins"

class Site(object):
    def __init__(self, root, site_data):
        print("Initialising Site", root)

        # Create a dictionary of available render entity types, we can then expand this in plugins if we like
        self._render_entities = {
            RESOURCES: {
                "less": LessResource,
                "scss": ScssResource,
                None: PlainResource,
            },
            PAGES: {
                "raw": RawContent,
                None: Page
            }
        }

        #Create an extensible list of plugins
        self._plugins = [DefaultPlugin(), ]

        external_plugins = site_data.get(PLUGINS, list())

        if external_plugins:
            # create a list of plugins
            for plugin in external_plugins:
                plugin_instance = self.load_plugin(root, plugin)
                if plugin_instance is not None:
                    self._plugins.append(plugin_instance)

        self.environment = environment
        self.renderer = markdown.Markdown(
            extensions=['extra', 'meta', 'toc', 'tables', 'abbr']
        )
        self.minifier = htmlmin.Minifier(remove_optional_attribute_quotes=False, reduce_boolean_attributes=False)

        self.pages = []
        self.page_reference = {}
        self.templates = []
        self.resources = []
        self.overrides = {}

        self.root = os.path.join(root, site_data.get("root"))

        output_relative = site_data.get("output_root", "output")
        if output_relative:
            self.output_root = os.path.join(self.root, output_relative)
        else:
            self.output_root = os.path.join(self.root, "output")

        base_url = site_data.get("domain", "")
        if base_url and not base_url.endswith("/"):
            base_url = base_url + "/"
        self.base_url = base_url

        self.uuid = uuid.uuid4()
        self.site_data = site_data

        # Process all the plugins
        for plugin in self._plugins:
            plugin.configure(site_data, self)

        self._parse(site_data)

    def minify(self, raw_html):
        return self.minifier.minify(raw_html)

    def register_renderer(self, entity_domain, entity_type, renderer_class):
        domain = self._render_entities.get(entity_domain, {})
        if entity_type in domain:
            warnings.warn("WARNING: Replacing existing renderer for %s" % entity_type)
        domain[entity_type] = renderer_class
        self._render_entities[entity_domain] = domain

    def register_resource_renderer(self, entity_type, renderer_class):
        self.register_renderer(RESOURCES, entity_type, renderer_class)

    def register_page_renderer(self, entity_type, renderer_class):
        self.register_renderer(PAGES, entity_type, renderer_class)

    def render_entity_selection(self, entity_domain, entity_dict):
        domain  = self._render_entities.get(entity_domain, {})
        requested_type = entity_dict.get("type", None)
        #Look up the render entity class, or grab the default No-oip if that fails
        renderer = domain.get(requested_type, DefaultRenderEntity)
        return renderer(self, **entity_dict)

    def add_resource(self, resource_dict):
        #Grab the correct resource type and add it to the list
        resource = self.render_entity_selection(RESOURCES, resource_dict)
        self.resources.append(resource)

    def add_page(self, page_dict):
        #Grab the correct page type and add it to the list
        page = self.render_entity_selection(PAGES, page_dict)
        self.pages.append(page)

        #Also add the page to a reference dict that indexes them by path
        try:
            path, file = page.target_url_parts
            try:
                self.page_reference[path].append((file, page))
            except KeyError:
                self.page_reference[path] = [(file, page), ]
        except AttributeError:
            pass

        return page

    def plugins(self):
        return self._plugins

    def load_plugin(self, root, module):
        # Plugins may be loaded from the project or from the builtins. Check the externals first then
        # try the builtins folder

        try:
            root_path = os.path.abspath(root)
            sys.path.append(root_path)
            instance = importlib.import_module("%s.%s" % (PLUGINS_MODULE, module), package=PLUGINS_MODULE).Plugin()
            print("External plugin '%s' loaded" % module)
            return instance
        except ImportError:
            # Try the builtins
            try:
                instance = importlib.import_module("sand.plugin.builtins.%s" % module).Plugin()
                print("Built-in plugin '%s' loaded" % module)
                return instance
            except ImportError:
                warnings.warn("Unable to load plugin '%s'" % module)
        return None

    def __repr__(self):
        return "SiteConfig(%r, %r, %r)" % (self.root, self.output_root, self.site_data)

    def _parse(self, data):
        """Load pages to be generated"""
        for plugin in self._plugins:
            plugin.parse(data, self)

    def render(self, compress=True):
        shutil.rmtree(os.path.abspath(self.output_root), ignore_errors=True)
        progress = Progress()

        for page in self.pages:
            progress.spinner("PAGES %s")
            page.render(self.environment, compress=compress)

        for resource in self.resources:
            progress.spinner("RESOURCES %s")
            resource.render(self.environment)
