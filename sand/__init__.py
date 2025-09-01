import json
import os
import click

from sand.config import ConfigLoader

def main_processor(sites, serve=False, compress=True, port=9000):
    perform_render(sites, compress)

    if serve:
        serve_render(sites, port)

@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('project_location')
@click.option("--page", nargs=1, default=None, help="Generate a new page in the provided site")
@click.option("--site", nargs=1, default=None, help="Generate a new basic site")
@click.option("--config-override", "-c", type=str, multiple=True)
@click.option("--uncompressed", is_flag=True, help="Do not compress the output HTML")
@click.option("--serve", is_flag=True, help="Run a server serving the generated site")
@click.option("--port", "-p", type=int, default=9000, multiple=False, help="Starting port for the test server")
def main(project_location, *args, **kwargs):
    config_overrides = {}
    if kwargs['config_override']:
        config_overrides = dict(arg.split("=") for arg in kwargs['config_override'])

    page = kwargs['page']
    site = kwargs['site']

    if page is None and site is None:
        if os.path.exists(project_location):
            sites = ConfigLoader().load(click.format_filename(project_location), config_overrides)
            main_processor(sites, kwargs['serve'], not kwargs['uncompressed'], kwargs['port'])
    elif page is not None:
        create_new_page(page)
    elif site is not None:
        create_new_site(site, project_location)


def perform_render(sites, compress):
    # Render
    for i, site in enumerate(sites):
        print("Rendering - %s to %s" % (site.root, site.output_root))
        site.render(compress)


def serve_render(sites, port=9000):
    from .server.test_server import Servers
    servers = Servers(port=port)
    servers.for_sites(sites)


def create_new_page(page):
    from .builder import components as builder_components
    # Generate a new page
    if not os.path.exists(page):
        dirs = os.path.split(page)[0]
        if dirs:
            os.makedirs(dirs, exist_ok=True)
        with open(page, "w") as out:
            out.write(builder_components.PAGE_TEMPLATE)
        click.echo("New page %s created" % page)
    else:
        click.echo("The path provided for the new page already exists and cannot be created.")


def create_new_site(site, project_location):
    from .builder import components as builder_components
    site_obj = builder_components.site_conf_basic(project_location)
    os.makedirs(site, exist_ok=True)

    if not os.path.exists(os.path.join(project_location, "site.conf")):
        with open(os.path.join(project_location, "site.conf"), "w") as json_file:
            json.dump(site_obj, json_file)

        os.makedirs(os.path.join(project_location, "resources/css"))
        os.makedirs(os.path.join(project_location, "resources/scripts"))
        os.makedirs(os.path.join(project_location, "resources/img"))
        os.makedirs(os.path.join(project_location, "templates"))
        os.makedirs(os.path.join(project_location, "pages"))

        with open(os.path.join(project_location, "templates/base.html"), "w") as template_file:
            template_file.write(builder_components.TEMPLATE_HTML)

        with open(os.path.join(project_location, "pages/index.md"), "w") as template_file:
            template_file.write(builder_components.INDEX_MD)

        with open(os.path.join(project_location, "resources/css/reset.less"), "w") as less_file:
            less_file.write(builder_components.RESET_LESS)

        with open(os.path.join(project_location, "resources/css/style.less"), "w") as less_file:
            less_file.write(builder_components.STYLE_LESS)

    else:
        click.echo("A site.json file already exists in this folder")