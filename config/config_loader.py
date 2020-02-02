import json
import errno
import os
from config.site import Site
import sys
from pyhocon import ConfigFactory


class ConfigLoader(object):
    site_config_files = ["site.json", "site.hocon", "site.conf"]

    def __init__(self):
        self.site_clazz = Site

    def load(self, path, config_overrides=None):
        extensions_module = os.path.join(path, "sand/")
        if os.path.exists(extensions_module):
            sys.path.append(os.path.abspath(extensions_module))
            try:
                from extensions import SiteExt
            except ImportError:
                pass
            else:
                class Extended(Site, SiteExt):
                    pass

                self.site_clazz = Extended

        configs = []
        found_config = False
        conf = {}

        for f in self.site_config_files:
            test_path = os.path.join(path, f)
            if os.path.exists(test_path):
                conf = ConfigFactory.parse_file(test_path)
                found_config = True
                break

        if not found_config:
            print("Error: No path to site config")
            exit(1)

        if not conf:
            print("Error: No config entries found")
            exit(1)

        try:
            for site_data in conf["sites"]:
                site_data["overrides"] = config_overrides
                os.path.join(path, site_data.get("root"))
                configs.append(self.site_clazz(path, site_data))
        except KeyError:
            pass

        return configs
