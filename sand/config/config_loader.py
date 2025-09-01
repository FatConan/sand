import os
from sand.config.site import Site
from pyhocon import ConfigFactory


class ConfigLoader(object):
    site_config_files = ["site.json", "site.conf"]

    def __init__(self):
        pass

    def from_individual_dict(self, path, conf=None, config_overrides=None):
        """
        Create a site instance from the configuration information in the site.conf/site.json file.

        :param path: The project path
        :param conf: The specific site configuration data
        :param config_overrides: Any config overrides passed in from the command line
        :return: A site instance
        """
        if conf is None:
            conf = {}

        conf["overrides"] = config_overrides
        conf["plugins"] = conf.get("plugins", [])
        os.path.join(path, conf.get("root"))
        # Initialise Site
        return Site(path, conf)

    def from_dict(self, path, conf=None, config_overrides=None):
        configs = []
        if conf is None:
            conf = {}

        #Load all sites from configuration file
        if not conf:
            print("Error: No config entries found")
            exit(1)

        #We need to have a properly formatted list of sites so make sure that's a thing
        try:
            for site_data in conf["sites"]:
                #And if it is, then instantiate the appropriate site from the site_data
                configs.append(
                    self.from_individual_dict(path, site_data, config_overrides)
                )
        except KeyError:
            print("Error: No site entries found configuration")
            exit(1)

        return configs

    def load(self, path, config_overrides=None):
        """
        Hunt for one of the permitted configurations files (site.conf, site.json) and then attempt
        to load and parse it to create the appropriate Site instances.

        :param path: The project path
        :param config_overrides: values to override in configuration file that can be specified on the command line
        :return: A list of site instances
        """

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

        return self.from_dict(path, conf, config_overrides)
