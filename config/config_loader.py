import json
import errno
import os
from config.site import Site


class ConfigLoader(object):
    site_config_file = "site.json"

    def __init__(self):
        pass

    def load(self, path):
        configs = []
        try:
            json_data = json.loads(
                open(os.path.join(path, self.site_config_file), "r").read())
        except FileNotFoundError as fnf:
            if fnf.errno != errno.ENOENT:
                raise
            else:
                print("Error: No path to site config")
                return 1

        try:
            for site_data in json_data["sites"]:
                configs.append(Site(path, site_data))
        except KeyError:
            pass

        return configs
