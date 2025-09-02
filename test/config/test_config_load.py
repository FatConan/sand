import pytest
from sand.config import Site, ConfigLoader


def test_empty_site_relative_path():
    site = Site("./root", {})
    assert site.root == "./root/."


def test_basic_site_definition():
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
    assert site.root == "./."


def test_basic_multiple_site_config():
    path = "."
    sites_data = {"sites": [
        {
            "root": "./site_one",
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
        },
        {
            "root": "./site_two",
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
        },
        {
            "root": "./site_three",
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
    ]}

    sites = ConfigLoader().from_dict(path, sites_data)
    #Make sure we loaded the entries
    assert len(sites) == 3
    assert sites[0].root == "././site_one"
    assert sites[1].root == "././site_two"
    assert sites[2].root == "././site_three"

def test_named_multiple_site_config():
    """
    With Hocon configuration namespacing would actually be a nice way of separating sites rather than
    just putting them in a list. Added this to the config loader mechanism and write a test for it
    """
    path = "."
    sites_data = {"site_one": {
            "root": "./site_one",
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
        },
        "site_two": {
            "root": "./site_two",
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
        },
        "site_three": {
            "root": "./site_three",
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
    }
    sites = ConfigLoader().from_dict(path, sites_data)
    # Make sure we loaded the entries
    assert len(sites) == 3
    assert sites[0].root == "././site_one"
    assert sites[1].root == "././site_two"
    assert sites[2].root == "././site_three"

def test_incorrect_configuration():
    path = "."
    sites_data = {"incorrect": [
        {
            "root": "./site_one",
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
        },
        {
            "root": "./site_two",
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
        },
        {
            "root": "./site_three",
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
    ]}

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ConfigLoader().from_dict(path, sites_data)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

