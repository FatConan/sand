import json
import errno
import os
import sys
from config.site import Site
from pyhocon import ConfigFactory


class ConfigLoader(object):
    site_config_files = ["site.json", "site.hocon", "site.conf"]

    def __init__(self):
        pass

    def load(self, path, config_overrides=None):
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
                site_data["plugins"] = site_data.get("plugins", [])
                os.path.join(path, site_data.get("root"))
                configs.append(Site(path, site_data))
        except KeyError:
            pass

        return configs
