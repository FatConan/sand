from loguru import logger
import os
from sand.config.site import Site
from pyhocon import ConfigFactory
from typing import AnyStr, List, Dict


class ConfigLoader:
    site_config_files = ["site.json", "site.conf"]

    def __init__(self):
        pass

    @staticmethod
    def is_valid_dict(conf:dict) -> bool:
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

    @staticmethod
    def from_individual_dict(path:AnyStr, conf:Dict=None, config_overrides:Dict=None, name:AnyStr=None) -> Site:
        """
        Create a site instance from the configuration information in the site.conf/site.json file.

        :param path: The project path
        :param conf: The specific site configuration data
        :param config_overrides: Any config overrides passed in from the command line
        :return: A site instance
        """
        if conf is None:
            conf = {}

        logger.debug(f"Parsing configuration for {name}")

        conf["overrides"] = config_overrides
        conf["plugins"] = conf.get("plugins", [])
        os.path.join(path, conf.get("root", ""))
        # Initialise Site
        site = Site(path, conf, name)

        logger.debug("Site initialised")
        return site

    @staticmethod
    def parse_sites_array(configs:List[Site], path:AnyStr, conf:Dict=None, config_overrides:Dict=None) -> None:
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
            if ConfigLoader.is_valid_dict(site_data):
                configs.append(
                    ConfigLoader.from_individual_dict(path, site_data, config_overrides, name="Unnamed-%d" % i)
                )
            else:
                logger.warning("Invalid definition found for site %d" % i)

    @staticmethod
    def parse_named_sites(configs:List[Site], path:AnyStr, conf:Dict=None, config_overrides:Dict=None) -> None:
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
        if conf is not None:
            for name, site_data in conf.items():
                #If they appear valid add them the configs list
                if ConfigLoader.is_valid_dict(site_data):
                    configs.append(
                        ConfigLoader.from_individual_dict(path, site_data, config_overrides, name=name)
                    )
                else:
                    logger.warning(f'Invalid definition found for site "{name}"')
        else:
            logger.error("No configuration provided")

    @staticmethod
    def from_dict(path:AnyStr, conf:Dict=None, config_overrides:Dict=None) -> List[Site]:
        """
        Instantiate a list of Sites from a provided conf dictionary (and command line overrides if required)
        and return that list of Sites

        :param path: path to the configuration file
        :param conf: dictionary from the parsed configuration
        :param config_overrides: overrides to the defined configuration passed on the CLI
        :return: the list of configured Sites
        """
        configs = []

        #Load all sites from configuration file
        if not conf:
            logger.error("Error: No config entries found")
            exit(1)

        #We need to have a properly formatted list of sites so make sure that's a thing
        if "sites" in conf:
            ConfigLoader.parse_sites_array(configs, path, conf, config_overrides)
        else:
            ConfigLoader.parse_named_sites(configs, path, conf, config_overrides)

        if not configs:
            logger.error("Error: No site entries found configuration")
            exit(1)

        return configs

    @staticmethod
    def load(path:AnyStr, config_overrides:Dict=None) -> List[Site]:
        """
        Hunt for one of the permitted configurations files (site.conf, site.json) and then attempt
        to load and parse it to create the appropriate Site instances.

        :param path: The project path
        :param config_overrides: values to override in configuration file that can be specified on the command line
        :return: A list of site instances
        """

        found_config = False
        conf = {}

        for f in ConfigLoader.site_config_files:
            test_path = os.path.join(path, f)
            if os.path.exists(test_path):
                conf = ConfigFactory.parse_file(test_path)
                found_config = True
                break

        if not found_config:
            logger.error("Error: No path to site config")
            exit(1)

        return ConfigLoader.from_dict(path, conf, config_overrides)
