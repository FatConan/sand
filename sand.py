from config.config_loader import ConfigLoader
import os
import click

PAGE_TEMPLATE = """title: [Add a page title]
template: [The template used to render]

# Page Header

This new markdown page will need to either be added to your site.json for rendering or may be picked up automatically if 
contained in a folder using wildcard rules to render.

"""



@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('site_json', type=click.Path(exists=True))
@click.option("--page", nargs=1, default=None, help="Generate a new page in the provided site")
def main(site_json, page=None):
    sites = ConfigLoader().load(click.format_filename(site_json))

    if page is None:
        #Render
        for site in sites:
            site.render()
    else:
        #Generate a new page
        if not os.path.exists(page):
            os.makedirs(os.path.split(page)[0], exist_ok=True)
            with open(page, "w") as out:
                out.write(PAGE_TEMPLATE)
            click.echo("New page %s created" % page)
        else:
            click.echo("The path provided for the new page already exists and cannot be created.")


if __name__ == "__main__":
    main()
