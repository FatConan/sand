# Sand: A simple static site generator

**Sand** is a static site generator based heavily on an early version of [Stone](https://github.com/neuralsandwich/stone) by
[NeuralSandwich](https://github.com/neuralsandwich). While **Stone** is becoming a more fully featured blog engine, **Sand**
pairs back functionality to the basics, and is designed to provide similar functionality to the early versions of Stone, but 
with added wildcard support, support for resources, and some other functions that proved useful when building projects.

## Built on Sand
This **README** serves as both documentation for this tool as well as an example project.  While this file contains the content, 
there are a number of pieces of additional metadata required to configure the **Sand** project, which are provided by the accompanying `site.conf` HOCON file.

### Installing with Pip

To install `sand` as a module run `pip install .` from within the cloned folder.
Once installed `sand` can be used by running:

```
sand
```

### Generating the documentation

To see **Sand** generate this documentation, clone this repository and run:

```
python3 sand example --serve
```

Or

```
sand example --serve
```

from within the checked out folder. This will build this documentation and start a development server at [http://localhost:9000](http://localhost:9000) serving it. Omitting the `--serve` argument will build this documentation without starting a server. 

```
sand example
```

## A Note on Security

The [plugin](#plugin) aspects of **Sand** are designed to make it flexible enough to accommodate a range of different project types 
(**Sand** has been used to generate a number of things from blogs, to portfolios, to documentation sites like this one), however, this also provides an avenue for potentially malicious code to be executed by **Sand**. 

For example, if you run **Sand** periodically on an accessible server and an attacker were able to compromise a `sand/plugin.py` file to modify any of the expected plugin methods (`configure`, `parse`, `add_render_context`) to do something malicious then **Sand** would execute them.

This hasn't been a major concern in its design as **Sand** is meant to generate static sites and so it's presumed that whatever safe environment
**Sand** was executed within would be separate to the potentially exposed environment in which its output would be deployed.

Still it's worth noting this potential vector as this plugins folder would be something that would be expected to exist outside the core **Sand** code where it might be inadvertently unprotected.
  

## Configuration 

A configuration file is required to inform **Sand** what to build and how to build it. It takes the form of a HOCON file typically named `site.conf` to detail where source and output files can be found, what plugins are required and a collection of other data required when creating the HTML output. Per-page configuration may be specified using a YAML header in the markdown, or by specifying a per-page `config` entry within the `site.conf` file.

In this overview of how the configuration works we'll walk through the `site.conf` file in the `example` folder that describes how this documentation is built. 

**NB:** In previous versions of **Sand** the configuration had been read only as JSON, but now is read as HOCON using [pyhocon](https://github.com/chimpler/pyhocon/). This preserves backwards compatibility, but also allows for the configuration bells and whistles that [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) supports. To make this a little less jarring **Sand** will now also attempt to read configuration data from `site.hocon` and `site.conf` in addition to `site.json` to ease any nomenclature-based anxiety.

When the above `python3 sand.py example` command is run the `site.conf` in the `example` folder informs **Sand** how to build the HTML output, and **Sand** follows these instructions to create a styled, HTML version of this README markdown (additionally it creates a configuration cheat sheet from the `supplementary-docs\sand-cheat-sheet.md` file).

If you open the [site.conf](https://github.com/FatConan/sand/blob/master/example/site.conf) file you'll see a configuration file
that describes how to build the example.

### site.conf

The top level map of the `site.conf` file contains the "sites" array. This is a list of sites that will be built by this particular file.
Each site is represented as a map containing some or all of these keys (there may be additional keys depending on the plugins being used, but these are the keys providing the base functionality):
`root`, `output_root`, `plugins`, `templates`, `pages` and `resources`.

In the case of the example `site.conf` file we see the following keys:

- "root"
- "domain"
- "plugins"
- "es6css"
- "pages" 
- "templates"
- "resources"

#### root

`root` defines the working directory of this particular site relative to the folder provided to the python command. Any `source` folders
will be defined relative to the `root`.

In this case our configuration states `"root": "."` so the working directory of this site is the `example` folder.

#### output_root

`output_root` defines the output directory relative to the folder provided to the python command. Any `target` folders defined
will be relative to the `output_root`. 

We don't specify a value in the example `site.conf` file, so it takes the default value of `"./output"` (so `example/output` in this particular case).

#### templates

`templates` defines a list of folders relative to `root` where our jinja2 templates can be found. We'll reference these by name in 
our page configuration when we define our pages.  

In this case we list a single templates folder ```"templates": ["templates"],``` and this is again relative to our `root` so that 
it can be found at `example/templates` in this instance. If you inspect this [templates folder](https://github.com/FatConan/sand/tree/master/example/templates) you'll find a single jinja2 template named [default.html](https://github.com/FatConan/sand/blob/master/example/templates/default.html)

#### pages

`pages` defines a list of markdown "pages" to be rendered as HTML output.  Each page consists of a map that contains at the very least a `source` (relative to `root`) and `target` (relative to `output_root`) key, and optionally a `config` key that can be used provide additional metadata about the page to be generated. This is an alternative (and less intrusive) way of adding metadata to the markdown pages beyond including YAML definitions at the top of the document.  More about this can be found in the **pages** section below. 

In our example the `pages` entry looks like this:

    "pages": [
        {
            "config": {
                "title": "Sand Documentation",
                "template": "default.html",
                "is_index": true,
                "rss": true,
                "created": "2023-07-16 18:12:00",
            },
            "source": "../README.md",
            "target": "./index.html"
        },
        {
            "config": {
                "title": "Sand Cheat Sheet",
                "template": "default.html",
                "rss": true,
                "created": "2023-07-16 18:12:00",
            },
            "source": "../supplementary-docs/sand-cheat-sheet.md",
            "target": "./cheat-sheet.html"
        }
    ]


This defines two pages, one processing the `README.md` file and the other the `supplementary-docs/sand-cheat-sheet.md` file. 
In both cases we also tell the renderer to use the `default.html` template from the template folder defined earlier. Additionally,
we provide a page title for each page and add an `is_index` flag to the main README (both of which become accessible through the DATA object at render time, more about this in the **pages** & **templates** sections). We also specify an `rss` flag to enable the page to be processed by the built-in rss plugin. More about plugins can be found in the plugin section.

#### resources

`resources` defines a list of supporting files that may be static or may require some alternative processing to the markdown processing **Sand** provides for content. Typically, these files include things like Javascript, images, media and css. In the case of the latter on of the alternative processors provided by **Sand** is the compilation of `less` files into `css` (using [lesscpy](https://github.com/lesscpy/lesscpy)). 

The default handling of a resource file is simply to copy it from the source location to the target location.

#### plugins

`plugins` defines a list of plugins (either built-in, or project-specific) that can be used to augment the functionality of **Sand**. More on this in the [plugins](#plugins) section.

## Usage

To get started with **Sand**:

    # Create project layout
    sand <project_folder> --site <project_name>
    # Generate site
    sand <project_folder>
    # Add a new page to an existing project
    sand <project_folder> --page <page_name>

### Folder Structure

The structure of a project is pretty flexible and can be expanded and contracted by updating the `site.json` metadata, however,
a common example structure (and that created by the built in site generator) is:

    .
    ├── sandplugins (optional)
    |   └── plugin.py (defines a plugin class)
    ├── pages
    │   └── ... (.md files)
    ├── resources
    │   ├── css
    │   │   └── ... (styles)
    │   ├── script
    │   │   └── ... (javascript)
    │   └── img
    │       └── ... (images)
    ├── site.conf
    └── templates
        └── ... (jinja templates)


`site.conf` is pretty flexible about the location of templates and files. As such you're not constrained to any particular layout for your site. You could have separate template folders inside each site or have one giant mess in your project root.

As a demonstration, if you look at the `site.conf` for this example you'll see that the README.md file is being included from outside the project root folder while the templates are stored within it.

## Pages

Pages are Markdown files with some optional YAML metadata
that define the content of a page and describe the attributes of the generated page including the page title and
the template it uses. For example:


    template: base.html
    title: Hello, World
    
    # This is a header
    
    Here is some content.

Additionally, metadata can be provided within the `site.conf` at the point the page is defined (as seen in the example project above). 
This has the benefit of removing the need to "tarnish" the Markdown with a YAML header, but the drawback that it may not be effectively used 
when **wildcarding** pages.

In either case, Sand makes the metadata defined available to the page when rendered as a dictionary named DATA.
In the example above the title can be accessed within the template as:

```
{{ DATA.get("title") }}
```

### Using wildcards in page definitions

Individually identifying pages can be a chore, especially if we wish them to be rendered with a common set of metadata (or their metadata
is provided with a YAML header). In these cases we can use wildcards to indicate "all the matching files". A wildcard is denoted using `*` and
is used in both the `source` and `target` of a page entry.

Wildcards can be very useful when you wish to process a whole folder of Markdown files:

    "pages": [
        {
            "source": "blog/*.md",
            "target": "blog/*.html"
        }
    ]


The above directive will take all the .md files in the blog folder, and render them out to a folder of the same name in the 
output root. All the files will be read as `[name].md` and output as the corresponding `[name].html` file.  You can also specify
a `config` map at this point, but it'll apply equally to all the files, which can be useful for defining a template, but 
not for page specific information such as page titles.

## Templates

Templates are HTML pages with **[jinja2](http://jinja.pocoo.org)** markup.  An example of the file that Sand produces 
when using the site generator is shown below. 

`base.html`:

    <html>
      <head>
        {% block head %}
        <title>{{ DATA.get("title") }}</title>
        {% endblock %}
      <head>
      <body>
      {% block body %}
        <h1>{{ DATA.get("title") }}</title>
        <div id="post">
          <!-- Most likely we are going to pass more html here --->
          {{ content|safe }}
        </div>
      {% endblock %}
      </body>
    </html>

The important points here are that the HTML representation of the Markdown content which is provided through the `{{ content }}`
variable (and in the template above passed through `safe` to avoid it being escaped), the page level metadata in `{{ DATA }}`,
 and the site level metadata in `{{ GLOBALS }}`. More about `GLOBALS` can be found in the **advanced usage**.  
 
## Generating

To generate a particular site invoke `sand` with the location of the project's
root folder.

```
sand <project_folder>
```

## Example

An example project that generates an html version of this README can be found in
the example folder.

You can build it by running:

```
sand example
```

## Advanced Usage

### Content Jinja Pass

**Sand** allows a Jinja pass to be performed on the markdown allowing you to (carefully) mix your markdown content with Jinja directives.
When activated, the markdown content will receive a secondary Jinja rendering pass in which any Jinja directives will be processed.
When processed they will be provided access to all the same `DATA` and `GLOBALS` values as all the other Jinja rendering phase.

This feature can be enabled by including:

```
jinja_pass: True
```

either as part of your YAML header, or within a `config` section of the `pages` definition in your `site.conf` for any required pages.

### GLOBALS

As mentioned previously a dictionary of the data passed from the page metadata into the content/template of each page may be accessed through
the `DATA` object.  In addition to this, every rendering phase is also provided access to a `GLOBALS` object that contains data
regarding the project as a whole.

The `GLOBALS` currently is a dictionary with three elements: 

- `site_root`: the root folder of the project
- `output_root`: the output folder of the project
- `site`: the site object as defined in the `site.py` file that contains the page_reference which is a path-indexed 
dictionary of all the project's pages and metadata.

### Plugins

A site is represented by an instance of the [Site class](https://github.com/FatConan/sand/blob/master/config/site.py). When the site is instantiated it will read a list of plugin names from the `site.conf`. It will then attempt to instantiate the plugins by loading a module named `<plugin-name>.py` first from the project's `sandplugins` folder, then from **Sand's** own `plugin\builtins` folder. Should the module load. the plugin will be instantiated by calling `Plugin()` from the loaded module. 

In this example's `site.conf` we list three plugins:

    "plugins": [
        "es6css",
        "rss",
        "example"
    ]

This loads two built-in plugins (`es6css` and `rss`) from the `plugin\builtins` folder and a third plugin (`example`) from the `example\sandplugins\` folder.

A plugin is defined as a class named `Plugin` requiring the following methods:

    class Plugin:
        def configure(self, site_data, site):
            pass
    
        def parse(self, site_data, site):
            pass
    
        def add_render_context(self, page, environment, data):
            pass 

With `sand` installed using pip, you can optionally base your Plugin class on the `SandPlugin` class like so:

    from sand.plugin import SandPlugin
    
    class Plugin(SandPlugin):
        pass

Which will provide all the stubs for you allowing you to only override those methods you require.

You can create a plugin named `<name>` by creating a class named `Plugin` in a `<name>.py` file within a folder named `sand` under your project root. Your plugin will have the ability to hook into the **Sand** process at both the stage at which the site structure is being constructed, and at the point the content is rendered. This can be done by modifying the `parse` and `add_render_context` methods. 

    .
    ├── sandplugins
    │   └── <plugin>.py
    └── site.conf


By way of example, if we add a list of terms to pages as "tags" in their metadata:

    "pages": [
        {
            "config": {
                "title": "Sand Documentation",
                "template": "default.html",
                "is_index": true,
                "rss": true,
                "created": "2023-07-16 18:12:00"
                "tags": ["guide"]
            },
            "source": "./README.md",
            "target": "./index.html"
        },
        {
            "config": {
                "title": "Sand Cheat Sheet",
                "template": "default.html",
                "rss": true,
                "created": "2023-07-16 18:12:00"
                "tags": ["guide", "cheat sheet"]
            },
            "source": "../supplementary-docs/sand-cheat-sheet.md",
            "target": "./cheat-sheet.html"
        }
    ]

We can then create a new `Plugin` class that will allow us to fetch the pages by their tag like so:
    
    from sand.plugin import SandPlugin


    class Tags:
        def __init__(self, pages):
            self.pages = pages
        
         def by_tag(self, tag):
                   return [p for p in self.pages if tag in p.data("tags", [])]


    class Plugin(SandPlugin):
        def __init__(self):
            self.tags = None

        def configure(self, site_data, site):
            self.tags = Tags(site.pages)

        def add_render_context(self, page, environment, data):
            data["TAGS"] = self.tags

If we save this plugin as `tags.py` in our project's `sand` folder then we'll be able to include it by adding `"tags"` to the list of plugins in our `site.conf` file. The `add_render_context` call will add a variable to our jinja environment names `TAGS` that allows us to access the `by_tag` method from within our templates or our `jinja_pass` enabled markdown like:

    {% for page in TAGS.by_tag("guide") %}
        {{ page.data("title") }}
    {% endfor %}

We could further augment the Tags class to provide the data for creating a tag cloud or any other function we would like.

The `add_render_context` method also allows you to augment the `jinja2` environment object (as passed as an argument to it) so that you can extend the templating functionality for a project. The plugin in `example.py` of this documentation's project adds a filter named `nl2br` that replaces new lines with html breaks.  

    class Plugin(SandPlugin):
        @staticmethod
        def nl2br(value):
            return value.replace("\n", "<br />")
    
        def add_render_context(self, page, environment, data):
            environment.filters["nl2br"] = self.nl2br

This can then be accessed within a template by piping content through the newly defined filter:

    {{ content|nl2br|safe }}
    
