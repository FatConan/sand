from sand.config import Site, ConfigLoader

def test_empty_site_relative_path():
    site = Site("./root", {})
    assert site.root == "./root/."

def test_basic_site_definition():
    path = "."
    site_data =  {
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
    pass