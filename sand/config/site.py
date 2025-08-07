import importlib
import os
import shutil
import sys
import uuid

import htmlmin
import markdown
from jinja2 import environment

from sand.config.default.site_data_processor import Plugin as DefaultPlugin
from sand.entities.page import Page
from sand.helpers.progress import Progress


class Site(object):
    def __init__(self, root, site_data):
        print("Initialising Site", root)
        self._plugins = [DefaultPlugin(), ]

        external_plugins = site_data.get("plugins", list())

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

        self.base_url = site_data.get("domain", "")

        self.uuid = uuid.uuid4()
        self.site_data = site_data

        # Process all the plugins
        for plugin in self._plugins:
            plugin.configure(site_data, self)

        self._parse(site_data)

    def minify(self, raw_html):
        return self.minifier.minify(raw_html)

    def add_page(self, page_dict):
        page = Page(self, **page_dict)
        self.pages.append(page)

        path, file = page.target_url_parts
        try:
            self.page_reference[path].append((file, page))
        except KeyError:
            self.page_reference[path] = [(file, page), ]

        return page

    def plugins(self):
        return self._plugins

    def load_plugin(self, root, module):
        # Plugins may be loaded from the project or from the builtins. Check the externals first then
        # try the builtins folder
        PLUGINS_MODULE = "sandplugins"
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
                print("Unable to load plugin '%s'" % module)
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
            page.render(self.environment, compress)

        for resource in self.resources:
            progress.spinner("RESOURCES %s")
            resource.render(self.environment)
