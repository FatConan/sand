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

When the above command is run the `site.json` informs **Sand** how to build the HTML output, and **Sand** follows these 
instructions to create a styled, HTML version of the README markdown 
(additionally it creates a `site.json` cheat sheet from the ConfigurationCheatSheet.md file).

If you open the [site.json](https://github.com/FatConan/sand/blob/master/example/site.json) file you'll see a configuration file
that describes how to build the example.

### site.json

The top level map of the site.json file contains the "sites" array. This is a list of sites that will be built by this particular file.
Each site is represented as a map containing up to four keys:
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
`pages` defines 

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
templates and files. As such your not constrained to any particular layout for
your site. You could have separate template folders inside each site or have
one giant mess in your project root.

As a demonstration, if you look at the `site.json` for this example you'll see that the 
README.md file is being included from outside the 
project root folder while the templates are stored within it.


## Pages

Pages are Markdown files with some optional YAML metadata
that describe the attributes of the generated page including the page title and
the template it uses. For example:


    template: base.html
    title: Hello, World
    
    # This is a header
    
    Here is some content.

Sand makes the metadata defined within the YAML header available to the page when rendered as a dictionary named DATA.
In the example above the title can be accessed within the template as:


```
{{ DATA.get("title") }}
```

## Templates

Templates are HTML pages with **[jinja2](http://jinja.pocoo.org)** markup.

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


## Generating

To generate a particular site invoke `sand.py` with the location of the project's
root folder.

```
python3 sand.py <project_folder>
```

### Example

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
When processed they will be provided access to all of the same DATA and GLOBAL values as all the other Jinja rendering phase.

This feature can be enabled by including:

```
jinja_pass: True
```

as part of your YAML header for any required pages.

### GLOBALS

As mentioned previously a dictionary of the data passed from the YAML into the content/template of each page may be accessed through
the `DATA` object.  In addition to this, every rendering phase is also provided access to a `GLOBALS` object that contains data
regarding the project as a whole.

The `GLOBALS` currently is a dictionary with three elements: 

- `site_root`: the root folder of the project
- `output_root`: the output folder of the project
- `site`: the site object as defined in the `site.py` file that contains the page_reference which is a path-indexed dictionary of all the project's pages and metadata.
 