# Sand : A simple static site generator

**Sand** is a static site generator based heavily on an early version of [Stone](https://github.com/neuralsandwich/stone) by
[NeuralSandwich](https://github.com/neuralsandwich). While **Stone** is becoming a more fully featured blog engine, **Sand**
pairs back functionality to the basics, and is designed to provide similar functionality to the early versions of Stone, but 
with added wildcard support, support for resources, and some other functions that proved useful when building projects.

# Built on Sand
This **README** serves as both documentation for this tool as well as an example project. 
If looking at this in Github you'll notice
that this file is rendering with the line:

```
title: Sand Documentation template: default.html
```

at the start of the document. This is part of the metadata required by **Sand** to render this page (written in YAML). The rest of the required
metadata is provided in an accompanying `site.json` JSON file.

To see **Sand** generate this documentation, clone this repository and run:
```bash
python3 sand.py example
```
from within the checked out folder.

# Usage

To get started with `Sand`:

    # Create project layout
    python3 sand.py <project_folder> --site <project_name>
    # Generate site
    python3 sand.py <project_folder>
    # Add a new page to an existing project
    python3 sand.py <project_folder> --page <page_name>

## Folder Structure

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
 