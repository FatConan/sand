import importlib
import os
import shutil
import sys
import uuid

import markdown

from config.default.site_data_processor import Plugin as DefaultPlugin
from entities.page import Page
from jinja2 import environment


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

        self.uuid = uuid.uuid4()
        self.site_data = site_data

        # Process all the plugins
        for plugin in self._plugins:
            plugin.configure(site_data, self)

        self._parse(site_data)

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
        try:
            root_path = os.path.abspath(root)
            package = "%s.sand" % os.path.split(root_path)[-1]
            module_path = os.path.abspath(os.path.join(root, "sand"))
            sys.path.append(module_path)
            instance = importlib.import_module(module, package=package).Plugin()
            print("External plugin '%s' loaded" % module)
            return instance
        except ImportError:
            # Try the builtins
            try:
                instance = importlib.import_module("plugin.builtins.%s" % module).Plugin()
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

    def render(self):
        shutil.rmtree(os.path.abspath(self.output_root), ignore_errors=True)

        for page in self.pages:
            page.render(self.environment)

        for resource in self.resources:
            resource.render(self.environment)
