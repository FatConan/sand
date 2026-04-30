from loguru import logger
import importlib
import os
import shutil
import sys
import uuid
import htmlmin
import markdown
import datetime

from typing import Union, List, Dict, AnyStr

from jinja2 import Environment

from sand.config.helpers import CONFIG_NULL, ConfigNull
from sand.config.default.site_data_processor import SiteDataProcessorPlugin as DefaultPlugin
from sand.entities.pages.__init__ import *
from sand.entities.resources.__init__ import *
from sand.entities.__init__ import RenderEntity as DefaultRenderEntity
from sand.plugin import SandPlugin

#Define some string constants
RESOURCES = "resources"
PAGES = "pages"
PLUGINS = "plugins"
PLUGINS_MODULE = "sandplugins"

#Define the renderers for the default entitie of various types
DEFAULT_RENDER_ENTITIES =  {
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

class Site:
    # The site environment is jinja2 Environment configured on a per site basis and instantiated from within
    # the SiteDataProcessorPlugin (in the parse method)
    _environment = None
    _render_entities = {}
    _templates:List[str] = []
    _overrides = {}

    resources = []
    pages = []
    page_reference = {}

    def __init__(self, root:AnyStr, site_data:Dict, name:AnyStr=None):
        logger.info(f"Initialising Site: {name}")

        self.name = name

        # Create a dictionary of available render entity types, we can then expand this in plugins if we like
        self._render_entities.update(DEFAULT_RENDER_ENTITIES)

        #Create an extensible list of plugins
        self._plugins:List[SandPlugin] = [ ]

        external_plugins = site_data.get(PLUGINS, list())

        if external_plugins:
            # create a list of plugins
            for plugin in external_plugins:
                plugin_instance = self.load_plugin(root, plugin)
                if plugin_instance is not None:
                    self._plugins.append(plugin_instance)

        self._plugins.append(DefaultPlugin())

        self.renderer = markdown.Markdown(
            extensions=['extra', 'meta', 'toc', 'tables', 'abbr']
        )
        self.minifier = htmlmin.Minifier(remove_optional_attribute_quotes=False, reduce_boolean_attributes=False)

        self.root = os.path.join(root, site_data.get("root", "."))

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

    def environment(self, environment:Union[Environment, ConfigNull]=CONFIG_NULL):
        """get or set the jinja2 environment used to render the templates and content of the site"""
        if not isinstance(environment, ConfigNull):
            self._environment = environment
        return self._environment

    def templates(self, templates:Union[List[AnyStr], ConfigNull]=CONFIG_NULL):
        """Set the location list of templates to be available to the jinja renderer"""
        if not isinstance(templates, ConfigNull):
            self.add_templates(templates)
        return self._templates

    def add_templates(self, templates:List[AnyStr]):
        """Add templates to the templates list, the plugins can use this to add their own templates"""
        logger.debug(f"Adding template folders {templates}")
        self._templates.extend(templates)

    def overrides(self, overrides:Union[Dict, ConfigNull]=CONFIG_NULL):
        """Set the overrides for the Site configuration"""
        if not isinstance(overrides, ConfigNull):
            self._overrides = overrides
        return self._overrides

    def stat(self, path:AnyStr):
        return os.stat(os.path.join(self.root, path))

    def created(self, path:AnyStr):
        return datetime.datetime.fromtimestamp(self.stat(path).st_ctime)

    def minify(self, raw_html:AnyStr):
        return self.minifier.minify(raw_html)

    def register_renderer(self, entity_domain:AnyStr, entity_type:AnyStr, renderer_class:type):
        domain = self._render_entities.get(entity_domain, {})
        if entity_type in domain:
            logger.warning(f"WARNING: Replacing existing renderer for {entity_type}")
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

    def add_resource(self, resource_dict:Dict):
        #Grab the correct resource type and add it to the list
        resource = self.render_entity_selection(RESOURCES, resource_dict)
        self.resources.append(resource)

    def add_page(self, page_dict:Dict):
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

    @staticmethod
    def load_plugin(root:AnyStr, module:AnyStr) -> Union[SandPlugin, None]:
        # Plugins may be loaded from the project or from the builtins. Check the externals first then
        # try the builtins folder

        try:
            root_path = os.path.abspath(root)
            sys.path.append(root_path)
            instance = importlib.import_module("%s.%s" % (PLUGINS_MODULE, module), package=PLUGINS_MODULE).Plugin()
            logger.info("External plugin '%s' loaded" % module)
            return instance
        except ImportError:
            # Try the builtins
            try:
                instance = importlib.import_module("sand.plugin.builtins.%s" % module).Plugin()
                logger.info("Built-in plugin '%s' loaded" % module)
                return instance
            except ImportError:
                logger.warning("Unable to load plugin '%s'" % module)
        return None

    def __repr__(self):
        return f"Site[{self.name}]({self.root}, {self.output_root})"

    def _parse(self, data:Dict):
        """Load pages to be generated"""
        for plugin in self._plugins:
            plugin.parse(data, self)

    def render(self, compress:bool=True):
        """
        Render the site's pages and resources

        :param compress: Should we compress the output (stripping wasted whitespace etc.)
        :return:
        """

        shutil.rmtree(os.path.abspath(self.output_root), ignore_errors=True)
        for page in self.pages:
            if page.validate():
                page.render(self.environment(), compress=compress)
            else:
                logger.warning("Page %s did not pass validation and won't be rendered", page)

        for resource in self.resources:
            if resource.validate():
                resource.render(self.environment())
            else:
                logger.warning("Resource %s did not pass validation and won't be rendered", resource)

