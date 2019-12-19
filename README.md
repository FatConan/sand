# Sand: A simple static site generator

**Sand** is a static site generator based heavily on an early version of [Stone](https://github.com/neuralsandwich/stone) by
[NeuralSandwich](https://github.com/neuralsandwich). While **Stone** is becoming a more fully featured blog engine, **Sand**
pairs back functionality to the basics, and is designed to provide similar functionality to the early versions of Stone, but 
with added wildcard support, support for resources, and some other functions that proved useful when building projects.

## Built on Sand
This **README** serves as both documentation for this tool as well as an example project.  While this file contains the content, 
there are a number pieces of additional metadata required to configure the **Sand** project, which are provided by the accompanying `site.json` JSON file.

To see **Sand** generate this documentation, clone this repository and run:

```
python3 sand.py example
```

from within the checked out folder.

## Configuration 

Describing the configuration in the `site.json` file we'll make reference to how we build our example. 

**NB:** In previous versions of `Sand` the configuration had been read only as JSON, but now is read as HOCON using [pyhocon](https://github.com/chimpler/pyhocon/). This preserves backwards compatibility, but also allows for the 
configuration bells and whistles that [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) supports. To make this a little less jarring
`Sand` will now also attempt to read configuration data from `site.hocon` and `site.conf` in addition to `site.json` to ease any 
nomenclature-based anxiety.

When the above command is run the `site.json` informs **Sand** how to build the HTML output, and **Sand** follows these 
instructions to create a styled, HTML version of the README markdown 
(additionally it creates a `site.json` cheat sheet from the ConfigurationCheatSheet.md file).

If you open the [site.json](https://github.com/FatConan/sand/blob/master/example/site.json) file you'll see a configuration file
that describes how to build the example.

### site.json

The top level map of the site.json file contains the "sites" array. This is a list of sites that will be built by this particular file.
Each site is represented as a map containing some or all of these keys:
`root`, `output_root`, `templates`, `pages` and `resources`.

#### root

`root` defines the working directory of this particular site relative to the folder provided to the python command. Any `source` folders
will be defined relative to the `root`.

In this case our configuration states `"root": "."` so the working directory of this site is the `example` folder.

#### output_root

`output_root` defines the output directory relative to the folder provided to the python command. Any `target` folders defined
will be relative to the `output_root`. 

We don't specify a value in the example `site.json` file so it takes the default value of `"./output"` (so `example/output` in this case).

#### templates

`templates` defines a list of folders relative to `root` where our jinja2 templates can be found. We'll reference these by name in 
our page configuration when we define our pages.  

In this case we list a single templates folder ```"templates": ["templates"],``` and this is again relative to our `root` so that 
it can be found at `example/templates` in this instance. If you inspect this [templates folder](https://github.com/FatConan/sand/tree/master/example/templates) you'll find a single jinja2 template named [default.html](https://github.com/FatConan/sand/blob/master/example/templates/default.html)

#### pages

`pages` defines a list of markdown "pages" to be rendered as HTML output.  Each page consists of a map that contains at the very least a 
`source` (relative th `root`) and `target` (relative to `output_root`) key, and optionally a `config` key that can be used provide additional metadata about the page to be generated. This is an alternative
(and less intrusive) way of adding metadata to the markdown pages beyond including YAML definitions at the top of the document.  More about this
can be found in the **pages** section below. 

In our example the `pages` entry looks like this:

```
"pages": [
    {
        "config": {
            "title": "Sand Documentation",
            "template": "default.html",
            "is_index": true
        },
        "source": "../README.md",
        "target": "./index.html"
    },
    {
        "config": {
            "title": "Sand Cheat Sheet",
            "template": "default.html"
        },
        "source": "../supplementary-docs/sand-cheat-sheet.md",
        "target": "./cheat-sheet.html"
    }
]
```

This defines two pages, one processing the `README.md` file and the other the `supplementary-docs/SandCheatSheet.md` file. 
In both cases we also tell the renderer to use the `default.html` template from the template folder defined earlier. Additionally
we provide a page title for each page and add an `is_index` flag to the main README (both of which become accessible through the DATA object at render time,
 more about this in the **pages** & **templates** sections).

## Usage

To get started with `Sand`:

    # Create project layout
    python3 sand.py <project_folder> --site <project_name>
    # Generate site
    python3 sand.py <project_folder>
    # Add a new page to an existing project
    python3 sand.py <project_folder> --page <page_name>

### Folder Structure

The structure of a project is pretty flexible and can be expanded and contracted by updating the `site.json` metadata, however,
a common example structure (and that created by the built in site generator) is:

    .
    ├── pages
    │   └── ... (.md files)
    ├── resources
    │   ├── css
    │   │   └── ... (styles)
    │   ├── script
    │   │   └── ... (javascript)
    │   └── img
    │       └── ... (images)
    ├── site.json
    └── templates
        └── ... (jinja templates)


`site.json` is pretty flexible about the location of
templates and files. As such you're not constrained to any particular layout for
your site. You could have separate template folders inside each site or have
one giant mess in your project root.

As a demonstration, if you look at the `site.json` for this example you'll see that the 
README.md file is being included from outside the 
project root folder while the templates are stored within it.


## Pages

Pages are Markdown files with some optional YAML metadata
that define the content of a page and describe the attributes of the generated page including the page title and
the template it uses. For example:


    template: base.html
    title: Hello, World
    
    # This is a header
    
    Here is some content.

Additionally metadata can be provided within the `site.json` at the point the page is defined (as seen in the example project above). 
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

```
"pages": [
    {
        "source": "blog/*.md",
        "target": "blog/*.html"
    }
]
```

The above directive will take all the .md files in the blog folder, and render them out to a folder of the same name in the 
output root. All the files will be read as `[name].md` and output as the corresponding `[name].html` file.  You can also specify
a `config` map at this point, but it'll apply equally to all of the files, which can be useful for defining a template, but 
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

To generate a particular site invoke `sand.py` with the location of the project's
root folder.

```
python3 sand.py <project_folder>
```

## Example

An example project that generates an html version of this README can be found in
the example folder.

You can build it by running:

```
python3 sand.py example
```

## Advanced Usage

### Content Jinja Pass

`Sand` allows a Jinja pass to be performed on the markdown allowing you to (carefully) mix your markdown content with Jinja directives.
When activated, the markdown content will receive a secondary Jinja rendering pass in which any Jinja directives will be processed.
When processed they will be provided access to all of the same `DATA` and `GLOBALS` values as all the other Jinja rendering phase.

This feature can be enabled by including:

```
jinja_pass: True
```

as part of your YAML header for any required pages.

### GLOBALS

As mentioned previously a dictionary of the data passed from the page metadata into the content/template of each page may be accessed through
the `DATA` object.  In addition to this, every rendering phase is also provided access to a `GLOBALS` object that contains data
regarding the project as a whole.

The `GLOBALS` currently is a dictionary with three elements: 

- `site_root`: the root folder of the project
- `output_root`: the output folder of the project
- `site`: the site object as defined in the `site.py` file that contains the page_reference which is a path-indexed 
dictionary of all the project's pages and metadata.

### Extended Site object

A site is represented by an instance of the [Site class](https://github.com/FatConan/sand/blob/master/config/site.py). 
You can extend this class by creating a class named `SiteExt` in an `extensions.py` file a folder called `sand` under the project root. 
Your `SiteExt` will be used to create a new `Site` class that extends both `Site` and `SiteExt` that you can then use to add logic
that you can't otherwise achieve in the templates.

    .
    ├── sand
    │   └── extensions.py
    └── site.json


By way of example, if we add a list of terms to pages as "tags" in their metadata:

    "pages": [
        {
            "config": {
                "title": "Sand Cheat Sheet",
                "template": "default.html",
                "tags": ["guide"]
            },
            "source": "./README.md",
            "target": "./index.html"
        },
        {
            "config": {
                "title": "Sand Cheat Sheet",
                "template": "default.html",
                "tags": ["guide", "cheat sheet"]
            },
            "source": "../supplementary-docs/sand-cheat-sheet.md",
            "target": "./cheat-sheet.html"
        }
    ]

We can then create a new `SiteExt` class that will allow us to fetch the pages by their tag like so:


    class SiteExt:
        def by_tag(self, tag):
           return [p for p in self.pages if tag in p.page_data.get("tags")]


Our site instance would then be augmented with this at render time so that we could reference the method from within our
templates or our `jinja_pass` enabled markdown:


    {% set guides = GLOBALS["site"].by_tag("guide") %} 
    {% for page in guides %}
        <li>{{ page.data("title") }}</li>
    {% endfor %}


