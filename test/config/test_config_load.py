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