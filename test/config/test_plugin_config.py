import pytest

from sand.config import Site, ConfigLoader, SiteDataProcessorPlugin
from sand.plugin.builtins.es6css import Plugin as Es6Plugin

def test_default_plugins():
    path = "."
    site_data = {
        "root": ".",
        "pages": [
            {
                "config": {
                    "static_content": "This is static content",
                    "template": "default.html",
                },
                "source": None,
                "target": "./index.html"
            },
        ],
        "templates": [
            "templates"
        ]
    }

    site = ConfigLoader().from_individual_dict(path, site_data)
    assert len(site._plugins) == 1
    assert isinstance(site._plugins[0], SiteDataProcessorPlugin)

def test_es6css_plugin():
    path = "."
    site_data = {
        "root": ".",
        "plugins": ["es6css"],
        "pages": [
            {
                "config": {
                    "static_content": "This is static content",
                    "template": "default.html",
                },
                "source": None,
                "target": "./index.html"
            },
        ],
        "templates": [
            "templates"
        ]
    }

    site = ConfigLoader().from_individual_dict(path, site_data)
    assert len(site._plugins) == 2
    assert isinstance(site._plugins[0], SiteDataProcessorPlugin)
    assert isinstance(site._plugins[1], Es6Plugin)