PAGE_TEMPLATE = """title: [Add a page title]
template: [The template used to render]

# Page Header

This new markdown page will need to either be added to your site.json for rendering or may be picked up automatically if 
contained in a folder using wildcard rules to render.

"""

SITE_CONF_BASIC = """{"sites": [
    {
        "root": "%s",
        "output_root": "output",
        "plugins": [
            "es6css"
        ],
        "es6css": {
            "CSS": ["/resources/css/style.css"]
            "CDN": [
                {"alias": "jquery", "src": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js"}
                {"alias": "underscore", "src": "https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.13.6/underscore-esm.min.js"}
            ],
            "scripts": []
        }
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
                "source": "./resources/css/*.less",
                "target": "./resources/css/*.css"
                "resource_type": "less"
            },
            {
                "source": "./resources/script",
                "target": "./resources/script"
            },
            {
                "source": "./resources/img",
                "target": "./resources/img"
            }
        ]
    }
]}"""

TEMPLATE_HTML = """<!DOCTYPE html>
<html>
    <head lang="en">
        <meta charset="UTF-8" />
        <title>{{ DATA.get("title") }}</title>
        {{ ES6CSS.headers() | safe }}
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

RESET_LESS = """/* http://meyerweb.com/eric/tools/css/reset/
   v2.0 | 20110126
   License: none (public domain)
*/

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
	display: block;
}
body {
	line-height: 1;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}"""

STYLE_LESS = """
import "reset.less";

"""