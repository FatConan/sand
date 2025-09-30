import os
import warnings
from sand.config.site import Site
from pyhocon import ConfigFactory


class ConfigLoader:
    site_config_files = ["site.json", "site.conf"]

    def __init__(self):
        pass

    def is_valid_dict(self, conf):
        """
        Check that the configuration looks to provide the basics of a site definition

        :param conf: The candidate configuration
        :return: A boolean indicating validity
        """
        if not isinstance(conf, dict):
            return False

        if not "root" in conf:
            return False

        return True

    def from_individual_dict(self, path, conf=None, config_overrides=None, name=None):
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
        return Site(path, conf, name)

    def parse_sites_array(self, configs, path, conf=None, config_overrides=None):
        """
        There are now two ways to represent sites, this method involves adding an array names "sites" to the config
        with the configuration for each site as elements withing it. This method parses that array and adds each site
        as an automatically named site to our configuration list.

        :param configs: The list of the current site configurations
        :param path: The path to the project
        :param conf: The configuration object being interpreted
        :param config_overrides: And command line specified configuration overrides
        :return:
        """
        for i, site_data in enumerate(conf["sites"]):
            # Check for a valid configuration then instantiate the appropriate site from the site_data
            # with a generated name of "Unnamed-{index}"
            if self.is_valid_dict(site_data):
                configs.append(
                    self.from_individual_dict(path, site_data, config_overrides, name="Unnamed-%d" % i)
                )
            else:
                warnings.warn("Invalid definition found for site %d" % i)

    def parse_named_sites(self, configs, path, conf=None, config_overrides=None):
        """ There are now two ways to represent sites, this method involves adding each site under a naming key to the
        config. This method parses that dictionary of keys and site configs and adds each site
        as an entry to the configs with the corresponding key as the site's name.

        :param configs: The list of the current site configurations
        :param path: The path to the project
        :param conf: The configuration object being interpreted
        :param config_overrides: And command line specified configuration overrides
        :return:
        """
        # Look at the root of the config for named sites this time and iterate over them
        for name, site_data in conf.items():
            #If they appear valid add them the configs list
            if self.is_valid_dict(site_data):
                configs.append(
                    self.from_individual_dict(path, site_data, config_overrides, name=name)
                )
            else:
                warnings.warn("Invalid definition found for site \"%s\"" % name)


    def from_dict(self, path, conf=None, config_overrides=None):
        configs = []
        if conf is None:
            conf = {}

        #Load all sites from configuration file
        if not conf:
            print("Error: No config entries found")
            exit(1)

        #We need to have a properly formatted list of sites so make sure that's a thing
        if "sites" in conf:
            self.parse_sites_array(configs, path, conf, config_overrides)
        else:
            self.parse_named_sites(configs, path, conf, config_overrides)

        if not configs:
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
