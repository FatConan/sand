from config.config_loader import ConfigLoader
import os
import click
import json

PAGE_TEMPLATE = """title: [Add a page title]
template: [The template used to render]

# Page Header

This new markdown page will need to either be added to your site.json for rendering or may be picked up automatically if 
contained in a folder using wildcard rules to render.

"""

SITE_JSON_BASIC = """{"sites": [
    {
        "root": "%s",
        "output_root": "output",
        "pages": [
            {
                "source": "./pages/*.md",
                "target": "*.html"
            }
        ],
        "templates": [
            "templates"
        ],
        "resources": [
            {
                "source": "./resources",
                "target": "./resources"
            }
        ]
    }
]}"""

TEMPLATE_HTML = """<!DOCTYPE html>
<html>
    <head>
        <title>{{ DATA.get("title") }}</title>
        <link rel="stylesheet" type="text/css" href="/resources/css/style.css" />
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js"></script>
    </head>
    <body>
        {{ content|safe }}
    </body>
</html>
"""

INDEX_MD = """title: Welcome to Sand
template: base.html

# Welcome to your new site

This is a new sand site.

"""


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('project_location')
@click.option("--page", nargs=1, default=None, help="Generate a new page in the provided site")
@click.option("--site", nargs=1, default=None, help="Generate a new basic site")
@click.option("--config-override", "-c", type=str, multiple=True)
def main(project_location, page=None, site=None, config_override=()):
    config_overrides = {}
    if config_override:
        config_overrides = dict(arg.split("=") for arg in config_override)
        print(config_overrides)

    if page is None and site is None:
        if os.path.exists(project_location):
            sites = ConfigLoader().load(click.format_filename(project_location), config_overrides)
            perform_render(sites)
    elif page is not None:
        create_new_page(page)
    elif site is not None:
        create_new_site(site, project_location)




def perform_render(sites):
    # Render
    for site in sites:
        print("Rendering - %s to %s" % (site.root, site.output_root))
        site.render()


def create_new_page(page):
    # Generate a new page
    if not os.path.exists(page):
        os.makedirs(os.path.split(page)[0], exist_ok=True)
        with open(page, "w") as out:
            out.write(PAGE_TEMPLATE)
        click.echo("New page %s created" % page)
    else:
        click.echo("The path provided for the new page already exists and cannot be created.")


def create_new_site(site, project_location):
    site_json_string = SITE_JSON_BASIC % site
    os.makedirs(site, exist_ok=True)

    if not os.path.exists(os.path.join(project_location, "site.json")):
        with open(os.path.join(project_location, "site.json"), "w") as json_file:
            json.dump(json.loads(site_json_string), json_file)

        os.makedirs(os.path.join(project_location, "resources/css"))
        os.makedirs(os.path.join(project_location, "resources/scripts"))
        os.makedirs(os.path.join(project_location, "resources/img"))
        os.makedirs(os.path.join(project_location, "templates"))
        os.makedirs(os.path.join(project_location, "pages"))

        with open(os.path.join(project_location, "templates/base.html"), "w") as template_file:
            template_file.write(TEMPLATE_HTML)

        with open(os.path.join(project_location, "pages/index.md"), "w") as template_file:
            template_file.write(INDEX_MD)

    else:
        click.echo("A site.json file already exists in this folder")


if __name__ == "__main__":
    main()
