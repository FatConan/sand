from entities.page import Page
from config.default.site_data_processor import Plugin as DefaultPlugin
from jinja2 import Environment, FileSystemLoader, select_autoescape
import importlib
import importlib.util as ilu
import markdown
import os, sys
import glob
import shutil
import re
import uuid

from entities.resources.resource_selector import ResourceSelector

class Site(object):
    def __init__(self, root, site_data):
        print("Initialising Site", root)
        self._plugins = [DefaultPlugin(),]

        external_plugins = site_data.get("plugins", list())
        print("PLUGIN_LIST", ",".join([p for p in external_plugins]))

        if external_plugins != []:
            # create a list of plugins
            for plugin in external_plugins:
                #spec = ilu.spec_from_file_location("Plugin", os.path.abspath(plugin))
                #print("SPEC", spec)

                #plugin_lib = ilu.module_from_spec(spec)
                #print("PLUGIN_LIB", plugin_lib)
                #print(self._load_plugin(plugin))
                # self._plugins.append(spec.loader.exec_module(plugin_lib).Plugin())
                self._plugins.append(self.load_plugin(root, plugin))
                pass

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

        #Process all the plugins
        for plugin in self._plugins:
            print(plugin)
            plugin.configure(site_data, self)

        self._parse(site_data)

    def load_plugin(self, root, module):
        root_path = os.path.abspath(root)
        package = "%s.sand" % os.path.split(root_path)[-1]
        module_path = os.path.abspath(os.path.join(root, "sand"))
        sys.path.append(module_path)
        return importlib.import_module(module, package=package).Plugin()




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



